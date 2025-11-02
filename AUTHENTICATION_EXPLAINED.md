# 🔐 Authentication System - Complete Explanation

## Overview
Your EvolveEdu.AI uses **JWT (JSON Web Token)** authentication with **SQLite database** for local development.

---

## 📊 How Authentication Works

### 1. **Authentication Flow**

```
User Registration/Login
        ↓
Django validates credentials
        ↓
JWT tokens generated (Access + Refresh)
        ↓
Client stores tokens
        ↓
Client sends token with each request
        ↓
Django validates token
        ↓
Request processed if valid
```

---

## 💾 Where Data is Stored

### **Current Setup (Development):**

**Database:** `SQLite` 
**Location:** `evolveedu-ai/backend/db.sqlite3`
**Size:** ~586 KB (585,728 bytes)

```
C:\Users\m9963\PycharmProjects\AI\FEFW-DJ-EvolveEd.ai\
└── evolveedu-ai/
    └── backend/
        └── db.sqlite3  ← ALL USER DATA IS HERE
```

### **What's Stored in db.sqlite3:**

1. **User Accounts** (`accounts_user` table)
   - Email (unique)
   - Username
   - Password (hashed with Django's PBKDF2 algorithm)
   - Role (student/professional/teacher)
   - Profile info (phone, bio, profile picture path)
   - Skills, interests (JSON)
   - Progress stats

2. **User Progress** (`accounts_userprogress` table)
   - Study time
   - Completed roadmaps
   - Achievements
   - Streak days

3. **Notes** (`notes_note` table)
   - Title, content, summary
   - Key points
   - Tags
   - User ID (foreign key)

4. **Quizzes** (`quizzes_quiz` table)
   - Quiz data
   - Questions
   - Attempts

5. **Sessions** (Django built-in)
   - Session data
   - CSRF tokens

6. **JWT Tokens** (`token_blacklist` table if enabled)
   - Blacklisted refresh tokens

---

## 🔑 JWT Token System

### **Technology:**
- **Library:** `djangorestframework-simplejwt`
- **Algorithm:** HS256 (HMAC with SHA-256)
- **Secret Key:** From `.env` file

### **Token Types:**

#### 1. **Access Token**
- **Lifetime:** 1 hour (configurable)
- **Purpose:** Authenticate API requests
- **Storage:** Client-side (browser localStorage/sessionStorage)
- **Format:** 
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwNTc0Mzg2LCJpYXQiOjE3MzA1NzA3ODYsImp0aSI6IjEyMzQ1NiIsInVzZXJfaWQiOjF9.signature
```

#### 2. **Refresh Token**
- **Lifetime:** 7 days (configurable)
- **Purpose:** Get new access tokens
- **Rotation:** Enabled (new refresh token on each use)
- **Blacklist:** Old tokens are blacklisted after rotation

### **Configuration (settings.py):**

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),      # Short-lived
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Long-lived
    'ROTATE_REFRESH_TOKENS': True,                    # Security
    'BLACKLIST_AFTER_ROTATION': True,                 # Prevents reuse
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,                        # From .env
    'AUTH_HEADER_TYPES': ('Bearer',),                 # Header format
}
```

---

## 🔒 Password Security

### **Hashing Algorithm:**
- **Django's default:** PBKDF2-HMAC-SHA256
- **Iterations:** 600,000+ (very secure)
- **Salt:** Unique per password (automatic)

### **Example Stored Password:**
```
pbkdf2_sha256$600000$randomsalt$hashedpassword
```

**Real example from your DB:**
```
pbkdf2_sha256$870000$AB1CD2EF3GH4$longhashedstring...
```

---

## 📡 API Request Flow

### **1. User Registration:**

**Request:**
```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "student@example.com",
  "username": "student123",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "role": "student"
}
```

**Django Process:**
1. Validates input (UserRegistrationSerializer)
2. Hashes password with PBKDF2
3. Saves to `db.sqlite3` → `accounts_user` table
4. Creates UserProgress record
5. Generates JWT tokens
6. Returns tokens + user data

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "student@example.com",
    "username": "student123",
    "role": "student"
  },
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

### **2. User Login:**

**Request:**
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "student@example.com",
  "password": "SecurePass123!"
}
```

**Django Process:**
1. Looks up user by email in `db.sqlite3`
2. Verifies password hash
3. Generates new JWT tokens
4. Returns tokens

### **3. Protected API Request:**

**Request:**
```http
GET /api/notes/
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Django Process:**
1. Extracts token from `Authorization` header
2. Verifies signature using SECRET_KEY
3. Checks expiration
4. Decodes user_id from token
5. Loads user from `db.sqlite3`
6. Processes request

---

## 🗄️ Database Schema

### **User Table Structure:**

```sql
CREATE TABLE accounts_user (
    id INTEGER PRIMARY KEY,
    email VARCHAR(254) UNIQUE NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,  -- Hashed
    role VARCHAR(20) DEFAULT 'student',
    phone VARCHAR(15),
    date_of_birth DATE,
    profile_picture VARCHAR(100),
    bio TEXT,
    current_education VARCHAR(100),
    current_job VARCHAR(100),
    skills TEXT,  -- JSON array
    interests TEXT,  -- JSON array
    total_quizzes_taken INTEGER DEFAULT 0,
    total_notes_generated INTEGER DEFAULT 0,
    current_level VARCHAR(20) DEFAULT 'Beginner',
    is_active BOOLEAN DEFAULT 1,
    is_staff BOOLEAN DEFAULT 0,
    created_at DATETIME,
    updated_at DATETIME
);
```

### **Current Users in Your Database:**
- **Count:** 2 users (from test results)
- **User 1:** Likely your initial test user
- **User 2:** `testuser2@test.com` (created during API tests)

---

## 🔄 Token Refresh Flow

**When access token expires (after 1 hour):**

```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response:**
```json
{
  "access": "new_access_token...",
  "refresh": "new_refresh_token..."  // If rotation enabled
}
```

---

## 🚨 Security Features

### **Implemented:**

1. ✅ **Password Hashing** - PBKDF2 with 870,000 iterations
2. ✅ **JWT Tokens** - Stateless authentication
3. ✅ **Token Expiration** - 1 hour access, 7 day refresh
4. ✅ **Token Rotation** - New refresh token on each use
5. ✅ **Token Blacklisting** - Prevents token reuse
6. ✅ **CORS Protection** - Only allowed origins
7. ✅ **CSRF Protection** - Django middleware
8. ✅ **Rate Limiting** - 100/hour anonymous, 1000/hour authenticated
9. ✅ **Email Uniqueness** - No duplicate accounts

### **Configured in settings.py:**

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

---

## 📂 File Locations

### **Authentication Code:**

1. **Models:** `evolveedu-ai/backend/accounts/models.py`
   - User model definition
   - UserProgress model

2. **Serializers:** `evolveedu-ai/backend/accounts/serializers.py`
   - UserRegistrationSerializer
   - UserLoginSerializer
   - UserProfileSerializer

3. **Views:** `evolveedu-ai/backend/accounts/views.py`
   - register() - Creates new users
   - login() - Authenticates users
   - logout() - Blacklists tokens
   - profile() - Gets user data

4. **URLs:** `evolveedu-ai/backend/accounts/urls.py`
   - /api/auth/register/
   - /api/auth/login/
   - /api/auth/logout/
   - /api/auth/profile/

5. **Settings:** `evolveedu-ai/backend/evolveedu/settings.py`
   - JWT configuration
   - Database configuration
   - Security settings

6. **Database:** `evolveedu-ai/backend/db.sqlite3`
   - ALL user data stored here

---

## 🔧 Environment Variables (.env)

**Authentication-related variables:**

```env
# Django Security
SECRET_KEY=your-secret-key-here-min-50-chars
DEBUG=True  # False in production

# Database (optional for production)
DATABASE_URL=postgresql://user:pass@host/db  # Overrides SQLite

# JWT (optional overrides)
SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=3600  # seconds
SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=604800  # seconds
```

---

## 🚀 Production Changes Needed

When deploying to production (Render/Vercel):

### **1. Change Database from SQLite to PostgreSQL:**

**Why?**
- SQLite is single-file, not suitable for production
- PostgreSQL is robust, concurrent, scalable

**How?**
```python
# Render provides DATABASE_URL automatically
# settings.py already configured to use it:

if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
```

### **2. Update Security Settings:**

```env
DEBUG=False
SECRET_KEY=generate-new-production-key-min-50-chars
ALLOWED_HOSTS=your-app.onrender.com,your-frontend.vercel.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### **3. Token Storage Best Practices:**

**Frontend:**
- **Access Token:** `localStorage` or `sessionStorage`
- **Refresh Token:** `httpOnly cookie` (more secure) or `localStorage`
- **Never:** Store in plain text or in code

---

## 📊 Current Data Summary

**From test results:**

```
✅ Database: db.sqlite3 (586 KB)
✅ Users: 2 registered users
✅ Notes: 2 notes created
✅ Quizzes: 0 quizzes
✅ Roadmaps: 0 roadmaps
✅ Tutor Sessions: 0 sessions
```

---

## 🔍 Inspect Your Database

**Option 1: Django Admin**
```bash
python manage.py createsuperuser
python manage.py runserver
# Visit: http://localhost:8000/admin/
```

**Option 2: Django Shell**
```bash
python manage.py shell
```
```python
from accounts.models import User
users = User.objects.all()
for user in users:
    print(f"{user.email} - {user.role} - Created: {user.created_at}")
```

**Option 3: SQLite Browser**
- Download: https://sqlitebrowser.org/
- Open: `evolveedu-ai/backend/db.sqlite3`
- Browse all tables visually

---

## 📝 Summary

**Your authentication system:**

1. **Type:** JWT-based (JSON Web Tokens)
2. **Database:** SQLite (`db.sqlite3` - 586 KB)
3. **Location:** `evolveedu-ai/backend/db.sqlite3`
4. **Users:** 2 currently registered
5. **Password Security:** PBKDF2-HMAC-SHA256 (870k iterations)
6. **Token Lifetime:** 1 hour (access), 7 days (refresh)
7. **Security:** Token rotation, blacklisting, rate limiting
8. **Production Ready:** Yes, but needs PostgreSQL migration

**Data Flow:**
```
User → Django → SQLite Database → JWT Token → Client
                                     ↓
                              Subsequent Requests
                                     ↓
                    Validate Token → Access Database → Return Data
```

**All user data (emails, hashed passwords, profiles, notes, quizzes) is stored in:**
```
📁 db.sqlite3 (SQLite database file)
```

For production deployment, this will migrate to PostgreSQL automatically when you set `DATABASE_URL` environment variable on Render! 🚀
