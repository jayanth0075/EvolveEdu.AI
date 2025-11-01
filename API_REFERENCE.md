# EvolveEdu.AI - Complete API Reference

## Base URL
```
http://localhost:8000/api
```

## Authentication
All endpoints (except register/login) require JWT token in header:
```
Authorization: Bearer <access_token>
```

---

## 1. Authentication APIs

### Register User
```
POST /auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe"
}

Response (201):
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Login
```
POST /auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}

Response (200):
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Logout
```
POST /auth/logout/
Authorization: Bearer <access_token>

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response (200):
{
  "message": "Logout successful"
}
```

### Refresh Token
```
POST /auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response (200):
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Get Profile
```
GET /auth/profile/
Authorization: Bearer <access_token>

Response (200):
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "phone": "+1234567890",
  "bio": "Passionate learner",
  "current_education": "College",
  "current_job": "Student",
  "skills": ["Python", "JavaScript"],
  "interests": ["AI", "Web Development"],
  "total_quizzes_taken": 5,
  "total_notes_generated": 10,
  "current_level": "Intermediate"
}
```

### Update Profile
```
PUT/PATCH /auth/profile/update/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "John",
  "bio": "Updated bio",
  "skills": ["Python", "JavaScript", "React"],
  "interests": ["AI", "Machine Learning"]
}

Response (200): Updated user object
```

### Change Password
```
POST /auth/change-password/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "old_secure_password",
  "new_password": "new_secure_password"
}

Response (200):
{
  "message": "Password updated successfully"
}
```

### Dashboard Stats
```
GET /auth/dashboard-stats/
Authorization: Bearer <access_token>

Response (200):
{
  "total_quizzes_taken": 15,
  "total_notes_generated": 30,
  "current_level": "Advanced",
  "study_time_minutes": 450,
  "streak_days": 7,
  "completed_roadmaps": 3,
  "current_roadmaps": 2,
  "achievements": ["First Note", "Quiz Master", "7-Day Streak"]
}
```

---

## 2. Notes APIs

### List Notes
```
GET /notes/?category=1&tags=python&search=algorithms&source_type=youtube
Authorization: Bearer <access_token>

Query Parameters:
  - category: Filter by category ID
  - tags: Comma-separated tags
  - search: Search in title/content
  - source_type: youtube, pdf, text, lecture, url

Response (200):
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Python Algorithms",
      "content": "...",
      "summary": "...",
      "source_type": "youtube",
      "source_url": "https://youtube.com/watch?v=...",
      "category": 1,
      "tags": ["python", "algorithms"],
      "key_points": ["Point 1", "Point 2"],
      "questions": ["Q1", "Q2"],
      "difficulty_level": "Medium",
      "estimated_read_time": 15,
      "is_public": false,
      "views": 42,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Get Note Detail
```
GET /notes/{id}/
Authorization: Bearer <access_token>

Response (200): Single note object (same structure as above)
```

### Generate Notes from YouTube
```
POST /notes/youtube/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "title": "Learn Python in 10 Minutes",
  "category_id": 1,
  "tags": ["python", "beginners"],
  "is_public": false
}

Response (201): Generated note object with AI-enhanced content
```

### Generate Notes from Text
```
POST /notes/text/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "text": "The study of algorithms...",
  "title": "Algorithms Overview",
  "category_id": 1,
  "tags": ["algorithms", "cs"],
  "is_public": false
}

Response (201): Generated note object
```

### Generate Notes from PDF
```
POST /notes/pdf/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

file: <PDF file>
title: "Lecture Notes"
category_id: 1
tags: ["lectures"]
is_public: false

Response (201): Generated note object
```

### Update Note
```
PUT/PATCH /notes/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "tags": ["updated", "tags"],
  "is_public": true
}

Response (200): Updated note object
```

### Delete Note
```
DELETE /notes/{id}/
Authorization: Bearer <access_token>

Response (204): No content
```

### Like Note
```
POST /notes/{id}/like/
Authorization: Bearer <access_token>

Response (200):
{
  "liked": true,
  "likes_count": 10
}
```

### Share Note
```
POST /notes/{id}/share/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "shared_with": 2,
  "message": "Check out these notes!"
}

Response (201):
{
  "id": 1,
  "note": 1,
  "shared_by": 1,
  "shared_with": 2,
  "message": "Check out these notes!",
  "created_at": "2024-01-15T10:30:00Z",
  "is_read": false
}
```

### Get Shared Notes
```
GET /notes/shared/
Authorization: Bearer <access_token>

Response (200): Array of note share objects
```

### Enhance Note
```
POST /notes/{id}/enhance/
Authorization: Bearer <access_token>

Response (200):
{
  "enhanced_summary": "...",
  "key_points": ["Point 1", "Point 2"],
  "practice_questions": ["Q1", "Q2"],
  "complex_concepts": ["Concept 1"],
  "study_tips": ["Tip 1", "Tip 2"]
}
```

### Note Categories
```
GET /notes/categories/
Authorization: Bearer <access_token>

Response (200):
{
  "results": [
    {
      "id": 1,
      "name": "Programming",
      "description": "Programming related notes",
      "icon": "💻"
    }
  ]
}
```

---

## 3. Quiz APIs

### List Quizzes
```
GET /quizzes/?category=1&difficulty=Medium&type=adaptive&search=python
Authorization: Bearer <access_token>

Query Parameters:
  - category: Filter by category ID
  - difficulty: Easy, Medium, Hard
  - type: adaptive, practice, test
  - search: Search in title/description

Response (200):
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "title": "Python Basics",
      "description": "Test your Python knowledge",
      "category": 1,
      "created_by": 1,
      "difficulty_level": "Medium",
      "quiz_type": "practice",
      "total_questions": 10,
      "duration_minutes": 15,
      "is_public": true,
      "attempts": 5,
      "average_score": 78.5,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Get Quiz Detail
```
GET /quizzes/{id}/
Authorization: Bearer <access_token>

Response (200):
{
  ...quiz object...,
  "questions": [
    {
      "id": 1,
      "question": "What is Python?",
      "question_type": "multiple_choice",
      "options": ["Language", "Snake", "Tool", "None"],
      "difficulty_level": "Easy",
      "points": 10
    }
  ]
}
```

### Generate Quiz from Notes
```
POST /quizzes/generate/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "notes_ids": [1, 2, 3],
  "num_questions": 10,
  "difficulty": "Medium",
  "title": "Python Quiz"
}

Response (201): Generated quiz object with questions
```

### Create Custom Quiz
```
POST /quizzes/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "My Quiz",
  "description": "Test quiz",
  "category_id": 1,
  "difficulty_level": "Medium",
  "quiz_type": "practice",
  "is_public": false,
  "duration_minutes": 30
}

Response (201): Created quiz object
```

### Start Quiz Attempt
```
POST /quizzes/{id}/attempt/
Authorization: Bearer <access_token>

Response (201):
{
  "id": 1,
  "quiz": 1,
  "user": 1,
  "started_at": "2024-01-15T10:30:00Z",
  "status": "in_progress"
}
```

### Submit Quiz Response
```
POST /quizzes/attempts/{attempt_id}/submit/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "question_id": 1,
  "answer_index": 2
}

Response (200): Updated attempt object
```

### Complete Quiz Attempt
```
POST /quizzes/attempts/{attempt_id}/complete/
Authorization: Bearer <access_token>

Response (200):
{
  "score": 78,
  "total_points": 100,
  "percentage": 78.0,
  "correct_answers": 8,
  "total_questions": 10,
  "performance_level": "Good",
  "feedback": [
    {
      "question_number": 1,
      "correct": true,
      "feedback": "Great job!"
    }
  ]
}
```

### Get Quiz Recommendations
```
GET /quizzes/recommendations/
Authorization: Bearer <access_token>

Response (200):
{
  "results": [recommended quizzes],
  "reason": "Based on your performance in weak areas"
}
```

### Get Quiz Analytics
```
GET /quizzes/{id}/analytics/
Authorization: Bearer <access_token>

Response (200):
{
  "total_attempts": 10,
  "average_score": 75.5,
  "average_percentage": 75.5,
  "highest_score": 95,
  "lowest_score": 45,
  "trend": "Improving",
  "weak_areas": ["Concepts", "Application"],
  "recommendation": "Keep practicing!"
}
```

---

## 4. Roadmap APIs

### List Roadmaps
```
GET /roadmaps/?category=web-development
Authorization: Bearer <access_token>

Response (200):
{
  "results": [
    {
      "id": 1,
      "title": "Full Stack Developer",
      "description": "6-month path to become a full stack developer",
      "difficulty": "Intermediate",
      "duration_weeks": 24,
      "modules_count": 5,
      "progress": 40,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Get Roadmap Detail
```
GET /roadmaps/{id}/
Authorization: Bearer <access_token>

Response (200):
{
  ...roadmap object...,
  "modules": [
    {
      "id": 1,
      "title": "HTML & CSS",
      "duration_weeks": 4,
      "lessons_count": 12,
      "progress": 100,
      "completed": true,
      "lessons": [
        {
          "id": 1,
          "title": "HTML Basics",
          "completed": true
        }
      ]
    }
  ]
}
```

### Get Recommended Roadmaps
```
GET /roadmaps/recommended/
Authorization: Bearer <access_token>

Response (200):
{
  "results": [recommended roadmaps],
  "reason": "Based on your interests and learning history"
}
```

### Get Roadmap Progress
```
GET /roadmaps/{id}/progress/
Authorization: Bearer <access_token>

Response (200):
{
  "overall_progress": 40,
  "completed_modules": 2,
  "total_modules": 5,
  "estimated_completion": "2024-06-15",
  "learning_streak": 7,
  "time_invested_hours": 45
}
```

### Mark Module Complete
```
POST /roadmaps/{id}/complete-module/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "module_id": 1
}

Response (200):
{
  "message": "Module marked as complete",
  "progress": 45
}
```

---

## 5. Tutor (Q&A) APIs

### Ask Question
```
POST /tutor/ask/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "question": "What is the difference between REST and GraphQL?",
  "topic": "API Design",
  "context": "Optional context about the topic"
}

Response (200):
{
  "question": "What is the difference between REST and GraphQL?",
  "answer": "REST and GraphQL are two different approaches to building APIs...",
  "question_type": "comparison",
  "confidence": 0.85,
  "follow_up_questions": [
    "When should I use REST vs GraphQL?",
    "What are the performance implications?",
    "How do they compare in terms of complexity?"
  ],
  "related_concepts": [
    "API Design",
    "Web Services",
    "Data Fetching"
  ],
  "sources": ["API Design"]
}
```

### Get Conversation History
```
GET /tutor/history/
Authorization: Bearer <access_token>

Response (200):
{
  "results": [
    {
      "id": 1,
      "question": "...",
      "answer": "...",
      "created_at": "2024-01-15T10:30:00Z",
      "rating": 5
    }
  ]
}
```

### Explain Concept
```
POST /tutor/explain/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "topic": "Machine Learning",
  "difficulty_level": "Intermediate"
}

Response (200):
{
  "topic": "Machine Learning",
  "difficulty_level": "Intermediate",
  "explanation": "Machine Learning is a subset of artificial intelligence...",
  "key_points": [
    "Point 1",
    "Point 2",
    "Point 3"
  ],
  "learning_resources": [
    "Tutorial videos",
    "Research papers"
  ],
  "prerequisite_knowledge": [
    "Statistics",
    "Probability"
  ]
}
```

### Get Feedback on Answer
```
POST /tutor/feedback/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "question": "What is OOP?",
  "student_answer": "Object Oriented Programming is about objects",
  "correct_answer": "Object Oriented Programming is a programming paradigm based on objects..."
}

Response (200):
{
  "is_correct": true,
  "feedback": "Your answer is correct!",
  "explanation": "OOP is indeed...",
  "learning_suggestions": [
    "Great understanding!"
  ],
  "confidence_score": 0.9
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request",
  "details": "Field validation error"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required",
  "detail": "Invalid or missing token"
}
```

### 403 Forbidden
```json
{
  "error": "Permission denied",
  "detail": "You don't have permission to access this resource"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found",
  "detail": "The requested resource does not exist"
}
```

### 500 Server Error
```json
{
  "error": "Internal server error",
  "detail": "An unexpected error occurred"
}
```

---

## Rate Limiting
- Default: 100 requests per hour per user
- Auth endpoints: 10 requests per hour (per IP)
- Premium users: 1000 requests per hour

---

## Webhook Events (Coming Soon)
- `quiz.completed`: Triggered when user completes a quiz
- `note.created`: Triggered when user creates a note
- `roadmap.module.completed`: Triggered when user completes a module
- `achievement.unlocked`: Triggered when user unlocks an achievement

---

## Pagination
All list endpoints support pagination:
```
GET /api/notes/?page=2&page_size=20

Response:
{
  "count": 150,
  "next": "http://localhost:8000/api/notes/?page=3",
  "previous": "http://localhost:8000/api/notes/?page=1",
  "results": [...]
}
```

---

## Filtering & Search
Most endpoints support filtering and searching via query parameters:
```
GET /api/quizzes/?difficulty=Medium&search=python&ordering=-created_at

Supported filters:
- search: Full-text search
- ordering: Sort by field (prefix with - for descending)
- category: Filter by category
- difficulty: Filter by difficulty level
- created_by: Filter by creator
```

