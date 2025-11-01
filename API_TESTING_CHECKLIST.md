# EvolveEdu.AI - Complete API Testing Checklist

## 📋 How to Use This List
- ✅ = Ready to test
- 🔄 = Needs implementation/verification
- Each API includes example request/response

---

## 🔐 AUTHENTICATION APIs (7 APIs)
These are the foundation - test these FIRST

### 1. ✅ Register User
```
POST /api/auth/register/
Body: {
  "email": "testuser@example.com",
  "password": "TestPass123!",
  "username": "testuser",
  "first_name": "Test",
  "last_name": "User"
}
Expected: 201 Created with tokens
```

### 2. ✅ Login
```
POST /api/auth/login/
Body: {
  "email": "testuser@example.com",
  "password": "TestPass123!"
}
Expected: 200 OK with access + refresh tokens
```

### 3. ✅ Refresh Token
```
POST /api/auth/token/refresh/
Body: {
  "refresh": "<refresh_token>"
}
Expected: 200 OK with new access token
```

### 4. ✅ Get Profile
```
GET /api/auth/profile/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with user details
```

### 5. ✅ Update Profile
```
PUT /api/auth/profile/update/
Headers: Authorization: Bearer <access_token>
Body: {
  "first_name": "Updated",
  "bio": "New bio",
  "skills": ["Python", "JavaScript"]
}
Expected: 200 OK with updated user
```

### 6. ✅ Change Password
```
POST /api/auth/change-password/
Headers: Authorization: Bearer <access_token>
Body: {
  "old_password": "TestPass123!",
  "new_password": "NewPass456!"
}
Expected: 200 OK
```

### 7. ✅ Logout
```
POST /api/auth/logout/
Headers: Authorization: Bearer <access_token>
Body: {
  "refresh": "<refresh_token>"
}
Expected: 200 OK
```

### 8. ✅ Dashboard Stats
```
GET /api/auth/dashboard-stats/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with user statistics
```

---

## 📝 NOTES APIS (15 APIs)
For note management and AI-powered note generation

### Core Operations
#### 1. ✅ List Notes (with filters)
```
GET /api/notes/?category=1&tags=python&search=algorithms
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with paginated notes
```

#### 2. ✅ Get Note Detail
```
GET /api/notes/{id}/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with full note details
```

#### 3. ✅ Create Note (Manual)
```
POST /api/notes/
Headers: Authorization: Bearer <access_token>
Body: {
  "title": "My Note",
  "content": "Note content here",
  "category": 1,
  "is_public": false
}
Expected: 201 Created
```

#### 4. ✅ Update Note
```
PUT /api/notes/{id}/
Headers: Authorization: Bearer <access_token>
Body: {
  "title": "Updated Title",
  "tags": ["updated"]
}
Expected: 200 OK
```

#### 5. ✅ Delete Note
```
DELETE /api/notes/{id}/
Headers: Authorization: Bearer <access_token>
Expected: 204 No Content
```

### AI-Powered Note Generation
#### 6. 🔄 Generate Notes from YouTube
```
POST /api/notes/youtube/
Headers: Authorization: Bearer <access_token>
Body: {
  "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "title": "Optional Title",
  "category_id": 1,
  "tags": ["youtube"]
}
Expected: 201 Created with AI-generated summary, key points, questions
```

#### 7. 🔄 Generate Notes from Text
```
POST /api/notes/text/
Headers: Authorization: Bearer <access_token>
Body: {
  "text": "Large text content here...",
  "title": "Text Notes",
  "category_id": 1
}
Expected: 201 Created with analyzed content
```

#### 8. 🔄 Generate Notes from PDF
```
POST /api/notes/pdf/
Headers: Authorization: Bearer <access_token>
Body (multipart/form-data): {
  "file": <PDF file>,
  "title": "PDF Notes"
}
Expected: 201 Created with extracted and summarized content
```

### Note Features
#### 9. ✅ Like/Unlike Note
```
POST /api/notes/{id}/like/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with like status and count
```

#### 10. ✅ Share Note
```
POST /api/notes/{id}/share/
Headers: Authorization: Bearer <access_token>
Body: {
  "shared_with": 2,
  "message": "Check this out!"
}
Expected: 201 Created share record
```

#### 11. ✅ Get Shared Notes
```
GET /api/notes/shared/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with notes shared with user
```

#### 12. 🔄 Enhance Note (AI)
```
POST /api/notes/{id}/enhance/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with enhanced summary, key points, tips
```

### Categories
#### 13. ✅ List Note Categories
```
GET /api/notes/categories/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with all categories
```

#### 14. ✅ Create Note Category (Admin)
```
POST /api/notes/categories/
Headers: Authorization: Bearer <access_token>
Body: {
  "name": "Web Development",
  "description": "Web dev notes",
  "icon": "🌐"
}
Expected: 201 Created
```

#### 15. ✅ Study Sessions
```
GET/POST /api/notes/study-sessions/
Headers: Authorization: Bearer <access_token>
Expected: 200/201 with study session data
```

---

## 🧪 QUIZ APIS (20+ APIs)
For quiz management and adaptive learning

### Core Operations
#### 1. ✅ List Quizzes (with filters)
```
GET /api/quizzes/?difficulty=Medium&search=python
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with paginated quizzes
```

#### 2. ✅ Get Quiz Detail
```
GET /api/quizzes/{id}/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with quiz and questions
```

#### 3. ✅ Create Custom Quiz
```
POST /api/quizzes/
Headers: Authorization: Bearer <access_token>
Body: {
  "title": "Custom Quiz",
  "description": "Test your knowledge",
  "category_id": 1,
  "difficulty_level": "Medium"
}
Expected: 201 Created
```

#### 4. ✅ Update Quiz
```
PUT /api/quizzes/{id}/
Headers: Authorization: Bearer <access_token>
Body: { "title": "Updated Quiz" }
Expected: 200 OK
```

#### 5. ✅ Delete Quiz
```
DELETE /api/quizzes/{id}/
Headers: Authorization: Bearer <access_token>
Expected: 204 No Content
```

### Question Management
#### 6. ✅ Add Question to Quiz
```
POST /api/quizzes/{quiz_id}/questions/
Headers: Authorization: Bearer <access_token>
Body: {
  "question": "What is Python?",
  "question_type": "multiple_choice",
  "options": ["Language", "Snake", "Tool"],
  "correct_answer_index": 0,
  "points": 10
}
Expected: 201 Created
```

#### 7. ✅ Update Question
```
PUT /api/quizzes/questions/{id}/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK
```

#### 8. ✅ Delete Question
```
DELETE /api/quizzes/questions/{id}/
Headers: Authorization: Bearer <access_token>
Expected: 204 No Content
```

### AI-Powered Quiz Generation
#### 9. 🔄 Generate Quiz from Notes
```
POST /api/quizzes/generate/
Headers: Authorization: Bearer <access_token>
Body: {
  "notes_ids": [1, 2, 3],
  "num_questions": 10,
  "difficulty": "Medium"
}
Expected: 201 Created with auto-generated questions
```

#### 10. 🔄 Generate Quiz from Text
```
POST /api/quizzes/generate-from-text/
Headers: Authorization: Bearer <access_token>
Body: {
  "text": "Content to generate quiz from",
  "num_questions": 5,
  "difficulty": "Easy"
}
Expected: 201 Created with questions
```

### Quiz Attempts
#### 11. ✅ Start Quiz Attempt
```
POST /api/quizzes/{id}/attempt/
Headers: Authorization: Bearer <access_token>
Expected: 201 Created attempt record
```

#### 12. ✅ Submit Answer to Question
```
POST /api/quizzes/attempts/{attempt_id}/responses/
Headers: Authorization: Bearer <access_token>
Body: {
  "question_id": 1,
  "answer_index": 2
}
Expected: 201 Created response
```

#### 13. ✅ Complete Quiz Attempt
```
POST /api/quizzes/attempts/{attempt_id}/complete/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with scoring and feedback
```

#### 14. ✅ Get Quiz Attempt History
```
GET /api/quizzes/attempts/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with all user attempts
```

### Analytics & Recommendations
#### 15. 🔄 Get Quiz Analytics
```
GET /api/quizzes/{id}/analytics/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with performance metrics
```

#### 16. 🔄 Get Quiz Recommendations
```
GET /api/quizzes/recommendations/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with recommended quizzes
```

#### 17. 🔄 Get Study Plan
```
GET /api/quizzes/study-plan/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with personalized study plan
```

### Categories
#### 18. ✅ List Quiz Categories
```
GET /api/quizzes/categories/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK
```

---

## 🛣️ ROADMAP APIS (12 APIs)
For learning paths and progress tracking

### Core Operations
#### 1. ✅ List Roadmaps
```
GET /api/roadmaps/?difficulty=Intermediate
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with available roadmaps
```

#### 2. ✅ Get Roadmap Detail
```
GET /api/roadmaps/{id}/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with modules and lessons
```

#### 3. ✅ Create Roadmap (Admin)
```
POST /api/roadmaps/
Headers: Authorization: Bearer <access_token>
Body: {
  "title": "Full Stack Developer",
  "description": "6-month path",
  "difficulty": "Intermediate"
}
Expected: 201 Created
```

### Module Management
#### 4. ✅ Add Module to Roadmap
```
POST /api/roadmaps/{id}/modules/
Headers: Authorization: Bearer <access_token>
Body: {
  "title": "HTML & CSS",
  "description": "Web fundamentals",
  "order": 1
}
Expected: 201 Created
```

#### 5. ✅ Add Lesson to Module
```
POST /api/roadmaps/modules/{module_id}/lessons/
Headers: Authorization: Bearer <access_token>
Body: {
  "title": "HTML Basics",
  "description": "Learn HTML structure"
}
Expected: 201 Created
```

### Progress Tracking
#### 6. ✅ Get Roadmap Progress
```
GET /api/roadmaps/{id}/progress/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with completion percentage
```

#### 7. ✅ Mark Module Complete
```
POST /api/roadmaps/{id}/complete-module/
Headers: Authorization: Bearer <access_token>
Body: { "module_id": 1 }
Expected: 200 OK
```

#### 8. ✅ Mark Lesson Complete
```
POST /api/roadmaps/modules/{module_id}/complete-lesson/
Headers: Authorization: Bearer <access_token>
Body: { "lesson_id": 1 }
Expected: 200 OK
```

### Recommendations
#### 9. 🔄 Get Recommended Roadmaps
```
GET /api/roadmaps/recommended/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with personalized suggestions
```

#### 10. ✅ Enroll in Roadmap
```
POST /api/roadmaps/{id}/enroll/
Headers: Authorization: Bearer <access_token>
Expected: 201 Created enrollment
```

#### 11. ✅ Unenroll from Roadmap
```
POST /api/roadmaps/{id}/unenroll/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK
```

#### 12. 🔄 Get Learning Stats
```
GET /api/roadmaps/stats/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with overall learning statistics
```

---

## 💬 TUTOR (Q&A) APIS (8 APIs)
For AI-powered tutoring

### Questions & Answers
#### 1. 🔄 Ask Question
```
POST /api/tutor/ask/
Headers: Authorization: Bearer <access_token>
Body: {
  "question": "What is REST API?",
  "topic": "Web Services",
  "context": "Optional context"
}
Expected: 200 OK with AI response
```

#### 2. ✅ Get Conversation History
```
GET /api/tutor/history/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with past Q&A
```

#### 3. ✅ Delete Conversation
```
DELETE /api/tutor/history/{id}/
Headers: Authorization: Bearer <access_token>
Expected: 204 No Content
```

### Concept Explanation
#### 4. 🔄 Explain Concept
```
POST /api/tutor/explain/
Headers: Authorization: Bearer <access_token>
Body: {
  "topic": "Machine Learning",
  "difficulty_level": "Intermediate"
}
Expected: 200 OK with detailed explanation
```

#### 5. 🔄 Get Practice Questions
```
GET /api/tutor/practice-questions/?topic=Python
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with practice questions
```

### Feedback & Analytics
#### 6. 🔄 Get Answer Feedback
```
POST /api/tutor/feedback/
Headers: Authorization: Bearer <access_token>
Body: {
  "question": "What is OOP?",
  "student_answer": "Object Oriented Programming...",
  "correct_answer": "Full definition..."
}
Expected: 200 OK with feedback
```

#### 7. 🔄 Rate Response
```
POST /api/tutor/history/{id}/rate/
Headers: Authorization: Bearer <access_token>
Body: { "rating": 5 }
Expected: 200 OK
```

#### 8. 🔄 Get Adaptive Question
```
GET /api/tutor/adaptive-question/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with next recommended question
```

---

## 📊 ADDITIONAL APIS (5 APIs)

#### 1. ✅ User List (for sharing)
```
GET /api/users/?search=john
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with user list
```

#### 2. ✅ Get User Profile (by ID)
```
GET /api/users/{id}/profile/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with public user info
```

#### 3. ✅ Get Achievements
```
GET /api/achievements/
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with earned achievements
```

#### 4. ✅ Get Leaderboard
```
GET /api/leaderboard/?period=monthly
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with top users
```

#### 5. ✅ Search (Global)
```
GET /api/search/?q=python
Headers: Authorization: Bearer <access_token>
Expected: 200 OK with results across all content
```

---

## 📈 SUMMARY BY PRIORITY

### Priority 1 - CRITICAL (Must Have)
**15 APIs** - Test these FIRST
- All 8 Auth APIs
- List/Detail/Create/Update/Delete for Notes
- List/Detail/Create Quiz
- Quiz Attempt/Submit/Complete
- Roadmap List/Detail

### Priority 2 - HIGH (Important)
**20 APIs** - Test after Priority 1
- Generate Notes from YouTube/Text
- Generate Quiz from Notes
- Quiz Analytics
- Roadmap Progress/Complete Module
- All Tutor APIs
- Study Plans

### Priority 3 - MEDIUM (Nice to Have)
**10 APIs** - Test for complete experience
- Note Enhancement
- Quiz Recommendations
- Roadmap Recommendations
- Leaderboard
- Achievements

### Priority 4 - LOW (Extra)
**5 APIs** - Polish features
- Advanced search
- User profiles
- Social features
- Analytics
- Admin operations

---

## 🧪 Testing Tools Recommendation

### Use Postman or Insomnia to test APIs:
1. **Create Environment**:
   - `base_url`: http://localhost:8000/api
   - `access_token`: From login response
   - `refresh_token`: From login response

2. **Test Flow**:
   - Start with Register + Login
   - Get access_token
   - Use token for all subsequent requests
   - Test each endpoint with the token

3. **Example Postman Collection Variables**:
   ```json
   {
     "base_url": "{{baseUrl}}/api",
     "email": "test@example.com",
     "password": "TestPass123!",
     "access_token": "{{access_token}}",
     "note_id": 1,
     "quiz_id": 1,
     "attempt_id": 1
   }
   ```

---

## Total API Count: **75+ Endpoints**
- ✅ Ready: ~50 endpoints
- 🔄 Needs AI implementation: ~25 endpoints

**You should provide all 75+ endpoints** once:
1. Backend is running (python manage.py runserver)
2. Frontend successfully connects and authenticates
3. All models are migrated
4. .env file is properly configured

