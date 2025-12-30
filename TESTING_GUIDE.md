# Testing Guide for AI-JanSahayak

## 🧪 Pre-Demo Testing Checklist

### Test 1: Microphone Detection
```bash
python -c "import speech_recognition as sr; print('Microphone:', sr.Microphone.list_microphone_names())"
```
**Expected:** List of available microphones

---

### Test 2: API Key Validation
1. Open `jan_sahayak.py`
2. Verify `GOOGLE_API_KEY` is set correctly
3. Run: `python jan_sahayak.py`
4. **Expected:** No "ERROR: Please set your Google API key"

---

### Test 3: Speech Recognition Test
```python
import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something in Hindi or English...")
    audio = recognizer.listen(source)
    
try:
    text = recognizer.recognize_google(audio, language='hi-IN')
    print(f"You said: {text}")
except Exception as e:
    print(f"Error: {e}")
```
**Expected:** Your speech transcribed correctly

---

### Test 4: TTS Test
```python
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io

text = "Namaste, main test kar raha hoon"
tts = gTTS(text=text, lang='hi')
fp = io.BytesIO()
tts.write_to_fp(fp)
fp.seek(0)
song = AudioSegment.from_file(fp, format="mp3")
play(song)
```
**Expected:** Hindi voice saying the text

---

### Test 5: Gemini API Test
```python
import google.generativeai as genai

GOOGLE_API_KEY = "YOUR_KEY_HERE"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Say 'Namaste' in Hindi")
print(response.text)
```
**Expected:** Gemini responds with "Namaste" or similar

---

### Test 6: Full System Test
```bash
python jan_sahayak.py
```

**Test Dialogue:**
1. Wait for greeting
2. Say: "Hello test"
3. **Expected:** AI responds in Hinglish
4. Say: "bye"
5. **Expected:** Graceful exit

---

### Test 7: Complaint Saving Test
1. Run application
2. Say: "Mere ghar me paani nahi aa raha hai"
3. Provide ward info when asked
4. Exit application
5. Check if `complaints_db.json` exists
6. Open file and verify complaint is saved
**Expected:** JSON file with your complaint

---

### Test 8: Empathy Detection Test
Say these angry phrases:
- "Bahut bekaar service hai"
- "Koi kaam nahi karta"
- "Worst system hai"

**Expected:** AI starts response with "Maafi chaahte hain"

---

## 🎯 Demo Scenarios

### Scenario 1: Happy Path
**User:** "Mere area me streetlight kharab hai"
**Expected Flow:**
1. AI asks for location
2. User provides ward/area
3. Complaint registered
4. Complaint ID returned

### Scenario 2: Angry User
**User:** "Bahut problem ho rahi hai, paani band hai teen din se"
**Expected Flow:**
1. AI detects anger
2. Starts with "Maafi chaahte hain"
3. Proceeds with registration

### Scenario 3: Hinglish Mix
**User:** "My road is broken, kab thik karenge?"
**Expected Flow:**
1. AI understands mixed language
2. Responds in Hinglish
3. Registers complaint

---

## 🔍 Error Scenarios to Test

### Error 1: No Microphone
**Trigger:** Disconnect microphone
**Expected:** "⚠️ Could not understand audio"

### Error 2: No Internet
**Trigger:** Disconnect WiFi
**Expected:** "⚠️ Speech recognition error" or "⚠️ Error communicating with Gemini"

### Error 3: Background Noise
**Trigger:** Play loud music while speaking
**Expected:** May transcribe incorrectly, but shouldn't crash

### Error 4: Long Silence
**Trigger:** Don't speak for 5+ seconds
**Expected:** "⚠️ No speech detected. Please try again."

---

## 📊 Performance Benchmarks

Track these metrics during testing:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Response Time | < 3 sec | Time from speech end to AI speech start |
| Transcription Accuracy | > 90% | Compare spoken vs transcribed |
| TTS Quality | Clear | Subjective listening test |
| Memory Usage | < 500 MB | Task Manager during operation |
| Database Write | < 100 ms | Time to save complaint |

---

## 🐛 Common Issues & Fixes

### Issue: PyAudio installation fails on Windows
```bash
pip install pipwin
pipwin install pyaudio
```

### Issue: FFmpeg not found
**Fix:**
1. Download FFmpeg: https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to PATH
4. Restart terminal

### Issue: Microphone not working in Python
**Fix:**
- Run as Administrator
- Check Windows Privacy Settings → Microphone
- Grant Python microphone permissions

### Issue: "Could not understand audio" every time
**Fix:**
- Reduce background noise
- Speak closer to microphone
- Speak slower and clearer
- Check microphone volume in Windows settings

### Issue: TTS sounds robotic
**Fix:**
- This is expected for free TTS
- gTTS has limited naturalness
- For better quality, consider Azure TTS (paid)

---

## 🎤 Voice Testing Tips

### Good Practices
- Speak at normal conversational speed
- Use natural sentences, not robotic commands
- Mix Hindi and English naturally
- Speak 6-12 inches from microphone

### Bad Practices
- Don't shout
- Don't whisper
- Don't speak too fast
- Don't use complex technical terms

---

## 📹 Recording Backup Demo Video

### Equipment Setup
- Use good internet connection
- Close all other applications
- Use external microphone if available
- Test audio levels before recording

### Recording Steps
1. Start screen recording (OBS/Windows Game Bar)
2. Run `python jan_sahayak.py`
3. Have scripted conversation ready
4. Speak clearly with pauses
5. Show `complaints_db.json` at end
6. Stop recording

### Video Checklist
- [ ] Audio is clear
- [ ] Terminal text is readable
- [ ] AI responses are audible
- [ ] Complaint ID is visible
- [ ] Duration < 2 minutes
- [ ] No background noise

---

## 🏆 Final Pre-Demo Checklist

**1 Day Before:**
- [ ] Test full flow 5 times
- [ ] Record backup video
- [ ] Prepare presentation slides
- [ ] Charge laptop fully

**1 Hour Before:**
- [ ] Test microphone
- [ ] Check internet speed
- [ ] Connect Bluetooth speaker
- [ ] Have backup video ready
- [ ] Close unnecessary apps

**On Stage:**
- [ ] Run application before presenting
- [ ] Have complaints_db.json open in another window
- [ ] Keep calm if something fails
- [ ] Switch to backup video if needed

---

## 📈 Success Metrics

Your demo is successful if:
1. ✅ AI greets in Hinglish
2. ✅ Understands your Hindi/English speech
3. ✅ Detects angry tone (if you test it)
4. ✅ Registers complaint successfully
5. ✅ Shows complaint ID
6. ✅ Saves to database file

**Even one successful end-to-end conversation is enough to impress judges!**

---

## 🎯 Testing Priority

**Must Test (Critical):**
1. Basic speech recognition
2. AI response generation
3. Complaint saving
4. Graceful exit

**Should Test (Important):**
5. Empathy detection
6. Hinglish mixing
7. Error handling

**Nice to Test (Optional):**
8. Performance under load
9. Long conversations
10. Edge cases

---

Good luck with your testing! 🚀

**Remember:** A well-tested demo is a winning demo!
