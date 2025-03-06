import pyttsx3
import speech_recognition as sr
import json
from datetime import datetime

class TaskAssistant:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
    
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self, prompt="Listening for a command..."):
        with sr.Microphone() as source:
            self.speak(prompt)
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=15, phrase_time_limit=12)  # Increased listening time
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand that.")
                return None
            except sr.RequestError:
                self.speak("Could not request results, please check your internet connection.")
                return None
            except sr.WaitTimeoutError:
                self.speak("No input detected. Please try again.")
                return None
    
    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file, indent=4)
    
    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                tasks = json.load(file)
                for t in tasks:
                    if "added_on" not in t:
                        t["added_on"] = "Unknown"
                return tasks
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def add_task(self, task):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tasks.append({"task": task, "completed": False, "added_on": timestamp})
        self.save_tasks()
        message = f"Task added: {task} at {timestamp}"
        print(message)
        self.speak(message)
    
    def remove_task(self, task):
        for t in self.tasks:
            if t["task"] == task:
                self.tasks.remove(t)
                self.save_tasks()
                message = f"Task removed: {task}"
                print(message)
                self.speak(message)
                return
        self.speak("Task not found.")
        print("Task not found.")
    
    def mark_complete(self, task):
        for t in self.tasks:
            if t["task"] == task:
                t["completed"] = True
                self.save_tasks()
                message = f"Task completed: {task}"
                print(message)
                self.speak(message)
                return
        self.speak("Task not found.")
        print("Task not found.")
    
    def show_tasks(self):
        self.tasks = self.load_tasks()  # Ensure the latest data is loaded before displaying
        if not self.tasks:
            self.speak("No tasks in the watchlist.")
            print("No tasks in the watchlist.")
        else:
            print("\nTask Watchlist:")
            self.speak("Here is your task watchlist.")
            for idx, t in enumerate(self.tasks, 1):
                status = "completed" if t["completed"] else "pending"
                added_on = t.get("added_on", "Unknown")
                message = f"Task {idx}: {t['task']} is {status}, added on {added_on}."
                print(f"{idx}. {t['task']} [{status}] (Added: {added_on})")
                self.speak(message)

# Example usage
if __name__ == "__main__":
    assistant = TaskAssistant()
    while True:
        command = assistant.listen()
        
        if command:
            if command.startswith("add task"):
                task = command.replace("add task", "").strip()
                if not task:
                    assistant.speak("Please specify the task to add.")
                    task = assistant.listen("What task would you like to add?")
                if task:
                    assistant.add_task(task)
            elif command.startswith("remove task"):
                task = command.replace("remove task", "").strip()
                if task:
                    assistant.remove_task(task)
                else:
                    assistant.speak("Please specify a task to remove.")
                    print("No task provided.")
            elif command.startswith("complete task"):
                task = command.replace("complete task", "").strip()
                if task:
                    assistant.mark_complete(task)
                else:
                    assistant.speak("Please specify a task to mark as complete.")
                    print("No task provided.")
            elif "show task" in command or "display my task" in command:
                assistant.show_tasks()
            elif "exit" in command or "quit" in command:
                assistant.speak("Goodbye!")
                break
            else:
                assistant.speak("Sorry, I didn't understand the command.")