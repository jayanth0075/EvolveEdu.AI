# 🚀 Quick Start Guide - Backend Setup & Running

## Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend)
- PostgreSQL 13+ (for production, SQLite for dev)
- Virtual environment (venv or conda)

---

## Step 1: Backend Setup (5 minutes)

### 1.1 Install Python Dependencies
```bash
cd evolveedu-ai/backend
pip install -r requirements.txt
```

### 1.2 Create .env File
Create `evolveedu-ai/backend/.env`:
```env
# Django Settings
SECRET_KEY=your-secret-key-here-min-50-chars
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Development - SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# Database (Production - PostgreSQL)
# DATABASE_URL=postgresql://username:password@localhost:5432/evolveedu

# JWT Settings
SIMPLE_JWT_SECRET_KEY=your-jwt-secret-key-min-50-chars
SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=3600  # 1 hour in seconds
SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=604800  # 7 days

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# AI/ML Configuration (Optional - for AI features)
HF_API_KEY=your-huggingface-api-key
HF_MODEL_NOTES=facebook/bart-large-cnn
HF_MODEL_QA=deepset/roberta-base-squad2

# Email Configuration (Optional - for notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password

# File Upload Settings
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes

# Redis Settings (Optional - for caching)
REDIS_URL=redis://localhost:6379/0
```

### 1.3 Run Migrations
```bash
python manage.py migrate
```

### 1.4 Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Enter: email, password
```

### 1.5 Create Initial Data
```bash
python manage.py shell
```

Then paste in Python shell:
```python
from notes.models import NoteCategory

categories = [
    NoteCategory(name='Programming', description='Programming tutorials and notes', icon='💻'),
    NoteCategory(name='Mathematics', description='Math concepts and problems', icon='🧮'),
    NoteCategory(name='Science', description='Science lessons and experiments', icon='🔬'),
    NoteCategory(name='History', description='Historical events and facts', icon='📚'),
    NoteCategory(name='Languages', description='Language learning resources', icon='🌍'),
]

for cat in categories:
    cat.save()

print("Categories created successfully!")
exit()
```

---

## Step 2: Start Backend Server (1 minute)

### 2.1 Run Development Server
```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 2.2 Verify Backend is Running
```bash
# In another terminal
curl http://localhost:8000/api/auth/login/
```

You should get a response (not a connection error).

---

## Step 3: Test Backend with Postman/Insomnia

### 3.1 Register a User
```
POST http://localhost:8000/api/auth/register/

Body (JSON):
{
  "email": "testuser@example.com",
  "password": "TestPass123!",
  "username": "testuser",
  "first_name": "Test",
  "last_name": "User"
}
```

Expected Response (201):
```json
{
  "user": {
    "id": 1,
    "email": "testuser@example.com",
    "username": "testuser"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3.2 Save Access Token
Copy the `access` token value and use it for all subsequent API calls.

### 3.3 Get Dashboard Stats (Test Protected Endpoint)
```
GET http://localhost:8000/api/auth/dashboard-stats/

Headers:
Authorization: Bearer <paste_your_access_token_here>
```

Expected Response (200):
```json
{
  "total_quizzes_taken": 0,
  "total_notes_generated": 0,
  "current_level": "Beginner",
  "study_time_minutes": 0,
  "streak_days": 0,
  "completed_roadmaps": 0,
  "current_roadmaps": 0,
  "achievements": []
}
```

---

## Step 4: Setup Frontend (3 minutes)

### 4.1 Install Frontend Dependencies
```bash
cd evolveedu-ai/frontend
npm install
```

### 4.2 Create Frontend .env
Create `evolveedu-ai/frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENV=development
```

### 4.3 Start Frontend
```bash
npm start
```

Frontend should open at `http://localhost:3000`

---

## Step 5: Test Complete Flow

### 5.1 Register & Login
1. Go to `http://localhost:3000`
2. Click "Sign Up"
3. Enter email, password, name
4. Click "Create Account"
5. Should redirect to Dashboard after login

### 5.2 Test Features
- Create a note
- Generate note from text
- Create a quiz
- View dashboard stats

---

## 🐛 Troubleshooting

### Issue: "Port 8000 is already in use"
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
python manage.py runserver 8001
```

### Issue: "Module not found" errors
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: Database migrations failed
```bash
# Reset database (development only!)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: CORS error from frontend
Check `.env` file has correct `CORS_ALLOWED_ORIGINS`:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Issue: JWT token not recognized
1. Get a new token via login
2. Copy full token value (no extra spaces)
3. Use format: `Authorization: Bearer <token>`

### Issue: 404 on API endpoints
Ensure backend server is running:
```bash
# Terminal 1
python manage.py runserver

# Terminal 2
curl http://localhost:8000/api/auth/profile/  # Should give 401 (not found)
```

---

## 📚 API Endpoints Reference

### Authentication (Already working ✅)
- `POST /api/auth/register/` - Create account
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update profile
- `POST /api/auth/change-password/` - Change password
- `GET /api/auth/dashboard-stats/` - Get stats

### Notes (Mostly ready 🟡)
- `GET /api/notes/` - List notes
- `POST /api/notes/` - Create note
- `POST /api/notes/youtube/` - Generate from YouTube
- `POST /api/notes/text/` - Generate from text
- `POST /api/notes/pdf/` - Generate from PDF

### Quizzes (Mostly ready 🟡)
- `GET /api/quizzes/` - List quizzes
- `POST /api/quizzes/` - Create quiz
- `POST /api/quizzes/generate/` - Generate from notes
- `POST /api/quizzes/{id}/attempt/` - Start attempt
- `POST /api/quizzes/attempts/{id}/complete/` - Submit quiz

### Roadmaps (Ready ✅)
- `GET /api/roadmaps/` - List roadmaps
- `GET /api/roadmaps/{id}/` - Get roadmap detail
- `POST /api/roadmaps/{id}/complete-module/` - Mark module complete

### Tutor (Ready but AI needed 🟡)
- `POST /api/tutor/ask/` - Ask a question
- `GET /api/tutor/history/` - Get chat history
- `POST /api/tutor/explain/` - Explain concept

---

## 🎯 What's Next?

### After Backend is Running:
1. ✅ Test all Auth APIs
2. ✅ Test Note creation/listing
3. ✅ Test Quiz creation/taking
4. ✅ Test Roadmap browsing
5. 🔄 Test AI features (YouTube/Text note generation)
6. 🔄 Test Quiz generation from notes
7. 🔄 Test Tutor Q&A

### To Enable AI Features:
```bash
# Install AI/ML packages
pip install torch transformers youtube-transcript-api PyPDF2

# Get HuggingFace API key from https://huggingface.co/settings/tokens
# Add to .env: HF_API_KEY=your_token
```

---

## 📞 Commands Cheat Sheet

### Backend
```bash
# Start development server
python manage.py runserver

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django admin
# Visit: http://localhost:8000/admin

# Run tests
python manage.py test

# Open Python shell
python manage.py shell

# Create static files
python manage.py collectstatic
```

### Frontend
```bash
# Start dev server
npm start

# Build for production
npm run build

# Run tests
npm test

# Install dependencies
npm install
```

### Git
```bash
# Commit changes
git add -A
git commit -m "Your message"

# Push to GitHub
git push origin master

# Pull latest changes
git pull origin master
```

---

## ✨ You're All Set!

Your EvolveEdu.AI backend is now:
- ✅ Running on http://localhost:8000
- ✅ Serving 75+ API endpoints
- ✅ Ready to accept frontend connections
- ✅ Configured with JWT authentication
- ✅ Connected to database (SQLite)

**Next step:** Start testing APIs or connect frontend! 🚀

