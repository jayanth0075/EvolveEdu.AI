"""
AI Service for Quiz Generation and Recommendations
Uses OpenAI GPT for generating questions and scoring
"""

import os
import json
import random
from typing import Dict, List, Tuple
import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')


class QuizAIService:
    """Service for AI-powered quiz generation and management"""

    def __init__(self):
        """Initialize OpenAI client"""
        self.api_key = OPENAI_API_KEY
        self.model = OPENAI_MODEL
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not configured in .env file")

    def _call_openai(self, prompt: str, max_tokens: int = 1000) -> str:
        """Call OpenAI API with given prompt"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are an expert quiz designer. Create clear, fair, and educational quiz questions. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException as e:
            return f"Error calling OpenAI API: {str(e)}"
        except Exception as e:
            return f"Error processing response: {str(e)}"

    @classmethod
    def generate_quiz_from_text(cls, text: str, num_questions: int = 5, difficulty: str = 'Medium') -> Dict:
        """Generate quiz questions from text content"""
        service = cls()
        
        prompt = f"""Generate {num_questions} quiz questions from this text at {difficulty} difficulty level.
        
Text: {text[:2000]}

Create a JSON response with this format:
{{
    "questions": [
        {{
            "question": "Question text?",
            "question_type": "multiple_choice",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer_index": 0,
            "difficulty_level": "{difficulty}",
            "points": 10
        }}
    ]
}}

Include both multiple choice questions (3-4 questions) and true/false questions (1-2 questions).
Ensure answers are factually correct based on the text.
"""
        
        response = service._call_openai(prompt, max_tokens=2000)
        
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            json_str = response[start_idx:end_idx]
            data = json.loads(json_str)
            
            return {
                'title': 'AI-Generated Quiz',
                'description': 'Quiz generated from text content',
                'questions': data.get('questions', [])[:num_questions],
                'total_questions': len(data.get('questions', [])),
                'difficulty_level': difficulty,
                'success': True
            }
        except:
            return {
                'error': 'Failed to parse quiz response',
                'success': False,
                'questions': []
            }

    @classmethod
    def generate_quiz_from_notes(cls, notes_list: List[str], difficulty: str = 'Medium', num_questions: int = 10) -> Dict:
        """Generate quiz from multiple notes"""
        combined_text = ' '.join(notes_list)
        return cls.generate_quiz_from_text(combined_text, num_questions, difficulty)

    @classmethod
    def score_quiz_response(cls, submitted_responses: List[Dict], correct_answers: List[Dict]) -> Dict:
        """Score quiz responses"""
        if len(submitted_responses) != len(correct_answers):
            return {'error': 'Response count mismatch', 'score': 0, 'percentage': 0}
        
        correct_count = 0
        total_points = 0
        earned_points = 0
        
        feedback = []
        
        for submitted, correct in zip(submitted_responses, correct_answers):
            points = correct.get('points', 10)
            total_points += points
            
            if submitted.get('answer_index') == correct.get('correct_answer_index'):
                correct_count += 1
                earned_points += points
                feedback.append({
                    'question_index': len(feedback),
                    'correct': True,
                    'message': 'Correct!'
                })
            else:
                feedback.append({
                    'question_index': len(feedback),
                    'correct': False,
                    'correct_answer': correct.get('correct_answer', ''),
                    'message': f"Incorrect. The correct answer was: {correct.get('correct_answer', '')}"
                })
        
        percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        
        return {
            'correct_answers': correct_count,
            'total_questions': len(correct_answers),
            'earned_points': earned_points,
            'total_points': total_points,
            'percentage': round(percentage, 2),
            'feedback': feedback,
            'success': True
        }

    @classmethod
    def analyze_quiz_performance(cls, quiz_attempts: List[Dict]) -> Dict:
        """Analyze quiz performance trends"""
        if not quiz_attempts:
            return {'error': 'No attempts found'}
        
        scores = [attempt.get('score', 0) for attempt in quiz_attempts]
        avg_score = sum(scores) / len(scores) if scores else 0
        highest_score = max(scores) if scores else 0
        lowest_score = min(scores) if scores else 0
        
        # Identify weak areas
        weak_topics = []
        for attempt in quiz_attempts:
            if attempt.get('score', 0) < 60:
                topic = attempt.get('topic', 'Unknown')
                if topic not in weak_topics:
                    weak_topics.append(topic)
        
        return {
            'average_score': round(avg_score, 2),
            'highest_score': highest_score,
            'lowest_score': lowest_score,
            'total_attempts': len(quiz_attempts),
            'weak_areas': weak_topics,
            'improvement_trend': 'improving' if len(scores) > 1 and scores[-1] > scores[0] else 'stable',
            'success': True
        }

    @classmethod
    def get_quiz_recommendations(cls, performance_data: Dict) -> Dict:
        """Get quiz recommendations based on performance"""
        service = cls()
        
        weak_areas = performance_data.get('weak_areas', [])
        avg_score = performance_data.get('average_score', 0)
        
        if not weak_areas:
            return {
                'recommendations': ['Keep practicing to maintain your strong performance!'],
                'next_quiz_difficulty': 'Advanced',
                'topics_to_focus': []
            }
        
        prompt = f"""Based on the following weak areas and average score, provide quiz recommendations:

Weak Areas: {', '.join(weak_areas)}
Average Score: {avg_score}%

Provide 3-4 specific recommendations as JSON array.
Response format: {{"recommendations": ["rec1", "rec2", "rec3"], "suggested_difficulty": "Medium or Hard"}}
"""
        
        response = service._call_openai(prompt, max_tokens=500)
        
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            json_str = response[start_idx:end_idx]
            data = json.loads(json_str)
            
            return {
                'recommendations': data.get('recommendations', []),
                'next_quiz_difficulty': data.get('suggested_difficulty', 'Medium'),
                'topics_to_focus': weak_areas,
                'success': True
            }
        except:
            return {
                'recommendations': [
                    f'Focus more on: {", ".join(weak_areas)}',
                    'Practice regularly with quizzes on your weak areas',
                    'Review the notes on difficult topics'
                ],
                'next_quiz_difficulty': 'Medium',
                'topics_to_focus': weak_areas,
                'success': True
            }

        for i, (response, correct) in enumerate(zip(submitted_responses, correct_answers)):
            question_index = i + 1
            
            if response.get('answer_index') == correct.get('correct_answer_index'):
                correct_count += 1
                points_earned = correct.get('points', 10)
                earned_points += points_earned
                feedback.append({
                    'question_number': question_index,
                    'correct': True,
                    'feedback': 'Great job!'
                })
            else:
                feedback.append({
                    'question_number': question_index,
                    'correct': False,
                    'correct_answer': correct.get('correct_answer'),
                    'your_answer': correct.get('options', [])[response.get('answer_index', 0)] if response.get('answer_index') is not None else 'Not answered',
                    'feedback': 'This is incorrect. Review the concept again.'
                })
            
            total_points += correct.get('points', 10)
        
        percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        
        # Determine performance level
        if percentage >= 90:
            performance = 'Excellent'
        elif percentage >= 75:
            performance = 'Good'
        elif percentage >= 60:
            performance = 'Fair'
        else:
            performance = 'Needs Improvement'
        
        return {
            'score': earned_points,
            'total_points': total_points,
            'percentage': round(percentage, 2),
            'correct_answers': correct_count,
            'total_questions': len(correct_answers),
            'performance_level': performance,
            'feedback': feedback
        }

    @classmethod
    def analyze_quiz_performance(cls, attempts: List[Dict]) -> Dict:
        """Analyze user's quiz performance over time"""
        if not attempts:
            return {
                'error': 'No attempts found',
                'total_attempts': 0,
                'average_score': 0
            }
        
        percentages = [attempt.get('percentage', 0) for attempt in attempts]
        scores = [attempt.get('score', 0) for attempt in attempts]
        
        average_score = sum(scores) / len(scores) if scores else 0
        average_percentage = sum(percentages) / len(percentages) if percentages else 0
        highest_score = max(scores) if scores else 0
        lowest_score = min(scores) if scores else 0
        
        # Trend analysis
        if len(attempts) >= 2:
            recent_3 = percentages[-3:] if len(percentages) >= 3 else percentages
            older_avg = sum(percentages[:-3]) / (len(percentages) - 3) if len(percentages) > 3 else percentages[0]
            recent_avg = sum(recent_3) / len(recent_3)
            
            if recent_avg > older_avg:
                trend = 'Improving'
            elif recent_avg < older_avg:
                trend = 'Declining'
            else:
                trend = 'Stable'
        else:
            trend = 'Insufficient data'
        
        # Weak areas (questions answered incorrectly most often)
        wrong_categories = {}
        for attempt in attempts:
            for feedback in attempt.get('feedback', []):
                if not feedback.get('correct'):
                    category = feedback.get('category', 'general')
                    wrong_categories[category] = wrong_categories.get(category, 0) + 1
        
        weak_areas = sorted(wrong_categories.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'total_attempts': len(attempts),
            'average_score': round(average_score, 2),
            'average_percentage': round(average_percentage, 2),
            'highest_score': highest_score,
            'lowest_score': lowest_score,
            'trend': trend,
            'weak_areas': [area[0] for area in weak_areas],
            'recommendation': cls._generate_recommendation(average_percentage, trend)
        }

    @staticmethod
    def _generate_recommendation(average_percentage: float, trend: str) -> str:
        """Generate personalized recommendation based on performance"""
        if average_percentage >= 85 and trend == 'Improving':
            return 'Excellent progress! Try harder difficulty quizzes.'
        elif average_percentage >= 75:
            return 'Good performance. Keep practicing to improve further.'
        elif average_percentage >= 60:
            return 'Fair performance. Review key concepts and try again.'
        elif trend == 'Improving':
            return 'You are improving. Keep consistent with your practice.'
        else:
            return 'Consider reviewing the material more thoroughly before taking quizzes.'

    @classmethod
    def get_quiz_recommendations(cls, user_history: List[Dict], all_available_quizzes: List[Dict]) -> List[Dict]:
        """Recommend quizzes based on user history"""
        if not user_history:
            # Return popular quizzes for new users
            return all_available_quizzes[:5]
        
        # Analyze user's performance
        weak_categories = {}
        for attempt in user_history:
            score_percent = attempt.get('percentage', 0)
            if score_percent < 70:
                category = attempt.get('category', 'general')
                weak_categories[category] = weak_categories.get(category, 0) + 1
        
        # Recommend quizzes in weak areas
        recommendations = []
        for quiz in all_available_quizzes:
            quiz_category = quiz.get('category', 'general')
            
            # Prioritize weak areas
            if quiz_category in weak_categories:
                quiz['priority'] = weak_categories[quiz_category]
                recommendations.append(quiz)
        
        # Sort by priority
        recommendations.sort(key=lambda x: x.get('priority', 0), reverse=True)
        
        # Add some general recommendations
        for quiz in all_available_quizzes:
            if quiz not in recommendations and len(recommendations) < 5:
                recommendations.append(quiz)
        
        return recommendations[:5]

    @classmethod
    def generate_study_plan(cls, weak_areas: List[str], available_quizzes: List[Dict]) -> Dict:
        """Generate personalized study plan based on weak areas"""
        study_plan = {
            'duration_days': 7,
            'daily_quizzes': 2,
            'daily_study_minutes': 30,
            'schedule': []
        }
        
        # Create daily schedule
        for day in range(1, 8):
            daily_plan = {
                'day': day,
                'quizzes': [],
                'focus_areas': []
            }
            
            # Assign quizzes to days
            for i, weak_area in enumerate(weak_areas):
                if i % 7 < day:
                    matching_quizzes = [q for q in available_quizzes if weak_area.lower() in q.get('title', '').lower()]
                    if matching_quizzes:
                        daily_plan['quizzes'].append(matching_quizzes[0])
                    daily_plan['focus_areas'].append(weak_area)
            
            study_plan['schedule'].append(daily_plan)
        
        return study_plan
