import pyttsx3
import webbrowser

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

answer = input("Do you know how to play chess? (yes/no/watch): ").strip().lower()

if answer == "yes":
    response = "Great! Let's play."
    webbrowser.open("https://www.chess.com/play/computer")
elif answer == "no":
    response = "No worries! You can learn from this video."
    speak(response)
    webbrowser.open("https://youtu.be/OCSbzArwB10?si=OCUfM-tsvIzcpCCD")  # Chess tutorial video
elif answer == "watch":
    response = "Here are some great chess games to watch."
    speak(response)
    webbrowser.open("https://www.youtube.com/watch?v=L2cbT3elGl8")  # Search for great chess games on YouTube
else:
    response = "Invalid response. Please answer with yes, no, or watch."
print(response)
speak(response)
