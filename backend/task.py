import os
import csv
from celery import shared_task
from flask import current_app 
from models import db, User, Score, Quiz, Question
from utils import format_report
from mails import send_email
from datetime import datetime
import requests

EXPORT_FOLDER = 'exports'  

@shared_task(ignore_results=False, name="download_csv_report")
def csv_report():
    from flask import current_app
    import os
    import csv
    from datetime import datetime
    from models import db, User

    with current_app.app_context():
        export_dir = os.path.join(current_app.root_path, 'static', 'exports')
        os.makedirs(export_dir, exist_ok=True)
        filename = f"users_export_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"
        filepath = os.path.join(export_dir, filename)

        users = User.query.filter_by(role='user').all()
        with open(filepath, "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "id", "username", "email", "full_name", "qualification", "dob", "role"
            ])
            for user in users:
                writer.writerow([
                    user.id,
                    user.username,
                    user.email,
                    user.full_name or "",
                    user.qualification or "",
                    user.dob.strftime('%Y-%m-%d') if user.dob else "",
                    user.role
                ])
        return filename  
@shared_task(ignore_results=False, name="monthly_user_report")
def monthly_user_report():
    
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    users = User.query.filter_by(role='user').all()
    for user in users:
        user_data = {}
        user_data['name'] = user.full_name or user.username
        user_data['email'] = user.email

        
        scores = (
            Score.query
            .filter_by(user_id=user.id)
            .filter(db.extract('month', Score.time_stamp_of_attempt) == current_month)
            .filter(db.extract('year', Score.time_stamp_of_attempt) == current_year)
            .all()
        )

        total_quizzes = len(scores)
        total_score = sum(s.total_scored for s in scores if s.total_scored is not None)

        quiz_details = []
        for score in scores:
            quiz = score.quiz
            quiz_details.append({
                "quiz_name": quiz.name,
                "subject_name": quiz.chapter.subject.name,
                "chapter_name": quiz.chapter.name,
                "score": score.total_scored,
                "reattempted": "Yes" if score.reattempted else "No",
                "date_attempted": score.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M")
            })

        user_data['statistics'] = {
            "total_quizzes": total_quizzes,
            "total_score": total_score
        }
        user_data['quiz_details'] = quiz_details

       
        message = format_report('static/Mail.html', user_data)
        send_email(user.email, subject="Monthly Quiz Report", message=message)

    return "Monthly quiz reports sent to all users"

@shared_task(ignore_results=False, name="daily_user_reminders")
def daily_user_reminders():
    total_quizzes = Quiz.query.count()
    users = User.query.filter_by(role='user').all()

    reminder_count = 0

    for user in users:
        attempted_quizzes = Score.query.filter_by(user_id=user.id).count()

        if attempted_quizzes < total_quizzes:
            remaining = total_quizzes - attempted_quizzes

            text = (
                f"Hi {user.full_name or user.username}, "
                f"you have {remaining} quiz{'es' if remaining > 1 else ''} remaining. "
                "Visit your dashboard to complete it: http://172.19.93.117:8080/user-dashboard"
            )

            # Send via webhook 
            response = requests.post(
                "https://chat.googleapis.com/v1/spaces/AAQAEgJzp9U/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=yhwz2lRtyS9YqbNIrm5qNktUS6k9lH6uYqzRvFd-5es",
                json={"text": text}
            )

            print(f"Reminder sent to {user.username} with status: {response.status_code}")
            reminder_count += 1

    return f"Reminders sent to {reminder_count} users with pending quizzes."