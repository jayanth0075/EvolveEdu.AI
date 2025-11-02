import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
provider = os.getenv('AI_PROVIDER')
model_name = os.getenv('GOOGLE_MODEL')

print(f"AI_PROVIDER: {provider}")
print(f"GOOGLE_API_KEY: {api_key[:30] if api_key else 'NOT FOUND'}...")
print(f"GOOGLE_MODEL: {model_name}")
print()

if api_key and api_key != 'your_google_api_key_here':
    print("✅ Testing Google Gemini...")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    
    # Configure safety settings
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    response = model.generate_content(
        "Explain what is machine learning in 2 sentences",
        safety_settings=safety_settings
    )
    
    print(f"✅ SUCCESS!\n\nAI Response:\n{response.text}")
    print("\n🎉 Your EvolveEdu.AI app is ready to use Google Gemini!")
else:
    print("❌ Google API key not found or not configured")
