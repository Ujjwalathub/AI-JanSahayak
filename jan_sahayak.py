"""
AI-JanSahayak Version 2.0: Hybrid Voice-First Grievance Redressal System
A dual-mode (Voice OR Text) AI agent for Delhi Government citizen services
Supports Hinglish (Hindi + English) for accessibility in any environment
"""

import os
import time
import json
import pygame
import speech_recognition as sr
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv
from datetime import datetime
import tempfile

# --- CONFIGURATION ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("❌ ERROR: GOOGLE_API_KEY not found. Check .env file.")
    exit()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')

DB_FILE = "complaints_db.json"
pygame.mixer.init()

# --- THE BRAIN (SYSTEM PROMPT) ---
SYSTEM_INSTRUCTION = """
You are 'AI-JanSahayak', a government assistant. 
1. INPUT: You will receive text (typed or transcribed voice).
2. OUTPUT: Reply in natural 'Hinglish' (Hindi + English mix).
3. TONE: Professional but empathetic. If user complains about basic needs (water/light), apologize first.
4. GOAL: Summarize the complaint in 1 sentence.
"""

chat = model.start_chat(history=[
    {"role": "user", "parts": [SYSTEM_INSTRUCTION]},
    {"role": "model", "parts": ["Ji namaste, main Jan Sahayak hoon. Bataiye kya shikayat hai?"]}
])

# --- HELPER FUNCTIONS ---

def save_to_db(user_text, ai_reply):
    """Saves the interaction to a JSON database"""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f: json.dump([], f)
    
    with open(DB_FILE, 'r') as f: db = json.load(f)

    entry = {
        "id": f"DEL-{int(time.time())}",
        "time": datetime.now().strftime("%H:%M:%S"),
        "user_input": user_text,
        "ai_response": ai_reply
    }
    db.append(entry)
    with open(DB_FILE, 'w') as f: json.dump(db, f, indent=4)
    return entry['id']

def speak(text):
    """The Mouth: Plays audio response"""
    print(f"🤖 AI: {text}")
    try:
        tts = gTTS(text=text, lang='hi', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_name = fp.name
            tts.save(temp_name)
        
        pygame.mixer.music.load(temp_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.music.unload()
        os.remove(temp_name)
    except Exception as e:
        print(f"❌ Audio Error: {e}")

def get_user_input():
    """The Dual-Mode Input Gate"""
    print("\n" + "="*40)
    print("  SELECT INPUT MODE:")
    print("  [1] 🎤 Press ENTER to Speak")
    print("  [2] ⌨️  Type 'T' to Text Chat")
    print("="*40)
    
    choice = input("👉 Selection: ").strip().lower()

    if choice == 't':
        return input("\n⌨️  Type here: ")
    
    # Voice Mode
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🔊 Calibrating Noise... (Quiet please)")
        r.adjust_for_ambient_noise(source, duration=1)
        print("🔴 LISTENING NOW... (Speak!)")
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("⏳ Processing...")
            text = r.recognize_google(audio, language="en-IN") # en-IN captures Hinglish best
            print(f"👤 You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("❌ No speech detected.")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

# --- MAIN LOOP ---
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🇮🇳 AI-JAN SAHAYAK STARTED")
    speak("Namaste! Main Delhi Jan Sahayak hoon.")

    while True:
        user_text = get_user_input()

        if not user_text:
            continue
            
        if user_text.lower() in ['exit', 'quit', 'stop']:
            speak("Dhanyavaad. Jai Hind.")
            break

        # Get AI Response
        try:
            response = chat.send_message(user_text)
            reply = response.text
            speak(reply)
            
            # Save Record
            cid = save_to_db(user_text, reply)
            print(f"✅ Saved Complaint ID: {cid}")
            
        except Exception as e:
            print(f"⚠️ Network Error: {e}")

if __name__ == "__main__":
    main()
