import ollama
import speech_recognition as sr
import pyttsx3

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust speech speed

# Initialize Speech Recognition
recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Captures speech input and converts it to text."""
    with mic as source:
        print("Listening... (Speak now)")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)  # Increased timeout
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected. Try again.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("Speech Recognition service is down.")
            return None

# Chatbot Loop
while True:
    user_input = listen()
    if user_input:
        if user_input.lower() == "exit":
            speak("Goodbye!")
            print("Chatbot: Goodbye!")
            break
        response = ollama.chat(model="llama2", messages=[{"role": "user", "content": user_input}])
        print("Chatbot:", response['message']['content'])
        speak(response['message']['content'])