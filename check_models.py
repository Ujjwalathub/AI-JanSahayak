import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load your API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("🔍 Checking available models for your API Key...")
try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ FOUND: {m.name}")
            available_models.append(m.name)

    if not available_models:
        print("❌ No models found. Check if your API Key is valid.")
except Exception as e:
    print(f"❌ Error: {e}")
