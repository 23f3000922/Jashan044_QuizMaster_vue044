from flask_restful import Resource, reqparse
from flask import jsonify
from models import db, Subject, Chapter, Quiz, Question,Score,User
from datetime import datetime


class QuizListResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=False, location='args')  
        args = parser.parse_args()

        if args['user_id'] is not None:
            attempted_quiz_ids = [score.quiz_id for score in Score.query.filter_by(user_id=args['user_id']).all()]
            available_quizzes = Quiz.query.filter(~Quiz.id.in_(attempted_quiz_ids)).all()
            completed_quizzes = Quiz.query.filter(Quiz.id.in_(attempted_quiz_ids)).all()
        else:
            available_quizzes = Quiz.query.all()
            completed_quizzes = []

        def quiz_to_dict(quiz):
            chapter = quiz.chapter
            subject = chapter.subject if chapter else None
            return {
                'id': quiz.id,
                'quiz_name': quiz.name,
                'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d %H:%M:%S') if quiz.date_of_quiz else None,
                'time_duration': quiz.time_duration,
                'remarks': quiz.remarks,
                'chapter_name': chapter.name if chapter else None,
                'subject_name': subject.name if subject else None,
                'number_of_questions': len(quiz.questions)
            }

        result = {
            'available_quizzes': [quiz_to_dict(quiz) for quiz in available_quizzes],
            'completed_quizzes': [quiz_to_dict(quiz) for quiz in completed_quizzes]
        }
        return result, 200
class ScoreResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, location='args')
        args = parser.parse_args()
        user_id = args['user_id']

        
        scores = Score.query.filter_by(user_id=user_id).all()
        result = []
        for score in scores:
            quiz = Quiz.query.get(score.quiz_id)
            if not quiz:
                continue

            total_questions = len(quiz.questions)
            right = score.total_scored if score.total_scored is not None else 0
            wrong = total_questions - right if total_questions >= right else 0

            result.append({
                "quiz_id": quiz.id,
                "quiz_name": quiz.name,
                "score": right,
                "total_questions": total_questions,
                "right": right,
                "wrong": wrong,
                "date_attempted": score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S') if score.time_stamp_of_attempt else None
            })
        return {"scores": result}, 200
   
    def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('quiz_id', type=int, required=True)
            parser.add_argument('user_id', type=int, required=True)
            parser.add_argument('total_scored', type=int, required=True)
            args = parser.parse_args()

            # Check if a score already exists for this user/quiz
            existing = Score.query.filter_by(quiz_id=args['quiz_id'], user_id=args['user_id']).first()
            if existing:
                # Allow only one reattempt: if already reattempted, block further tries
                if getattr(existing, 'reattempted', False):
                    return {'message': 'You have already reattempted this quiz.'}, 400
                # Overwrite the score and mark as reattempted
                existing.total_scored = args['total_scored']
                existing.time_stamp_of_attempt = datetime.utcnow()
                existing.reattempted = True  
                db.session.commit()
                return {'message': 'Score updated successfully (reattempt).'}, 200

            # First attempt
            score = Score(
                quiz_id=args['quiz_id'],
                user_id=args['user_id'],
                total_scored=args['total_scored'],
                time_stamp_of_attempt=datetime.utcnow(),
                reattempted=False  
            )
            db.session.add(score)
            db.session.commit()
            return {'message': 'Score saved successfully.'}, 201    

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'qualification': user.qualification,
                'dob': user.dob.strftime('%Y-%m-%d') if user.dob else None,
                'role': user.role
            })
        return user_list, 200

class UserScoreResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID is required', location='args')
        args = parser.parse_args()
        user = User.query.get(args['user_id'])
        if not user:
            return {'message': 'User not found'}, 404

        scores = Score.query.filter_by(user_id=args['user_id']).all()
        result = []
        for s in scores:
            quiz = Quiz.query.get(s.quiz_id)
            chapter = Chapter.query.get(quiz.chapter_id) if quiz else None
            subject = Subject.query.get(chapter.subject_id) if chapter else None
            result.append({
                'quiz_id': quiz.id if quiz else None,
                'quiz_name': quiz.name if quiz else None,
                'chapter_name': chapter.name if chapter else None,
                'subject_name': subject.name if subject else None,
                'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d %H:%M:%S') if quiz and quiz.date_of_quiz else None,
                'score': s.total_scored,
                'reattempted': s.reattempted,
                'attempted_on': s.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S') if s.time_stamp_of_attempt else None
            })
        return result, 200    