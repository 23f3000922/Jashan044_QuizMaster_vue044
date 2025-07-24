# Quiz Master V2 - Modern Application Development II

A comprehensive quiz management system built with Flask (Backend) and Vue.js (Frontend).

## Features
- User Authentication & Role-Based Access Control
- Admin Dashboard for managing subjects, chapters, quizzes, and questions
- User Dashboard for attempting quizzes
- Real-time quiz timer and scoring
- Background jobs for reminders and reports
- Advanced analytics and performance tracking
- Redis caching for optimized performance

## Tech Stack
- **Backend**: Flask, SQLAlchemy, JWT, Celery, Redis
- **Frontend**: Vue.js, Chart.js, Bootstrap
- **Database**: SQLite
- **Task Queue**: Celery with Redis

## Project Structure
\\\
proj/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── subject.py
│   ├── authorization/
│   └── task.py
    └── utils.py
    └── celery_init.py
    └── mails.py
    └──Requirements.py

├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
└── README.md
\\\

## Installation & Setup
1. Clone the repository
2. Set up backend dependencies
3. Set up frontend dependencies
4. Configure Redis and Celery
5. Run the application

## Milestones Completed
- [x] Database Schema Design & Implementation
- [x] Token-Based Authentication & RBAC
- [x] Admin Dashboard Management
- [x] User Dashboard & Quiz Attempt System
- [x] Score Management and Quiz Result Display
- [x] Quiz Scheduling & Time Management
- [x] Backend Jobs - Daily Reminders & Monthly Reports
- [x] Search Functionality
- [x] Async CSV Export
- [x] API Performance Optimization & Caching
- [x] Advanced Quiz Analytics & Leaderboard

## Contributors
- Jashan Tiwari - Full Stack Developer
