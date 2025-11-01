"""
AI Service for Notes Generation and Enhancement
Uses HuggingFace Transformers for text summarization, Q&A generation, and key point extraction
"""

import os
import json
import re
from typing import Dict, List
import requests
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv('HF_API_KEY', '')


class NotesAIService:
    """Service for AI-powered note generation and enhancement"""

    def __init__(self):
        """Initialize HuggingFace models"""
        # Summarization model
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=0 if self._has_gpu() else -1
        )
        
        # Question answering model for Q&A generation
        self.qa_pipeline = pipeline(
            "question-answering",
            model="deepset/roberta-base-squad2",
            device=0 if self._has_gpu() else -1
        )

    @staticmethod
    def _has_gpu():
        """Check if GPU is available"""
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False

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

    @staticmethod
    def _extract_key_points(text: str, num_points: int = 5) -> List[str]:
        """Extract key points from text using sentence importance"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Simple heuristic: longer, more complex sentences are likely key points
        scored_sentences = [
            (s, len(s.split())) for s in sentences
        ]
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        key_points = [s[0] for s in scored_sentences[:num_points]]
        return [point for point in key_points if point]

    @staticmethod
    def _generate_questions_from_text(text: str, num_questions: int = 5) -> List[str]:
        """Generate potential questions from text"""
        questions = []
        
        # Extract sentences that contain important words
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Generate questions from selected sentences
        for sentence in sentences[:num_questions]:
            # Simple question generation patterns
            if ' is ' in sentence.lower():
                question = sentence.replace(' is ', ' is what ').rstrip() + '?'
                questions.append(question)
            elif ' have ' in sentence.lower():
                words = sentence.split()
                question = f"What {' '.join(words)}?"
                questions.append(question)
            else:
                question = f"Explain: {sentence.rstrip()}?"
                questions.append(question)
        
        return questions[:num_questions]

    @staticmethod
    def _estimate_difficulty(text: str) -> str:
        """Estimate text difficulty level based on word complexity"""
        words = text.split()
        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
        
        if avg_word_length < 4:
            return "Easy"
        elif avg_word_length < 6:
            return "Medium"
        else:
            return "Hard"

    @staticmethod
    def _estimate_read_time(text: str) -> int:
        """Estimate reading time in minutes (avg 200 words per minute)"""
        words = len(text.split())
        return max(1, words // 200)

    def _summarize_text(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """Generate summary using BART model"""
        try:
            # Split text into chunks if too long (model has token limit)
            max_chunk_length = 1000
            chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
            
            summaries = []
            for chunk in chunks[:3]:  # Limit to 3 chunks to avoid too much processing
                if len(chunk.split()) > 20:
                    try:
                        summary = self.summarizer(chunk, max_length=max_length, min_length=min_length)
                        summaries.append(summary[0]['summary_text'])
                    except:
                        pass
            
            return ' '.join(summaries) if summaries else text[:500]
        except Exception as e:
            return f"Summary generation error: {str(e)}"

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
                'summary': 'Please try another video or provide the transcript manually'
            }
        
        # Generate components
        summary = service._summarize_text(text)
        key_points = service._extract_key_points(text)
        questions = service._generate_questions_from_text(text)
        difficulty = service._estimate_difficulty(text)
        read_time = service._estimate_read_time(text)
        
        # Extract tags from text
        tags = ['youtube', 'video']
        if any(word in text.lower() for word in ['python', 'javascript', 'java']):
            tags.append('programming')
        if any(word in text.lower() for word in ['algorithm', 'data structure', 'complexity']):
            tags.append('algorithms')
        if any(word in text.lower() for word in ['machine learning', 'ai', 'neural']):
            tags.append('AI/ML')
        
        return {
            'title': title or 'YouTube Notes',
            'content': text[:2000],  # Store first 2000 chars as preview
            'summary': summary,
            'key_points': key_points[:5],
            'questions': questions[:5],
            'difficulty_level': difficulty,
            'estimated_read_time': read_time,
            'tags': tags
        }

    @classmethod
    def process_text_input(cls, text: str, title: str) -> Dict:
        """Process text input and generate structured notes"""
        service = cls()
        
        # Generate components
        summary = service._summarize_text(text)
        key_points = service._extract_key_points(text)
        questions = service._generate_questions_from_text(text)
        difficulty = service._estimate_difficulty(text)
        read_time = service._estimate_read_time(text)
        
        # Extract tags from text
        tags = ['text-input']
        if any(word in text.lower() for word in ['python', 'javascript', 'java', 'code']):
            tags.append('programming')
        if any(word in text.lower() for word in ['math', 'equation', 'formula']):
            tags.append('mathematics')
        if any(word in text.lower() for word in ['history', 'historical', 'dates']):
            tags.append('history')
        
        return {
            'title': title,
            'content': text,
            'summary': summary,
            'key_points': key_points[:5],
            'questions': questions[:5],
            'difficulty_level': difficulty,
            'estimated_read_time': read_time,
            'tags': tags
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
                'summary': 'Please check the PDF file format'
            }
        
        # Generate components
        summary = service._summarize_text(text)
        key_points = service._extract_key_points(text)
        questions = service._generate_questions_from_text(text)
        difficulty = service._estimate_difficulty(text)
        read_time = service._estimate_read_time(text)
        
        # Extract tags from text
        tags = ['pdf']
        if any(word in text.lower() for word in ['research', 'study', 'methodology']):
            tags.append('research')
        if any(word in text.lower() for word in ['business', 'economics', 'finance']):
            tags.append('business')
        
        return {
            'title': title or 'PDF Notes',
            'content': text[:2000],  # Store first 2000 chars as preview
            'summary': summary,
            'key_points': key_points[:5],
            'questions': questions[:5],
            'difficulty_level': difficulty,
            'estimated_read_time': read_time,
            'tags': tags
        }

    @classmethod
    def enhance_existing_notes(cls, content: str) -> Dict:
        """Enhance existing notes with additional insights"""
        service = cls()
        
        # Generate enhancement
        summary = service._summarize_text(content)
        key_points = service._extract_key_points(content, num_points=7)
        questions = service._generate_questions_from_text(content, num_questions=7)
        
        # Additional insights
        sentences = content.split('.')
        complex_sentences = [s for s in sentences if len(s.split()) > 15]
        
        return {
            'enhanced_summary': summary,
            'key_points': key_points,
            'practice_questions': questions,
            'complex_concepts': complex_sentences[:3],
            'study_tips': [
                'Focus on the key points identified above',
                'Try to answer the practice questions',
                'Review the enhanced summary before exams',
                'Connect these concepts with previous knowledge'
            ]
        }
