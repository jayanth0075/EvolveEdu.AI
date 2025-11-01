"""
AI Service for Quiz Generation and Recommendations
Uses HuggingFace models for generating questions and scoring
"""

import os
import json
import random
from typing import Dict, List, Tuple
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv('HF_API_KEY', '')


class QuizAIService:
    """Service for AI-powered quiz generation and management"""

    def __init__(self):
        """Initialize HuggingFace models"""
        try:
            self.qa_pipeline = pipeline(
                "question-answering",
                model="deepset/roberta-base-squad2",
                device=0 if self._has_gpu() else -1
            )
        except:
            self.qa_pipeline = None

    @staticmethod
    def _has_gpu():
        """Check if GPU is available"""
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False

    @staticmethod
    def _generate_multiple_choice(question: str, correct_answer: str, context: str) -> Dict:
        """Generate multiple choice options for a question"""
        # Generate distractors from context
        words = context.split()
        random.shuffle(words)
        
        # Create simple distractors (in production, use more sophisticated methods)
        distractors = []
        
        # Distractor 1: Random phrases from context
        if len(words) > 10:
            distractor1 = ' '.join(random.sample(words, min(5, len(words))))
            distractors.append(distractor1)
        
        # Distractor 2: Partial answer
        answer_words = correct_answer.split()
        if len(answer_words) > 1:
            distractor2 = ' '.join(answer_words[:-1])
            distractors.append(distractor2)
        else:
            distractor2 = correct_answer + ' not'
            distractors.append(distractor2)
        
        # Distractor 3: Similar word
        distractors.append(f"None of the above")
        
        # Compile options
        options = [correct_answer] + distractors[:3]
        random.shuffle(options)
        
        return {
            'options': options,
            'correct_index': options.index(correct_answer),
            'correct_answer': correct_answer
        }

    @classmethod
    def generate_quiz_from_text(cls, text: str, num_questions: int = 5, difficulty: str = 'Medium') -> Dict:
        """Generate quiz questions from text content"""
        service = cls()
        
        # Split text into sentences
        import re
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            return {'error': 'Text too short to generate quiz', 'questions': []}
        
        questions = []
        
        # Generate questions from sentences
        for i, sentence in enumerate(sentences[:num_questions]):
            # Multiple choice question
            question_text = f"Which of the following best describes: {sentence[:80]}...?"
            
            choice = service._generate_multiple_choice(
                question_text,
                sentence[:50],
                text
            )
            
            questions.append({
                'question': question_text,
                'question_type': 'multiple_choice',
                'options': choice['options'],
                'correct_answer_index': choice['correct_index'],
                'difficulty_level': difficulty,
                'points': 10 if difficulty == 'Easy' else (20 if difficulty == 'Medium' else 30)
            })
        
        # Add true/false questions
        for i in range(min(2, num_questions // 2)):
            sentence = random.choice(sentences)
            questions.append({
                'question': f"True or False: {sentence[:80]}?",
                'question_type': 'true_false',
                'options': ['True', 'False'],
                'correct_answer_index': 0,
                'difficulty_level': difficulty,
                'points': 5
            })
        
        return {
            'title': f'Auto-Generated Quiz',
            'description': 'Quiz generated from text content',
            'questions': questions[:num_questions],
            'total_questions': len(questions),
            'difficulty_level': difficulty,
            'total_points': sum(q.get('points', 10) for q in questions[:num_questions])
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
