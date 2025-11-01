# EvolveEdu.AI - Setup & Running Guide

Complete guide to set up and run the EvolveEdu.AI project locally and in production.

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+ (for production)
- Git
- pip (Python package manager)
- npm (Node package manager)

## 🚀 Quick Start (Development)

### 1. Backend Setup

```bash
# Clone the repository
git clone https://github.com/jayanth0075/EvolveEdu.AI.git
cd EvolveEdu.AI

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r evolveedu-ai/backend/requirements-dev.txt

# Create .env file
cp .env.example .env

# Navigate to backend
cd evolveedu-ai/backend

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Run development server
python manage.py runserver 0.0.0.0:8000
```

### 2. Frontend Setup

```bash
# In a new terminal, navigate to frontend
cd evolveedu-ai/frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOF
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_DEBUG=true
EOF

# Start development server
npm start
```

### 3. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api
- **Admin Panel:** http://localhost:8000/admin (use superuser credentials)

---

## 🐳 Docker Setup (Production-like)

```bash
# Build and start containers
docker-compose up -d

# Run migrations in Docker
docker-compose exec backend python manage.py migrate

# Create superuser in Docker
docker-compose exec backend python manage.py createsuperuser

# Access the app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Admin: http://localhost:8000/admin
```

---

## 📝 Environment Variables

Copy `.env.example` to `.env` and update:

```env
DEBUG=True                          # Set to False in production
SECRET_KEY=your-secret-key         # Generate new in production
DATABASE_URL=postgresql://...      # PostgreSQL connection string
HUGGINGFACE_API_KEY=your-key       # For AI features
CORS_ALLOWED_ORIGINS=...           # Frontend URL
```

---

## 🗄️ Database

### SQLite (Development - Default)
- Automatically created as `db.sqlite3`
- No setup required

### PostgreSQL (Production)
```bash
# Create database
createdb evolveedu

# Set DATABASE_URL in .env
DATABASE_URL=postgresql://username:password@localhost:5432/evolveedu

# Run migrations
python manage.py migrate
```

---

## 📚 API Documentation

### Authentication
```bash
# Register
POST /api/accounts/register/
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}

# Login
POST /api/accounts/login/
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Using Access Token
```bash
Header: Authorization: Bearer <access_token>
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test module
pytest evolveedu-ai/backend/accounts/tests.py

# With coverage report
pytest --cov=.
```

---

## 🔧 Common Issues & Solutions

### Issue: ModuleNotFoundError: No module named 'evolveedu'
**Solution:** Make sure you're in the `backend` directory when running migrations/server

### Issue: PostgreSQL connection refused
**Solution:** Ensure PostgreSQL is running and DATABASE_URL is correct

### Issue: Port 8000 already in use
**Solution:** `python manage.py runserver 8000` use different port or kill the process

### Issue: Frontend can't connect to backend
**Solution:** Check CORS_ALLOWED_ORIGINS in settings.py and .env

---

## 📦 Project Structure

```
EvolveEdu.AI/
├── evolveedu-ai/
│   ├── backend/              # Django REST API
│   │   ├── evolveedu/        # Project settings
│   │   ├── accounts/         # User management
│   │   ├── notes/            # Notes functionality
│   │   ├── quizzes/          # Quiz system
│   │   ├── roadmaps/         # Learning roadmaps
│   │   └── tutor/            # AI tutor
│   └── frontend/             # React application
│       └── src/
│           ├── pages/        # Page components
│           ├── components/   # Reusable components
│           └── api/          # API client
├── docker-compose.yml        # Docker configuration
├── Dockerfile               # Docker build instructions
├── requirements.txt         # Python dependencies
└── .env.example            # Environment variables template
```

---

## 🚢 Deployment

### Using Docker on Heroku/Railway/DigitalOcean:

```bash
# Push to Docker registry
docker build -t your-registry/evolveedu-ai .
docker push your-registry/evolveedu-ai

# Deploy using docker-compose
docker-compose -f docker-compose.yml up -d
```

### Using Traditional Server:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn evolveedu.wsgi:application --bind 0.0.0.0:8000
```

---

## 📞 Support & Contributing

- Report issues on GitHub Issues
- See CONTRIBUTING.md for contribution guidelines
- Check CHANGELOG.md for version history

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Happy Learning! 🎓**
