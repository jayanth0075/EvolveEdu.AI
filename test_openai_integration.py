"""
Quick test script to verify OpenAI integration is working
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, 'c:\\Users\\m9963\\PycharmProjects\\AI\\FEFW-DJ-EvolveEd.ai\\evolveedu-ai\\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolveedu.settings')
django.setup()

from notes.ai_service import NotesAIService
from quizzes.ai_service import QuizAIService
from tutor.ai_service import TutorAIService

print("=" * 60)
print("Testing OpenAI Integration")
print("=" * 60)

# Test 1: Notes AI Service
print("\n1️⃣ Testing Notes AI Service...")
try:
    notes_service = NotesAIService()
    result = notes_service.process_text_input(
        "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
        title="ML Overview"
    )
    if result.get('success'):
        print("✅ Notes AI: SUCCESS")
        print(f"   Summary: {result.get('summary', '')[:100]}...")
    else:
        print(f"❌ Notes AI: FAILED - {result.get('error', 'Unknown error')}")
except Exception as e:
    print(f"❌ Notes AI Error: {str(e)}")

# Test 2: Quiz AI Service
print("\n2️⃣ Testing Quiz AI Service...")
try:
    quiz_service = QuizAIService()
    result = quiz_service.generate_quiz_from_text(
        "Python is a high-level programming language known for its simplicity and readability.",
        num_questions=3,
        difficulty="Easy"
    )
    if result.get('success'):
        print("✅ Quiz AI: SUCCESS")
        print(f"   Questions generated: {len(result.get('questions', []))}")
    else:
        print(f"❌ Quiz AI: FAILED - {result.get('error', 'Unknown error')}")
except Exception as e:
    print(f"❌ Quiz AI Error: {str(e)}")

# Test 3: Tutor AI Service
print("\n3️⃣ Testing Tutor AI Service...")
try:
    tutor_service = TutorAIService()
    result = tutor_service.generate_response(
        "What is the difference between a list and a tuple in Python?",
        learning_level="Beginner"
    )
    if result.get('success'):
        print("✅ Tutor AI: SUCCESS")
        print(f"   Response: {result.get('response', '')[:100]}...")
    else:
        print(f"❌ Tutor AI: FAILED - {result.get('error', 'Unknown error')}")
except Exception as e:
    print(f"❌ Tutor AI Error: {str(e)}")

print("\n" + "=" * 60)
print("Testing Complete!")
print("=" * 60)
