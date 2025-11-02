"""
AI Service for Notes Generation and Enhancement
Supports multiple AI providers: OpenAI, GitHub Models (Copilot), Google Gemini
"""

import os
import sys
import json
import re
from typing import Dict, List
from dotenv import load_dotenv

# Add parent directory to path to import core module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.ai_service import ai_service

load_dotenv()


class NotesAIService:
    """Service for AI-powered note generation and enhancement"""

    def __init__(self):
        """Initialize AI service (supports multiple providers)"""
        self.ai = ai_service
        provider_info = self.ai.get_provider_info()
        print(f"📝 Notes AI using: {provider_info['provider']} ({provider_info['model']})")

    def _call_ai(self, prompt: str, system_prompt: str = None, max_tokens: int = 1000) -> str:
        """Call AI API with given prompt using unified service"""
        try:
            if not system_prompt:
                system_prompt = "You are an expert educational assistant. Provide clear, concise, and accurate responses."
            
            return self.ai.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=0.7
            )
        except Exception as e:
            return f"Error calling AI API: {str(e)}"

    @staticmethod
    def _extract_text_from_youtube(url: str) -> str:
        """Extract transcript from YouTube video"""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            
            # Extract video ID from URL
            video_id = url.split('v=')[-1].split('&')[0]
            
            # Get transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            text = ' '.join([t['text'] for t in transcript])
            return text
        except Exception as e:
            return f"Error extracting YouTube transcript: {str(e)}"

    @staticmethod
    def _extract_text_from_pdf(pdf_file) -> str:
        """Extract text from PDF file"""
        try:
            import PyPDF2
            
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"

    @classmethod
    def process_youtube_url(cls, url: str, title: str = "") -> Dict:
        """Process YouTube URL and generate structured notes"""
        service = cls()
        
        # Extract transcript
        text = service._extract_text_from_youtube(url)
        
        if "Error" in text:
            return {
                'error': text,
                'content': 'YouTube transcript could not be extracted',
                'summary': 'Please try another video or provide the transcript manually',
                'success': False
            }
        
        # Use OpenAI to generate components
        summary_prompt = f"""Provide a concise summary (2-3 sentences) of the following transcript:
        
{text[:2000]}"""
        
        summary = service._call_ai(summary_prompt, max_tokens=300)
        
        keypoints_prompt = f"""Extract 5 key points from this transcript as a JSON array:

{text[:2000]}

Respond ONLY with a JSON array like: ["point1", "point2", "point3", "point4", "point5"]"""
        
        keypoints_response = service._call_ai(keypoints_prompt, max_tokens=300)
        try:
            key_points = json.loads(keypoints_response)
        except:
            key_points = [s.strip() for s in keypoints_response.split('\n') if s.strip()][:5]
        
        questions_prompt = f"""Generate 5 study questions based on this transcript as a JSON array:

{text[:2000]}

Respond ONLY with a JSON array like: ["question1?", "question2?", "question3?", "question4?", "question5?"]"""
        
        questions_response = service._call_ai(questions_prompt, max_tokens=300)
        try:
            questions = json.loads(questions_response)
        except:
            questions = [s.strip() for s in questions_response.split('\n') if s.strip() and '?' in s][:5]
        
        # Estimate read time
        word_count = len(text.split())
        read_time = max(1, word_count // 200)
        
        return {
            'title': title or 'YouTube Video Notes',
            'content': text[:2000],
            'summary': summary,
            'key_points': key_points[:5],
            'questions': questions[:5],
            'difficulty_level': 'Intermediate',
            'estimated_read_time': read_time,
            'tags': ['youtube', 'video'],
            'success': True
        }

    @classmethod
    def process_text_input(cls, text: str, title: str = "") -> Dict:
        """Process text input and generate structured notes"""
        service = cls()
        
        # Generate summary
        summary_prompt = f"""Provide a concise summary (2-3 sentences) of the following text:
        
{text[:2000]}"""
        
        summary = service._call_ai(summary_prompt, max_tokens=300)
        
        # Generate key points
        keypoints_prompt = f"""Extract 5 key points from this text as a JSON array:

{text[:2000]}

Respond ONLY with a JSON array like: ["point1", "point2", "point3", "point4", "point5"]"""
        
        keypoints_response = service._call_ai(keypoints_prompt, max_tokens=300)
        try:
            key_points = json.loads(keypoints_response)
        except:
            key_points = [s.strip() for s in keypoints_response.split('\n') if s.strip()][:5]
        
        # Generate questions
        questions_prompt = f"""Generate 5 study questions based on this text as a JSON array:

{text[:2000]}

Respond ONLY with a JSON array like: ["question1?", "question2?", "question3?", "question4?", "question5?"]"""
        
        questions_response = service._call_ai(questions_prompt, max_tokens=300)
        try:
            questions = json.loads(questions_response)
        except:
            questions = [s.strip() for s in questions_response.split('\n') if s.strip() and '?' in s][:5]
        
        # Estimate read time
        word_count = len(text.split())
        read_time = max(1, word_count // 200)
        
        return {
            'title': title or 'AI Generated Notes',
            'content': text,
            'summary': summary,
            'key_points': key_points[:5],
            'questions': questions[:5],
            'difficulty_level': 'Intermediate',
            'estimated_read_time': read_time,
            'tags': ['text-input', 'ai-generated'],
            'success': True
        }

    @classmethod
    def process_pdf_file(cls, pdf_file, title: str = "") -> Dict:
        """Process PDF file and generate structured notes"""
        service = cls()
        
        # Extract text from PDF
        text = service._extract_text_from_pdf(pdf_file)
        
        if "Error" in text:
            return {
                'error': text,
                'content': 'PDF text could not be extracted',
                'summary': 'Please check the PDF file format',
                'success': False
            }
        
        # Use OpenAI to generate components
        summary_prompt = f"""Provide a concise summary (2-3 sentences) of this PDF content:
        
{text[:2000]}"""
        
        summary = service._call_ai(summary_prompt, max_tokens=300)
        
        keypoints_prompt = f"""Extract 5 key points from this PDF as a JSON array:

{text[:2000]}

Respond ONLY with a JSON array like: ["point1", "point2", "point3", "point4", "point5"]"""
        
        keypoints_response = service._call_ai(keypoints_prompt, max_tokens=300)
        try:
            key_points = json.loads(keypoints_response)
        except:
            key_points = [s.strip() for s in keypoints_response.split('\n') if s.strip()][:5]
        
        questions_prompt = f"""Generate 5 study questions based on this PDF as a JSON array:

{text[:2000]}

Respond ONLY with a JSON array like: ["question1?", "question2?", "question3?", "question4?", "question5?"]"""
        
        questions_response = service._call_ai(questions_prompt, max_tokens=300)
        try:
            questions = json.loads(questions_response)
        except:
            questions = [s.strip() for s in questions_response.split('\n') if s.strip() and '?' in s][:5]
        
        # Estimate read time
        word_count = len(text.split())
        read_time = max(1, word_count // 200)
        
        return {
            'title': title or 'PDF Notes',
            'content': text[:2000],
            'summary': summary,
            'key_points': key_points[:5],
            'questions': questions[:5],
            'difficulty_level': 'Intermediate',
            'estimated_read_time': read_time,
            'tags': ['pdf', 'ai-generated'],
            'success': True
        }

    @classmethod
    def enhance_existing_notes(cls, content: str) -> Dict:
        """Enhance existing notes with additional insights"""
        service = cls()
        
        enhance_prompt = f"""Enhance these study notes by adding:
1. More detailed explanations
2. Real-world examples
3. Common misconceptions to avoid
4. Practice tips

Original notes:
{content[:2000]}

Provide enhanced notes in a clear format."""
        
        enhanced_content = service._call_ai(enhance_prompt, max_tokens=1500)
        
        # Generate summary of enhancements
        summary_prompt = f"""Summarize what was added to enhance these notes (1-2 sentences):
{enhanced_content}"""
        
        summary = service._call_ai(summary_prompt, max_tokens=200)
        
        return {
            'enhanced_content': enhanced_content,
            'enhancement_summary': summary,
            'success': True
        }
