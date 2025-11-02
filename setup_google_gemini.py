"""
🎯 Quick Setup: Get Your Google Gemini API Key

Follow these steps to get FREE unlimited AI access!
"""

print("=" * 80)
print(" 🚀 GOOGLE GEMINI - FREE API KEY SETUP ".center(80, "="))
print("=" * 80)
print()

print("📝 STEP 1: Get Your API Key")
print("-" * 80)
print("1. Open your browser and go to:")
print("   👉 https://aistudio.google.com/app/apikey")
print()
print("2. Sign in with your Google account (Gmail)")
print()
print("3. Click the blue button: 'Create API Key'")
print()
print("4. Copy the API key (starts with 'AIza...')")
print()

input("Press Enter after you've copied your API key...")

print("\n" + "=" * 80)
print("📝 STEP 2: Add API Key to .env File")
print("-" * 80)
print("1. Open file: evolveedu-ai/backend/.env")
print()
print("2. Find this line:")
print("   GOOGLE_API_KEY=your_google_api_key_here")
print()
print("3. Replace 'your_google_api_key_here' with your copied key:")
print("   GOOGLE_API_KEY=AIza....")
print()
print("4. Save the file")
print()

input("Press Enter after you've updated the .env file...")

print("\n" + "=" * 80)
print("🧪 STEP 3: Test Your Setup")
print("-" * 80)
print()

try:
    import os
    from dotenv import load_dotenv
    import google.generativeai as genai
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key or api_key == 'your_google_api_key_here':
        print("❌ ERROR: API key not found in .env file")
        print("   Please make sure you saved the .env file correctly")
        exit(1)
    
    print(f"✅ API Key found: {api_key[:20]}...")
    print()
    print("🔄 Testing connection to Google Gemini...")
    
    # Configure and test
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    response = model.generate_content("Say 'Hello! Google Gemini is working!' in a friendly way.")
    
    print("✅ SUCCESS! Google Gemini is working!")
    print()
    print("Response from AI:")
    print("-" * 80)
    print(response.text)
    print("-" * 80)
    print()
    print("🎉 SETUP COMPLETE!")
    print()
    print("Your app is now using Google Gemini for FREE!")
    print("- 60 requests per minute")
    print("- Unlimited free tier")
    print("- No credit card required")
    print()
    print("Next step: Restart your Django server")
    print("  cd evolveedu-ai/backend")
    print("  python manage.py runserver")
    
except ImportError as e:
    print("❌ ERROR: Required package not installed")
    print(f"   {e}")
    print()
    print("Run: pip install google-generativeai")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print()
    print("Common issues:")
    print("1. Invalid API key - Make sure you copied it correctly")
    print("2. API key not enabled - Visit https://aistudio.google.com/app/apikey")
    print("3. Internet connection required")

print()
print("=" * 80)
