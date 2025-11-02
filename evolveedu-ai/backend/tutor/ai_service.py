import os
import json
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')


class TutorAIService:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.model = OPENAI_MODEL
        self.api_url = "https://api.openai.com/v1/chat/completions"
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not configured")

    def _call_openai(self, prompt, max_tokens=1000, system_prompt=None):
        try:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            system = system_prompt or "You are an expert tutor."
            payload = {"model": self.model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.7}
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Error: {str(e)}"

    @classmethod
    def generate_response(cls, question, context="", learning_level="Intermediate"):
        service = cls()
        prompt = f"Explain at a {learning_level} level: {question}"
        response = service._call_openai(prompt, max_tokens=1000)
        return {'response': response, 'learning_level': learning_level, 'success': True}

    @classmethod
    def explain_concept(cls, concept, level="Beginner"):
        service = cls()
        prompt = f"Explain '{concept}' at a {level} level with definition, characteristics, example, and why it matters."
        explanation = service._call_openai(prompt, max_tokens=800)
        return {'explanation': explanation, 'difficulty_level': level, 'success': True}

    @classmethod
    def generate_feedback(cls, student_answer, correct_answer, question):
        service = cls()
        prompt = f"Evaluate this student answer.\n\nQuestion: {question}\nStudent Answer: {student_answer}\nCorrect Answer: {correct_answer}"
        feedback = service._call_openai(prompt, max_tokens=800)
        return {'feedback': feedback, 'success': True}

    @classmethod
    def generate_adaptive_question(cls, topic, difficulty="Medium", student_performance=0.5):
        service = cls()
        if student_performance > 0.8:
            difficulty = "Hard"
        elif student_performance < 0.4:
            difficulty = "Easy"
        prompt = f"Generate a {difficulty} question about '{topic}'."
        response = service._call_openai(prompt, max_tokens=400)
        return {'question': response, 'difficulty': difficulty, 'success': True}

    @classmethod
    def categorize_question(cls, question):
        service = cls()
        prompt = f"Categorize this question type (Definition/Explanation/Example/Comparison/Calculation/Opinion): {question}"
        response = service._call_openai(prompt, max_tokens=20)
        return {'question_type': response.strip(), 'success': True}
