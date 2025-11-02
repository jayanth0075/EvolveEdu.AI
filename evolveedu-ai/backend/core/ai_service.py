"""
Unified AI Service supporting multiple providers
Supports: OpenAI, GitHub Models (Copilot), Google Gemini
"""

import os
import logging
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class UnifiedAIService:
    """
    Unified AI service supporting multiple providers:
    - Google Gemini (FREE, unlimited)
    - GitHub Models (FREE with Copilot subscription)
    - OpenAI (standard API)
    """
    
    def __init__(self):
        self.provider = os.getenv('AI_PROVIDER', 'google').lower()
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate AI client based on provider"""
        try:
            if self.provider == 'google':
                self._initialize_google()
            
            elif self.provider == 'github':
                # GitHub Models - FREE with Copilot
                github_token = os.getenv('GITHUB_TOKEN')
                if not github_token or github_token == 'your_github_token_here':
                    logger.warning("GitHub token not configured, falling back to Google Gemini")
                    self._initialize_google()
                else:
                    from openai import OpenAI
                    self.client = OpenAI(
                        base_url="https://models.inference.ai.azure.com",
                        api_key=github_token
                    )
                    self.model = os.getenv('GITHUB_MODEL', 'gpt-4o-mini')
                    logger.info(f"✅ GitHub Models initialized with {self.model}")
            
            elif self.provider == 'openai':
                self._initialize_openai()
            
            else:
                logger.warning(f"Unknown provider: {self.provider}, falling back to Google Gemini")
                self._initialize_google()
        
        except Exception as e:
            logger.error(f"Error initializing {self.provider}: {e}")
            # Final fallback to Google Gemini
            try:
                self._initialize_google()
            except:
                self._initialize_openai()
    
    def _initialize_google(self):
        """Initialize Google Gemini client"""
        try:
            import google.generativeai as genai
            
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key or api_key == 'your_google_api_key_here':
                logger.warning("Google API key not configured, falling back to OpenAI")
                self._initialize_openai()
                return
            
            genai.configure(api_key=api_key)
            self.model = os.getenv('GOOGLE_MODEL', 'gemini-1.5-flash')
            self.client = genai.GenerativeModel(self.model)
            self.provider = 'google'
            logger.info(f"✅ Google Gemini initialized with {self.model}")
        except ImportError:
            logger.error("google-generativeai not installed. Run: pip install google-generativeai")
            self._initialize_openai()
        except Exception as e:
            logger.error(f"Error initializing Google Gemini: {e}")
            self._initialize_openai()
    
    def _initialize_openai(self):
        """Initialize OpenAI client"""
        from openai import OpenAI
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("No AI provider configured properly. Please add API keys to .env")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.provider = 'openai'
        logger.info(f"✅ OpenAI initialized with {self.model}")
    
    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text completion using the configured AI provider
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0-1)
        
        Returns:
            Generated text response
        """
        try:
            if self.provider == 'google':
                return self._generate_google(prompt, system_prompt, max_tokens, temperature)
            elif self.provider in ['openai', 'github']:
                return self._generate_openai_compatible(prompt, system_prompt, max_tokens, temperature, **kwargs)
            else:
                raise Exception(f"Unknown provider: {self.provider}")
        
        except Exception as e:
            logger.error(f"Error generating completion with {self.provider}: {e}")
            raise Exception(f"AI generation failed: {str(e)}")
    
    def _generate_google(self, prompt: str, system_prompt: Optional[str], max_tokens: int, temperature: float) -> str:
        """Generate using Google Gemini"""
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        generation_config = {
            "max_output_tokens": max_tokens,
            "temperature": temperature,
        }
        
        # Configure safety settings to be less restrictive for educational content
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        
        response = self.client.generate_content(
            full_prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Handle blocked or empty responses
        try:
            # Check if we have candidates before accessing text
            if not response.candidates:
                logger.warning("No candidates in response")
                return "Unable to generate response. Please try a different prompt."
            
            # Check finish reason
            finish_reason = response.candidates[0].finish_reason
            if finish_reason == 2:  # RECITATION - blocked due to recitation
                logger.warning(f"Response blocked with finish_reason=2 (RECITATION)")
                # Try accessing parts directly
                if response.candidates[0].content.parts:
                    return response.candidates[0].content.parts[0].text.strip()
                return "Response blocked by safety filter. Please rephrase your question."
            
            # Normal response
            if response.text:
                return response.text.strip()
            else:
                logger.warning("Empty response text")
                return "No response generated. Please try again."
                
        except Exception as e:
            logger.error(f"Error accessing response: {e}")
            if response.prompt_feedback:
                return f"Response blocked: {response.prompt_feedback}"
            return "Unable to generate response. Please try a different prompt."
    
    def _generate_openai_compatible(self, prompt: str, system_prompt: Optional[str], max_tokens: int, temperature: float, **kwargs) -> str:
        """Generate using OpenAI or GitHub Models"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )
        
        return response.choices[0].message.content.strip()
    
    def get_provider_info(self) -> Dict[str, str]:
        """Get information about the current AI provider"""
        return {
            "provider": self.provider,
            "model": self.model,
            "status": "active" if self.client else "inactive"
        }


# Global instance
ai_service = UnifiedAIService()


# Convenience functions for backward compatibility
def generate_text(prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
    """Generate text using the unified AI service"""
    return ai_service.generate_completion(prompt, system_prompt, **kwargs)


def get_ai_provider() -> str:
    """Get the current AI provider name"""
    return ai_service.provider
