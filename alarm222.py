import time
import cv2
import mediapipe as mp
import numpy as np
import pygame  # For playing alarm
import pyttsx3
from scipy.spatial import distance
import os

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def play_alarm(sound_file):
    """Function to play an alarm sound"""
    print("\n⏰ Alarm ringing! Press ENTER to stop. ⏰")

    if not os.path.exists(sound_file):
        print("❌ Error: Audio file not found!")
        speak("Error. Audio file not found.")
        return

    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play(-1)  # Loop indefinitely

    input("\nPress ENTER to stop the alarm...")
    pygame.mixer.music.stop()
    print("✅ Alarm stopped.")

# First, play the alarm
play_alarm("alarm.mp3")  # Replace with your alarm sound file

print("\n🚀 Starting face detection now...")

# Define eye landmarks
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(eye):
    """Calculate Eye Aspect Ratio (EAR)"""
    if len(eye) != 6:
        return 1.0  # High EAR prevents false positives
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3]) + 1e-6  # Avoid division by zero
    return (A + B) / (2.0 * C)

# Sleep detection parameters
EAR_THRESHOLD = 0.25  # Below this, eyes are considered closed
CLOSED_DURATION = 10  # How long eyes need to be closed to trigger alarm (seconds)
SCAN_DURATION = 10  # Total scan duration before stopping detection

# Start webcam
cap = cv2.VideoCapture(0)
start_time = time.time()
close_start_time = None
awake = True
face_detected = False

def elapsed_time():
    return time.time() - start_time

while elapsed_time() < SCAN_DURATION:
    ret, frame = cap.read()
    if not ret:
        break
    
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    
    if results.multi_face_landmarks and not face_detected:
        face_detected = True
        print("✅ Face detected")

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye = np.array([(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in LEFT_EYE])
            right_eye = np.array([(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in RIGHT_EYE])
            
            left_EAR = eye_aspect_ratio(left_eye)
            right_EAR = eye_aspect_ratio(right_eye)
            avg_EAR = (left_EAR + right_EAR) / 2.0
            
            # Display EAR values on screen
            cv2.putText(frame, f"EAR: {avg_EAR:.2f}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            # Draw eye landmarks
            cv2.polylines(frame, [left_eye], isClosed=True, color=(0, 255, 0), thickness=1)
            cv2.polylines(frame, [right_eye], isClosed=True, color=(0, 255, 0), thickness=1)
            
            # Check if eyes are closed for the required duration
            if avg_EAR < EAR_THRESHOLD:
                if close_start_time is None:
                    close_start_time = time.time()
                elif time.time() - close_start_time >= CLOSED_DURATION:
                    cv2.putText(frame, "⚠ SLEEP DETECTED! ⚠", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    print("⚠ Sleep detected! Triggering alarm...")
                    awake = False
            else:
                close_start_time = None  # Reset timer if eyes open
                if not awake:
                    print("✅ Awake again")
                    awake = True
    
    # Show video feed
    cv2.imshow("Sleep Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# If the person was asleep, ring the alarm again
if not awake:
    print("\n⏳ Alarm will ring again in 10 seconds...\n")
    time.sleep(5)
    print("⚠️ Alarm will ring in 5 seconds! ⚠️")
    time.sleep(5)
    play_alarm("alarm.mp3")  # Replace with your own music file
else:
    print("✅ You stayed awake! No alarm needed.")
    speak("You are awake.")
