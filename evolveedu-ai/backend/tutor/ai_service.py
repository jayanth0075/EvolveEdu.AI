"""
AI Service for Tutor (Q&A Chatbot)
Uses HuggingFace models for question answering and concept explanation
"""

import os
import re
from typing import Dict, List, Optional
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv('HF_API_KEY', '')


class TutorAIService:
    """Service for AI-powered tutoring and Q&A"""

    def __init__(self):
        """Initialize HuggingFace models"""
        try:
            # QA model for answering questions based on context
            self.qa_pipeline = pipeline(
                "question-answering",
                model="deepset/roberta-large-squad2-distilled",
                device=0 if self._has_gpu() else -1
            )
        except:
            self.qa_pipeline = None
        
        try:
            # Zero-shot classification for understanding question intent
            self.classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=0 if self._has_gpu() else -1
            )
        except:
            self.classifier = None

    @staticmethod
    def _has_gpu():
        """Check if GPU is available"""
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False

    @staticmethod
    def _categorize_question(question: str) -> str:
        """Categorize question type"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['what is', 'what are', 'define', 'explain']):
            return 'definition'
        elif any(word in question_lower for word in ['how', 'why', 'solve']):
            return 'explanation'
        elif any(word in question_lower for word in ['give example', 'example', 'like']):
            return 'example'
        elif any(word in question_lower for word in ['different', 'difference', 'compare', 'vs']):
            return 'comparison'
        elif any(word in question_lower for word in ['when', 'where', 'which']):
            return 'specific'
        else:
            return 'general'

    @staticmethod
    def _get_knowledge_base_context(question: str, topic: str = '') -> str:
        """Get relevant context from knowledge base"""
        # This would connect to a knowledge base in production
        # For now, return a generic context
        
        contexts = {
            'programming': """
                Programming is the process of creating a set of instructions that tell a computer
                how to perform a task. Programming can be done using a variety of computer programming
                languages, such as JavaScript, Python, and C++. Programmers use these languages to
                communicate with computers and create software applications.
                
                Key concepts: Variables, Data types, Functions, Loops, Conditionals, Arrays,
                Object-oriented programming, Functional programming, Design patterns
            """,
            'mathematics': """
                Mathematics is the study of numbers, quantity, shape, and space. It involves the study
                of quantities, structures, space, and change. Mathematicians use patterns, formulas,
                and logical deduction to solve problems and make discoveries.
                
                Key concepts: Algebra, Geometry, Calculus, Statistics, Linear Algebra, Probability
            """,
            'science': """
                Science is a systematic enterprise that builds and organizes knowledge in the form
                of testable explanations and predictions about the natural world. It involves
                observation, experimentation, and the development of theories.
                
                Key concepts: Physics, Chemistry, Biology, Earth Science, Astronomy
            """,
            'history': """
                History is the study of past events and how they shaped human civilization.
                It involves analyzing primary sources, understanding context, and identifying
                patterns and causes of historical events.
                
                Key concepts: Ancient history, Medieval history, Modern history, World history, Cultural history
            """
        }
        
        # Find best matching context
        question_lower = question.lower()
        for key, context in contexts.items():
            if key in question_lower or key in topic.lower():
                return context
        
        return contexts['programming']  # Default context

    @classmethod
    def generate_response(cls, question: str, context: Optional[str] = None, topic: str = '') -> Dict:
        """Generate AI response to a student question"""
        service = cls()
        
        # Categorize question
        question_type = service._categorize_question(question)
        
        # Get knowledge base context if not provided
        if not context:
            context = service._get_knowledge_base_context(question, topic)
        
        # Generate answer using QA model
        answer = ""
        try:
            if service.qa_pipeline and len(context) > 50:
                # Extract answer from context
                qa_input = {
                    'question': question,
                    'context': context
                }
                result = service.qa_pipeline(qa_input)
                answer = result['answer']
            else:
                answer = cls._generate_template_response(question, question_type, context)
        except:
            answer = cls._generate_template_response(question, question_type, context)
        
        # Generate follow-up suggestions
        follow_ups = cls._generate_follow_up_questions(question, question_type)
        
        # Generate related concepts
        related_concepts = cls._extract_related_concepts(question, context)
        
        return {
            'question': question,
            'answer': answer,
            'question_type': question_type,
            'confidence': 0.85,
            'follow_up_questions': follow_ups,
            'related_concepts': related_concepts,
            'sources': [topic] if topic else ['General Knowledge']
        }

    @staticmethod
    def _generate_template_response(question: str, question_type: str, context: str) -> str:
        """Generate response using templates"""
        templates = {
            'definition': f"""
                Based on the concept you're asking about:
                
                {context[:500]}...
                
                Key points to remember:
                - This is a fundamental concept in the field
                - Understanding this will help you grasp more advanced topics
                - Try to connect this with real-world examples
            """,
            'explanation': f"""
                Here's how this works:
                
                {context[:500]}...
                
                Step-by-step breakdown:
                1. First, understand the basic concept
                2. Learn the underlying principles
                3. Apply it to concrete examples
                4. Practice with different scenarios
            """,
            'example': f"""
                Here are some examples:
                
                {context[:300]}...
                
                Real-world applications:
                - In academic settings, this is used for...
                - In professional contexts, you'll encounter...
                - Common scenarios include...
            """,
            'comparison': f"""
                Here's how they compare:
                
                {context[:400]}...
                
                Key differences:
                - Similarity 1
                - Difference 1
                - When to use each
                - Pros and cons of each approach
            """,
            'general': f"""
                Great question! Here's what you should know:
                
                {context[:500]}...
                
                Additional insights:
                - This concept connects to...
                - Common misconceptions to avoid...
                - Resources for deeper learning
            """
        }
        
        return templates.get(question_type, templates['general'])

    @staticmethod
    def _generate_follow_up_questions(question: str, question_type: str) -> List[str]:
        """Generate follow-up questions"""
        follow_ups = {
            'definition': [
                'What is the history of this concept?',
                'How is this used in real-world applications?',
                'What are common misconceptions about this?'
            ],
            'explanation': [
                'Can you give me an example?',
                'Why is this important to understand?',
                'What happens if we change one of the variables?'
            ],
            'example': [
                'Can you explain the principle behind this example?',
                'How would this work in a different scenario?',
                'What are the edge cases?'
            ],
            'comparison': [
                'Which one should I use in my case?',
                'What are the performance implications?',
                'How do they combine or interact?'
            ],
            'general': [
                'Can you explain this more simply?',
                'How does this relate to other concepts?',
                'What should I study next?'
            ]
        }
        
        return follow_ups.get(question_type, follow_ups['general'])[:3]

    @staticmethod
    def _extract_related_concepts(question: str, context: str) -> List[str]:
        """Extract related concepts from context"""
        # Simple keyword extraction
        keywords = [
            'algorithm', 'data structure', 'complexity', 'optimization',
            'pattern', 'concept', 'principle', 'method', 'approach',
            'theory', 'framework', 'model', 'system'
        ]
        
        related = []
        for keyword in keywords:
            if keyword in context.lower():
                related.append(keyword.title())
        
        return related[:5] if related else ['Related Topics', 'Advanced Concepts', 'Practice Problems']

    @classmethod
    def explain_concept(cls, topic: str, difficulty_level: str = 'Intermediate') -> Dict:
        """Explain a concept at a specific difficulty level"""
        explanations = {
            'Beginner': f"""
                Let's start with the basics of {topic}:
                
                {topic} is a fundamental concept that involves...
                
                Simple analogy: Think of it like...
                
                Key takeaways:
                - Point 1
                - Point 2
                - Point 3
            """,
            'Intermediate': f"""
                Understanding {topic} at the intermediate level:
                
                {topic} is built on several key principles...
                
                How it connects to other concepts:
                - Connection 1
                - Connection 2
                - Connection 3
                
                Common applications:
                - Application 1
                - Application 2
            """,
            'Advanced': f"""
                Advanced understanding of {topic}:
                
                At the advanced level, {topic} involves:
                - Deep principle 1
                - Deep principle 2
                - Deep principle 3
                
                Mathematical formulation: ...
                
                Research directions and open problems...
            """
        }
        
        explanation = explanations.get(difficulty_level, explanations['Intermediate'])
        
        return {
            'topic': topic,
            'difficulty_level': difficulty_level,
            'explanation': explanation,
            'key_points': [
                'Point 1: Understanding the fundamentals',
                'Point 2: Connecting with other concepts',
                'Point 3: Practical applications'
            ],
            'learning_resources': [
                'Tutorial videos',
                'Research papers',
                'Practice problems',
                'Real-world examples'
            ],
            'prerequisite_knowledge': [
                'Basic concept 1',
                'Basic concept 2',
                'Foundational principle'
            ]
        }

    @classmethod
    def generate_feedback(cls, student_answer: str, correct_answer: str, question: str) -> Dict:
        """Generate feedback on student's answer"""
        service = cls()
        
        # Analyze answer quality
        is_correct = cls._evaluate_answer(student_answer, correct_answer)
        
        if is_correct:
            feedback = "Excellent! Your answer is correct."
            suggestions = [
                "Great job understanding this concept!",
                "Try explaining this to someone else to deepen your understanding",
                "Can you identify similar problems and solve them?"
            ]
        else:
            feedback = "Not quite right. Let me help you understand better."
            suggestions = cls._generate_learning_suggestions(student_answer, correct_answer)
        
        return {
            'is_correct': is_correct,
            'feedback': feedback,
            'correct_answer': correct_answer,
            'student_answer': student_answer,
            'explanation': f"""
                The correct answer is: {correct_answer}
                
                Here's why:
                - Key reason 1
                - Key reason 2
                - Key reason 3
            """,
            'learning_suggestions': suggestions,
            'similar_problems': [
                'Problem 1',
                'Problem 2',
                'Problem 3'
            ],
            'confidence_score': 0.9 if is_correct else 0.7
        }

    @staticmethod
    def _evaluate_answer(student_answer: str, correct_answer: str) -> bool:
        """Simple answer evaluation"""
        # Remove common variations
        student_clean = student_answer.lower().strip()
        correct_clean = correct_answer.lower().strip()
        
        # Exact match
        if student_clean == correct_clean:
            return True
        
        # Partial match (contains key words)
        key_words = correct_clean.split()
        if len(key_words) > 0 and all(word in student_clean for word in key_words[:min(2, len(key_words))]):
            return True
        
        return False

    @staticmethod
    def _generate_learning_suggestions(student_answer: str, correct_answer: str) -> List[str]:
        """Generate suggestions for improvement"""
        return [
            "Review the key concepts related to this problem",
            "Try breaking down the problem into smaller parts",
            "Look for similar worked examples in your textbook",
            "Discuss this problem with your peers or instructor",
            "Practice more problems of this type to build confidence"
        ]

    @classmethod
    def generate_adaptive_question(cls, student_performance: Dict) -> Dict:
        """Generate next question based on student performance"""
        average_score = student_performance.get('average_score', 50)
        incorrect_topics = student_performance.get('incorrect_topics', [])
        
        # Adjust difficulty based on performance
        if average_score > 80:
            difficulty = 'Hard'
            topic_focus = 'advanced'
        elif average_score > 60:
            difficulty = 'Medium'
            topic_focus = 'intermediate'
        else:
            difficulty = 'Easy'
            topic_focus = 'fundamental'
        
        # Focus on weak areas
        if incorrect_topics:
            topic = incorrect_topics[0]
        else:
            topic = 'General'
        
        return {
            'recommended_difficulty': difficulty,
            'recommended_topic': topic,
            'question_type': 'conceptual' if average_score < 70 else 'application',
            'estimated_time': 5 if difficulty == 'Easy' else (10 if difficulty == 'Medium' else 15),
            'tips': [
                f"This is a {difficulty} level question",
                f"Focus on understanding the {topic} concept",
                "Take your time and read carefully",
                "Show your work/reasoning"
            ]
        }
