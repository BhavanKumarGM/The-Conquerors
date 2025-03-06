import pyttsx3
import speech_recognition as sr
import json

class TaskAssistant:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
    
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        with sr.Microphone() as source:
            self.speak("Listening for a command...")
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand that.")
                return None
            except sr.RequestError:
                self.speak("Could not request results, please check your internet connection.")
                return None
    
    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file)
    
    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def add_task(self, task):
        self.tasks.append({"task": task, "completed": False})
        self.save_tasks()
        message = f"Task added: {task}"
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
        if not self.tasks:
            self.speak("No tasks in the watchlist.")
            print("No tasks in the watchlist.")
        else:
            print("\nTask Watchlist:")
            self.speak("Here is your task watchlist.")
            for idx, t in enumerate(self.tasks, 1):
                status = "completed" if t["completed"] else "pending"
                message = f"Task {idx}: {t['task']} is {status}."
                print(f"{idx}. {t['task']} [{status}]")
                self.speak(message)

# Example usage
if __name__ == "__main__":
    assistant = TaskAssistant()
    while True:
        command = assistant.listen()
        
        if command:
            if "add task" in command:
                task = command.replace("add task", "").strip()
                if task:
                    assistant.add_task(task)
                else:
                    assistant.speak("Please specify a task to add.")
            elif "remove task" in command:
                task = command.replace("remove task", "").strip()
                if task:
                    assistant.remove_task(task)
                else:
                    assistant.speak("Please specify a task to remove.")
            elif "complete task" in command:
                task = command.replace("complete task", "").strip()
                if task:
                    assistant.mark_complete(task)
                else:
                    assistant.speak("Please specify a task to mark as complete.")
            elif "show task" in command or "display my tasks" in command:
                assistant.show_tasks()
            elif "exit" in command or "quit" in command:
                assistant.speak("Goodbye!")
                break
            else:
                assistant.speak("Sorry, I didn't understand the command.")