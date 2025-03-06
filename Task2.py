import webbrowser
import random
import pyttsx3
import pyautogui
import time
import speech_recognition as sr
import pygetwindow as gw
import ctypes

# Check if script is running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("⚠️ Please run this script as an administrator for best results!")

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# List of YouTube motivational videos
videos = [
    "https://www.youtube.com/watch?v=-hVHeP-1hGc",
    "https://www.youtube.com/watch?v=RkaCnfJZXT4",
    "https://www.youtube.com/watch?v=QkCa--fyGjA",
    "https://www.youtube.com/watch?v=e-z9qSCOfFE",
    "https://www.youtube.com/watch?v=IKZtj-5LNeo"
]

# Pick a random video and announce it
random_video = random.choice(videos)
message = "Starting your day with motivation. Here is a video for you."
print(message)
engine.say(message)
engine.runAndWait()

# Open the video
webbrowser.open(random_video)
time.sleep(5)  # Allow browser to open

def bring_browser_to_front():
    """Try bringing YouTube to the front. Uses pygetwindow, then Alt+Tab fallback."""
    print("Attempting to bring YouTube window to front...")
    time.sleep(2)
    
    # Find the YouTube window (modify this if needed)
    browser_windows = [w for w in gw.getAllTitles() if "YouTube" in w]

    if browser_windows:
        window = gw.getWindowsWithTitle(browser_windows[0])[0]
        if window.isMinimized:  # Restore if minimized
            window.restore()
            time.sleep(1)

        try:
            window.activate()  # Try activating window
            time.sleep(1)
            print("YouTube window activated.")
        except:
            print("⚠️ Could not activate YouTube window. Using Alt+Tab as fallback.")
            pyautogui.hotkey("alt", "tab")  # Fallback to Alt+Tab
            time.sleep(1)
    else:
        print("⚠️ YouTube window not found. Try clicking on it manually.")
        pyautogui.hotkey("alt", "tab")  # Try switching manually

def listen_for_command():
    """Listen for voice commands and control YouTube playback."""
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("🎤 Listening... Say 'stop', 'play', or 'exit'.")
            recognizer.adjust_for_ambient_noise(source)

            try:
                command = recognizer.recognize_google(recognizer.listen(source, timeout=7)).lower()
                print(f"You said: {command}")

                if "stop" in command or "pause" in command:
                    bring_browser_to_front()
                    time.sleep(0.5)  # Ensure focus before key press
                    pyautogui.press("space")
                    print("⏸ Video Paused!")

                elif "play" in command:
                    bring_browser_to_front()
                    time.sleep(0.5)
                    pyautogui.press("space")
                    print("▶ Video Resumed!")

                elif "exit" in command:
                    print("🛑 Exiting voice control...")
                    return False

            except sr.UnknownValueError:
                print("🤷 Could not understand. Try again.")
            except sr.RequestError:
                print("⚠️ Speech recognition service unavailable. Check internet connection.")

    return True

# Voice control loop
while listen_for_command():
    pass
