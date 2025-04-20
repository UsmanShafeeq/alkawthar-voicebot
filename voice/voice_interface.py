import speech_recognition as sr
import pyttsx3
import time
from threading import Thread

class VoiceInterface:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_listening = False
        
        # Configure voice engine
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Change index for different voice
        self.engine.setProperty('rate', 150)  # Speed percent

    def speak(self, text):
        """Convert text to speech"""
        print(f"Bot: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen to microphone and convert speech to text"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=5)
            
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Please try again.")
            return None
        except sr.RequestError:
            self.speak("Sorry, my speech service is down. Please try again later.")
            return None

    def continuous_listen(self, callback):
        """Continuously listen for commands"""
        self.is_listening = True
        while self.is_listening:
            query = self.listen()
            if query:
                callback(query)
            time.sleep(1)

    def start_continuous_listen(self, callback):
        """Start continuous listening in a separate thread"""
        Thread(target=self.continuous_listen, args=(callback,), daemon=True).start()

    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False