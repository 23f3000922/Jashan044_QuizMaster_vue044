from flask import Flask , request, jsonify , send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db, User, Subject  , Chapter ,Quiz , Question , Score    
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from subject import SubjectResource , ChapterResource , QuestionResource , QuizResource
from authorization.authorization import  QuizListResource , ScoreResource , UserResource, UserScoreResource
from celery_init import celery_init_app
from task import csv_report, monthly_user_report, daily_user_reminders
from celery.result import AsyncResult
import os
from celery.schedules import crontab
from subject import cache

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'quizmaster'
app.config['celery_config'] = {
    'broker_url': 'redis://localhost:6379/0',
    'result_backend': 'redis://localhost:6379/0',
    'Timezone' : 'Asia/kolkata',
    'task_ignore_result': False,
    'broker_connection_retry_on_startup': True  
}
from flask_migrate import Migrate

migrate = Migrate(app, db)
cache.init_app(app)

db.init_app(app)
CORS(app, origins='*')
jwt = JWTManager(app)
api = Api(app)

celery = celery_init_app(app)
celery.autodiscover_tasks()


@app.route('/test-cache')
def test_cache():
    from app import cache
    if not cache.get('test'):
        cache.set('test', 'cached!', timeout=60)
        return 'Set in cache'
    return 'From cache: ' + cache.get('test')

class SignupResource(Resource):
    
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('username', type=str , required=True , help='Username is required')
        parser.add_argument('password', type=str , required=True , help='Password is required')
        parser.add_argument('email', type=str , required=True , help='Email is required')
        parser.add_argument('qualifications', type=str , required=False , help='Qualification is optional')
        parser.add_argument('dob', type=str , required=False , help='Date of birth is optional')
        args = parser.parse_args()
        print(args)

        if User.query.filter_by(username=args['username']).first():
            return {'message': 'Username already exists'}, 400
        if User.query.filter_by(email=args['email']).first():
            return {'message': 'email already exists'}, 400
        
        hash_password=generate_password_hash(args['password'])

        new_user = User(
                        username=args['username'],
                        email=args['email'],  
                        password=hash_password,
                        qualification=args['qualifications'],
                        dob=datetime.strptime(args['dob'], '%Y-%m-%d') if args['dob'] else None,
                        role='user'  
                       )

        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201


class LoginResource(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('username', type=str , required=True , help='Username is required')
        parser.add_argument('password', type=str , required=True , help='Password is required')
        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()
        if user and check_password_hash(user.password, args['password']):
            access_token = create_access_token(identity=user.role)
            user_info = {
                "id": user.id,
                "username": user.username,
                "role": user.role

            }
           

            return {'access_token': access_token, 'user': user_info}, 200
        else:
            return {'message': 'Invalid credentials'}, 401
        

class GetQuizStats(Resource):
    def get(self):
        quizzes = Quiz.query.all()
        stats = []
        for quiz in quizzes:
            scores = Score.query.filter_by(quiz_id=quiz.id).all()
            highest_mark = max((score.total_scored for score in scores if score.total_scored is not None), default=0)
            attempts = len(scores)
            stats.append({
                'quiz_id': quiz.id,
                'quiz_name': quiz.name,
                'highest_mark': highest_mark,
                'attempts': attempts
            })
        return jsonify(stats)
class UserSummaryResource(Resource):
    def get(self):
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return {'message': 'user_id is required'}, 400

        # Bar chart: Highest marks per quiz for this user
        quiz_stats = []
        quizzes = Quiz.query.all()
        for quiz in quizzes:
            scores = Score.query.filter_by(quiz_id=quiz.id, user_id=user_id).all()
            highest_mark = max((s.total_scored for s in scores if s.total_scored is not None), default=0)
            quiz_stats.append({
                "quiz_id": quiz.id,
                "quiz_name": quiz.name,
                "highest_mark": highest_mark
            })

        # Pie chart: Number of quizzes attempted per subject
        subject_stats = []
        subjects = Subject.query.all()
        for subject in subjects:
            subject_quizzes = Quiz.query.join(Chapter).filter(Chapter.subject_id == subject.id).all()
            attempted_count = 0
            for quiz in subject_quizzes:
                # Check if user has attempted this quiz (has at least one score)
                scores = Score.query.filter_by(quiz_id=quiz.id, user_id=user_id).all()
                if scores:  # If user has attempted this quiz
                    attempted_count += 1
            
            subject_stats.append({
                "subject_id": subject.id,
                "subject_name": subject.name,
                "attempted_count": attempted_count
            })

        return jsonify({
            "quiz_stats": quiz_stats,
            "subject_stats": subject_stats
        })

@app.route('/api/export_users_csv', methods=['POST'])
def export_service_requests():
    result = csv_report.delay()
    return jsonify({
        "message": "CSV export started successfully",
        "task_id": result.id
    }), 200

@app.route('/api/csv_result/<task_id>', methods=['GET'])
def csv_result(task_id):
    result = celery.AsyncResult(task_id)
    if result.ready():
        if result.successful():
            filename = result.get()
            export_dir = os.path.join(app.root_path, 'static', 'exports')
            
            print(f"Serving file: {filename} from {export_dir}")
            try:
                return send_from_directory(export_dir, filename, as_attachment=True)
            except Exception as e:
                
                print(f"Error sending file: {e}")
                return jsonify({"status": "Failed", "error": str(e)}), 500
        else:
            return jsonify({
                "status": "Failed",
                "error": str(result.result)
            }), 500
    else:
        return jsonify({
            "status": "Processing",
            "task_id": task_id
        }), 202





@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    # Daily at 9:00 AM
    sender.add_periodic_task(
        crontab(minute = '*/2'),
        #crontab(hour=9, minute=0),
        daily_user_reminders.s(),
        name="Daily Reminder for Users Without Quiz Attempts"
    )
    
    sender.add_periodic_task(
        crontab(minute = '*/2'),
        #crontab(minute=0, hour=0, day_of_month=1), 
        monthly_user_report.s(),
        name="Monthly Reminder" 
    )        
api.add_resource(SignupResource, '/api/signup') 
api.add_resource(LoginResource, '/api/login')   
api.add_resource(SubjectResource, '/api/subject')  
api.add_resource(ChapterResource, '/api/chapter')
api.add_resource(QuizResource, '/api/quiz')
api.add_resource(QuestionResource, '/api/question')
api.add_resource(QuizListResource, '/api/quizzes')
api.add_resource(ScoreResource, '/api/score')
api.add_resource(UserResource, '/api/users')
api.add_resource(UserScoreResource, '/api/user-scores')
api.add_resource(GetQuizStats, '/api/quiz-stats')
api.add_resource(UserSummaryResource, '/api/user-summary')






if __name__ == '__main__':
    app.run(debug=True)