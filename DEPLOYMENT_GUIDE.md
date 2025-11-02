# 🚀 EvolveEdu.AI - Deployment Guide

## ✅ Current Setup Status

**AI Provider:** Google Gemini (FREE)  
**API Key:** Configured ✅  
**Model:** gemini-2.5-flash  
**Backend:** Django REST Framework  
**Frontend:** React  

---

## 📋 Pre-Deployment Checklist

### 1. Environment Variables (.env)

Your `.env` file is configured for **LOCAL DEVELOPMENT**. For deployment, you need to set these as **Environment Variables** in your hosting platform.

**Required Environment Variables:**

```env
# Django Settings
SECRET_KEY=your-secret-key-here-min-50-chars-change-in-production
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-app.vercel.app

# Database (Use PostgreSQL for production)
DATABASE_URL=postgresql://user:password@host:port/dbname

# JWT Authentication
SIMPLE_JWT_SECRET_KEY=your-jwt-secret-key-min-50-chars-change-in-production
SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=3600
SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=604800

# CORS (Add your frontend domains)
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

# AI Provider (PRIMARY)
AI_PROVIDER=google
GOOGLE_API_KEY=AIzaSyBPNkNDYKJ3Nz1UEt05eesIblJyXiho-QE
GOOGLE_MODEL=gemini-2.5-flash

# AI Provider (Fallback - Optional)
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

---

## 🔧 Deployment Options

### Option 1: Render.com (RECOMMENDED for Backend)

**Why Render?**
- ✅ FREE tier available
- ✅ PostgreSQL database included
- ✅ Easy Django deployment
- ✅ Automatic HTTPS

**Steps:**

1. **Create account:** https://render.com/

2. **Create PostgreSQL Database:**
   - New → PostgreSQL
   - Name: `evolveedu-db`
   - Plan: Free
   - Copy the "Internal Database URL"

3. **Create Web Service:**
   - New → Web Service
   - Connect your GitHub repo
   - Name: `evolveedu-api`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd evolveedu-ai/backend && gunicorn evolveedu.wsgi:application`

4. **Add Environment Variables:**
   Go to Environment tab and add all variables from above
   - Use the DATABASE_URL from step 2
   - Set DEBUG=False
   - Set ALLOWED_HOSTS=your-app.onrender.com

5. **Deploy!**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deployment

---

### Option 2: Vercel (For Frontend ONLY)

**Note:** Vercel is best for React frontend, not Django backend.

**Steps:**

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy Frontend:**
   ```bash
   cd evolveedu-ai/frontend
   vercel
   ```

3. **Configure:**
   - Add environment variable: `REACT_APP_API_URL=https://your-render-backend.onrender.com`

---

### Option 3: Railway.app (Alternative to Render)

1. **Create account:** https://railway.app/
2. **New Project → Deploy from GitHub**
3. **Add PostgreSQL database**
4. **Configure environment variables**
5. **Deploy**

---

## 🧪 Test Before Deployment

Run this script to verify everything works:

```bash
cd evolveedu-ai/backend
python test_deployment.py
```

---

## 📝 Deployment Configuration Files

### For Render.com:

Create `render.yaml` in root:

```yaml
services:
  - type: web
    name: evolveedu-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "cd evolveedu-ai/backend && gunicorn evolveedu.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        fromDatabase:
          name: evolveedu-db
          property: connectionString

databases:
  - name: evolveedu-db
    plan: free
```

### For Vercel (Frontend):

Create `vercel.json` in `evolveedu-ai/frontend`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
```

---

## ⚠️ Important Security Notes

### Before Deploying:

1. **Change SECRET_KEY:**
   ```python
   # Generate new secret key
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Set DEBUG=False** in production

3. **Update ALLOWED_HOSTS:**
   ```env
   ALLOWED_HOSTS=your-domain.com,your-app.onrender.com
   ```

4. **Never commit .env file:**
   - Add `.env` to `.gitignore`
   - Set environment variables in hosting platform

5. **Use PostgreSQL for production:**
   - SQLite is for development only
   - Get free PostgreSQL from Render, Railway, or Supabase

---

## 🎯 Recommended Deployment Stack

**For Best Results:**

1. **Backend (Django API):** Render.com
   - Free tier
   - PostgreSQL included
   - Auto-scaling

2. **Frontend (React):** Vercel
   - Free tier
   - CDN included
   - Auto-deploy from GitHub

3. **Database:** Render PostgreSQL (Free)
   - Included with Render backend
   - Automatic backups

4. **AI Provider:** Google Gemini
   - FREE unlimited
   - Already configured ✅

**Total Cost: $0/month** ✅

---

## 📊 Current Status

✅ **Google Gemini API:** Working  
✅ **Backend Structure:** Ready  
✅ **Requirements.txt:** Updated  
✅ **Environment Variables:** Configured  
⚠️ **Database:** Using SQLite (change to PostgreSQL for production)  
⚠️ **DEBUG Mode:** True (change to False for production)  

---

## 🚀 Quick Deploy Commands

### Test Locally First:
```bash
cd evolveedu-ai/backend
python test_gemini.py          # Test AI
python manage.py check         # Check for issues
python manage.py test          # Run tests
```

### Deploy to Render:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
# Then create web service on Render dashboard
```

### Deploy Frontend to Vercel:
```bash
cd evolveedu-ai/frontend
vercel --prod
```

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app

---

## ✅ Next Steps

1. ✅ Google Gemini is working locally
2. 🔄 Choose hosting platform (Render recommended)
3. 🔄 Create PostgreSQL database
4. 🔄 Set environment variables on hosting platform
5. 🔄 Deploy backend
6. 🔄 Deploy frontend
7. 🔄 Test live APIs

**Your app is ready for deployment!** 🎉
