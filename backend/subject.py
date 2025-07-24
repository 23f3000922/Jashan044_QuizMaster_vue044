from flask_restful import Resource, reqparse
from flask import jsonify
from models import db, Subject, Chapter, Quiz, Question,Score
from datetime import datetime
from flask_caching import Cache
from flask import request

cache = Cache(config={'CACHE_TYPE':'SimpleCache','CACHE_DEFAULT_TIMEOUT': 300})
class SubjectResource(Resource):
    @cache.cached(timeout=60, key_prefix='subject_data')
    def get(self):
        subjects = Subject.query.all()

        return [{
            'id': subject.id,
            'name': subject.name,
            'description': subject.description,
            'chapters': [chapter.name for chapter in subject.chapters]
        } for subject in subjects], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Subject name is required')
        parser.add_argument('description', type=str, required=False, help='Subject description is optional')
        args = parser.parse_args()

        if Subject.query.filter_by(name=args['name']).first():
            return {'message': 'Subject already exists'}, 400

        new_subject = Subject(name=args['name'], description=args['description'])
        db.session.add(new_subject)
        db.session.commit()
        cache.delete('subject_data')
        return {'message': 'Subject created successfully'}, 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=False)
        args = parser.parse_args()

        subject = Subject.query.get(args['id'])
        if not subject:
            return {'message': 'Subject not found'}, 404

        subject.name = args['name']
        subject.description = args['description']
        db.session.commit()
        cache.delete('subject_data')
        return {'message': 'Subject updated successfully'}, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()

        subject = Subject.query.get(args['id'])
        if not subject:
            return {'message': 'Subject not found'}, 404

        db.session.delete(subject)
        db.session.commit()
        cache.delete('subject_data')
        return {'message': 'Subject deleted successfully'}, 200

class ChapterResource(Resource):
    #@cache.cached(timeout=300, key_prefix='chapter_data')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('subject_id', type=int, required=True, help='Subject ID is required', location='args')
        args = parser.parse_args()

        subject = Subject.query.get(args['subject_id'])
        if not subject:
            return {'message': 'Subject not found'}, 404

        chapters = Chapter.query.filter_by(subject_id=args['subject_id']).all()
        return [{
            'id': chapter.id,
            'name': chapter.name,
            'description': chapter.description
        } for chapter in chapters], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('subject_id', type=int, required=True, help='Subject ID is required')
        parser.add_argument('name', type=str, required=True, help='Chapter name is required')
        parser.add_argument('description', type=str, required=False)
        args = parser.parse_args()

        subject = Subject.query.get(args['subject_id'])
        if not subject:
            return {'message': 'Subject not found'}, 404

        
        if Chapter.query.filter_by(subject_id=args['subject_id'], name=args['name']).first():
            return {'message': 'Chapter with this name already exists in the subject'}, 400

        new_chapter = Chapter(
            name=args['name'],
            description=args['description'],
            subject_id=args['subject_id']
        )
        db.session.add(new_chapter)
        db.session.commit()
        #cache.delete('chapter_data')
        return {'message': 'Chapter created successfully'}, 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='Chapter ID is required')
        parser.add_argument('name', type=str, required=True, help='Chapter name is required')
        parser.add_argument('description', type=str, required=False)
        args = parser.parse_args()

        chapter = Chapter.query.get(args['id'])
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        
        if Chapter.query.filter(
            Chapter.subject_id == chapter.subject_id,
            Chapter.name == args['name'],
            Chapter.id != args['id']
        ).first():
            return {'message': 'Another chapter with this name already exists in the subject'}, 400

        chapter.name = args['name']
        chapter.description = args['description']
        db.session.commit()
        #cache.delete('chapter_data')
        return {'message': 'Chapter updated successfully'}, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='Chapter ID is required')
        args = parser.parse_args()

        chapter = Chapter.query.get(args['id'])
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        db.session.delete(chapter)
        db.session.commit()
        #cache.delete('chapter_data')
        return {'message': 'Chapter deleted successfully'}, 200


class QuizResource(Resource):

    def _make_quiz_cache_key(self):
        """Generate cache key for quiz data based on chapter_id"""
        chapter_id = request.args.get('chapter_id')
        return f"quiz_data_{chapter_id}" if chapter_id else "quiz_data_none"

    @cache.cached(timeout=300, make_cache_key=_make_quiz_cache_key)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('chapter_id', type=int, required=True, help='Chapter ID is required', location='args')
        args = parser.parse_args()

        chapter = Chapter.query.get(args['chapter_id'])
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        quizzes = Quiz.query.filter_by(chapter_id=args['chapter_id']).all()
        return [{
            'id': quiz.id,
            'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d %H:%M:%S') if quiz.date_of_quiz else None,
            'time_duration': quiz.time_duration,
            'quiz_name':quiz.name,
            'remarks': quiz.remarks,
            'chapter_name': chapter.name,
            'number_of_questions': len(quiz.questions)
        } for quiz in quizzes], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('chapter_id', type=int, required=True, help='Chapter ID is required')
        parser.add_argument('quiz_name', type=str, required=True, help='Quiz name is required')
        parser.add_argument('date_of_quiz', type=str, required=False)
        parser.add_argument('time_duration', type=str, required=False)
        parser.add_argument('remarks', type=str, required=False)
        args = parser.parse_args()

        chapter = Chapter.query.get(args['chapter_id'])
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        date_of_quiz = datetime.strptime(args['date_of_quiz'], '%Y-%m-%d %H:%M:%S') if args['date_of_quiz'] else datetime.utcnow()
        new_quiz = Quiz(
            chapter_id=args['chapter_id'],
            date_of_quiz=date_of_quiz,
            name=args['quiz_name'],
            time_duration=args['time_duration'],
            remarks=args['remarks']
        )
        db.session.add(new_quiz)
        db.session.commit()
        
        
        cache.delete(f"quiz_data_{args['chapter_id']}")
        
        return {'message': 'Quiz created successfully', 'quiz_id': new_quiz.id}, 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='Quiz ID is required')
        parser.add_argument('chapter_id', type=int, required=False, help='Chapter ID is required')
        parser.add_argument('date_of_quiz', type=str, required=False)
        parser.add_argument('time_duration', type=str, required=False)
        parser.add_argument('remarks', type=str, required=False)
        parser.add_argument('quiz_name', type=str, required=False)  
        args = parser.parse_args()

        quiz = Quiz.query.get(args['id'])
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        
      
        original_chapter_id = quiz.chapter_id
        
        if args['chapter_id']:
            chapter = Chapter.query.get(args['chapter_id'])
            if not chapter:
                return {'message': 'Chapter not found'}, 404
            quiz.chapter_id = chapter.id

        if args['date_of_quiz']:
            quiz.date_of_quiz = datetime.strptime(args['date_of_quiz'], '%Y-%m-%d %H:%M:%S')
        if args['time_duration']:
            quiz.time_duration = args['time_duration']
        if args['remarks']:
            quiz.remarks = args['remarks']
        if args['quiz_name']:
            quiz.name = args['quiz_name']
        
        db.session.commit()
        
        
        cache.delete(f"quiz_data_{original_chapter_id}")
        
       
        if args['chapter_id'] and args['chapter_id'] != original_chapter_id:
            cache.delete(f"quiz_data_{args['chapter_id']}")
        
        return {'message': 'Quiz updated successfully'}, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='Quiz ID is required')
        args = parser.parse_args()

        quiz = Quiz.query.get(args['id'])
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        chapter_id = quiz.chapter_id
        
        db.session.delete(quiz)
        db.session.commit()
        
        cache.delete(f"quiz_data_{chapter_id}")
        
        return {'message': 'Quiz deleted successfully'}, 200

class QuestionResource(Resource):
   
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('quiz_id', type=int, required=True, help='Quiz ID is required', location='args')
        args = parser.parse_args()

        quiz = Quiz.query.get(args['quiz_id'])
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        questions = Question.query.filter_by(quiz_id=args['quiz_id']).all()
        return [{
            'id': q.id,
            'question_statement': q.question_statement,
            'option1': q.option1,
            'option2': q.option2,
            'option3': q.option3,
            'option4': q.option4,
            'correct_option': q.correct_option
        } for q in questions], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('quiz_id', type=int, required=True, help='Quiz ID is required')
        parser.add_argument('question_statement', type=str, required=True, help='Question statement is required')
        parser.add_argument('option1', type=str, required=True)
        parser.add_argument('option2', type=str, required=True)
        parser.add_argument('option3', type=str, required=True)
        parser.add_argument('option4', type=str, required=True)
        parser.add_argument('correct_option', type=int, required=True, help='Correct option (1-4) is required')
        args = parser.parse_args()

        quiz = Quiz.query.get(args['quiz_id'])
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        if args['correct_option'] not in [1, 2, 3, 4]:
            return {'message': 'Correct option must be 1, 2, 3, or 4'}, 400

        new_question = Question(
            quiz_id=args['quiz_id'],
            question_statement=args['question_statement'],
            option1=args['option1'],
            option2=args['option2'],
            option3=args['option3'],
            option4=args['option4'],
            correct_option=args['correct_option']
        )
        db.session.add(new_question)
        db.session.commit()
        
        return {'message': 'Question added successfully', 'question_id': new_question.id}, 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='Question ID is required')
        parser.add_argument('question_statement', type=str, required=False)
        parser.add_argument('option1', type=str, required=False)
        parser.add_argument('option2', type=str, required=False)
        parser.add_argument('option3', type=str, required=False)
        parser.add_argument('option4', type=str, required=False)
        parser.add_argument('correct_option', type=int, required=False)
        args = parser.parse_args()

        question = Question.query.get(args['id'])
        if not question:
            return {'message': 'Question not found'}, 404

        if args['question_statement']:
            question.question_statement = args['question_statement']
        if args['option1']:
            question.option1 = args['option1']
        if args['option2']:
            question.option2 = args['option2']
        if args['option3']:
            question.option3 = args['option3']
        if args['option4']:
            question.option4 = args['option4']
        if args['correct_option']:
            if args['correct_option'] not in [1, 2, 3, 4]:
                return {'message': 'Correct option must be 1, 2, 3, or 4'}, 400
            question.correct_option = args['correct_option']
        db.session.commit()
        
        return {'message': 'Question updated successfully'}, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='Question ID is required')
        args = parser.parse_args()

        question = Question.query.get(args['id'])
        if not question:
            return {'message': 'Question not found'}, 404

        db.session.delete(question)
        db.session.commit()
        
        return {'message': 'Question deleted successfully'}, 200  

