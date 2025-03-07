import webbrowser
import pyttsx3
import random
import os
import time

def open_youtube_video(video_url):
    """Opens a YouTube video in the default web browser and speaks the action."""
    engine = pyttsx3.init()
    engine.say("Here is an informative and brain puzzling video for you")
    engine.runAndWait()
    webbrowser.open(video_url)

def stop_youtube_video():
    """Stops the YouTube video by closing the browser tab (not precise but closes the browser)."""
    engine = pyttsx3.init()
    engine.say("Stopping YouTube video")
    engine.runAndWait()
    os.system("taskkill /IM chrome.exe /F")  # WARNING: This closes all Chrome windows!

def choose_random_video():
    """Selects a random YouTube video and opens it."""
    videos = [
        "https://youtu.be/isdLel273rQ?si=yP0LNvpEeuNXvTOA",
        "https://youtu.be/fa8k8IQ1_X0?si=Y1dXDIDi2zbGaVnt",
        "https://youtu.be/bgo7rm5Maqg?si=zZXR0Pq6vPP5HYoE",
        "https://youtu.be/BmUZ2wp1lM8?si=cj2v4g84zoNShU2I"
    ]
    choice = random.choice(videos)
    print(f"Selected video: {choice}")
    open_youtube_video(choice)
    
    time.sleep(10)  # Wait for 10 seconds before stopping the video
    stop_youtube_video()

# Example usage
choose_random_video()
