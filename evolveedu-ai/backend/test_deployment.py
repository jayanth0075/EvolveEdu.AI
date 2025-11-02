#!/usr/bin/env python
"""
EvolveEdu.AI - Pre-Deployment Test Script
Tests all critical components before deploying to production
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolveedu.settings')
django.setup()

def test_imports():
    """Test that all critical imports work"""
    print("\n🔍 Testing imports...")
    try:
        from core.ai_service import ai_service
        print("   ✅ core.ai_service imported successfully")
        
        from notes.ai_service import NotesAIService
        print("   ✅ notes.ai_service imported successfully")
        
        from quizzes.ai_service import QuizAIService
        print("   ✅ quizzes.ai_service imported successfully")
        
        from tutor.ai_service import TutorAIService
        print("   ✅ tutor.ai_service imported successfully")
        
        return True
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_service():
    """Test unified AI service"""
    print("\n🤖 Testing AI service...")
    try:
        from core.ai_service import ai_service
        
        # Check provider
        print(f"   📊 Provider: {ai_service.provider}")
        print(f"   📊 Model: {ai_service.model}")
        
        # Test generation with educational content (safer than math)
        response = ai_service.generate_completion(
            "What is machine learning? Answer in one simple sentence suitable for students.",
            max_tokens=100
        )
        
        if response and len(response) > 10:
            print(f"   ✅ AI generation working!")
            print(f"   📝 Response: {response[:100]}...")
            return True
        else:
            print("   ❌ AI generation returned empty or very short response")
            return False
            
    except Exception as e:
        print(f"   ❌ AI service error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database():
    """Test database connection"""
    print("\n🗄️  Testing database...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("   ✅ Database connection successful")
            
        # Check if migrations are applied
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            print(f"   ⚠️  Warning: {len(plan)} unapplied migrations")
            print("   Run: python manage.py migrate")
            return False
        else:
            print("   ✅ All migrations applied")
            return True
            
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\n🌍 Testing environment variables...")
    
    required_vars = [
        'SECRET_KEY',
        'AI_PROVIDER',
        'GOOGLE_API_KEY',
    ]
    
    all_present = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"   ✅ {var}: {masked}")
        else:
            print(f"   ❌ {var}: NOT SET")
            all_present = False
    
    # Warnings for production
    debug = os.getenv('DEBUG', 'True')
    if debug.lower() == 'true':
        print("   ⚠️  WARNING: DEBUG=True (should be False in production)")
    
    db_url = os.getenv('DATABASE_URL')
    if not db_url or 'sqlite' in db_url.lower():
        print("   ⚠️  WARNING: Using SQLite (use PostgreSQL in production)")
    
    return all_present

def test_models():
    """Test that all models are accessible"""
    print("\n📊 Testing models...")
    try:
        from accounts.models import User
        print(f"   ✅ User model: {User.objects.count()} users")
        
        from notes.models import Note
        print(f"   ✅ Note model: {Note.objects.count()} notes")
        
        from quizzes.models import Quiz
        print(f"   ✅ Quiz model: {Quiz.objects.count()} quizzes")
        
        from roadmaps.models import PersonalizedRoadmap
        print(f"   ✅ PersonalizedRoadmap model: {PersonalizedRoadmap.objects.count()} roadmaps")
        
        from tutor.models import TutorSession
        print(f"   ✅ TutorSession model: {TutorSession.objects.count()} sessions")
        
        return True
    except Exception as e:
        print(f"   ❌ Model error: {e}")
        return False

def test_settings():
    """Test Django settings"""
    print("\n⚙️  Testing Django settings...")
    try:
        from django.conf import settings
        
        print(f"   📊 DEBUG: {settings.DEBUG}")
        print(f"   📊 ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"   📊 DATABASE: {settings.DATABASES['default']['ENGINE']}")
        print(f"   📊 CORS_ORIGINS: {len(getattr(settings, 'CORS_ALLOWED_ORIGINS', []))} origins")
        
        # Check static files
        print(f"   📊 STATIC_URL: {settings.STATIC_URL}")
        print(f"   📊 STATIC_ROOT: {getattr(settings, 'STATIC_ROOT', 'Not set')}")
        
        return True
    except Exception as e:
        print(f"   ❌ Settings error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 EvolveEdu.AI - Pre-Deployment Test Suite")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "Environment Variables": test_environment(),
        "Django Settings": test_settings(),
        "Database": test_database(),
        "Models": test_models(),
        "AI Service": test_ai_service(),
    }
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"\n🎯 Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED! Your app is ready for deployment!")
        print("\n📋 Next Steps:")
        print("   1. Review DEPLOYMENT_GUIDE.md")
        print("   2. Choose hosting platform (Render recommended)")
        print("   3. Set environment variables on hosting platform")
        print("   4. Deploy!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Fix issues before deploying.")
        print("\n📋 Troubleshooting:")
        print("   - Check .env file configuration")
        print("   - Run: python manage.py migrate")
        print("   - Verify Google API key is valid")
        print("   - Review error messages above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
