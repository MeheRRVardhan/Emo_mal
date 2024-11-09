import threading
import subprocess
from pynput import keyboard
import joblib
import time
import pyautogui

# Initialize an empty string to store keystrokes
string_empty = ""

# Load the model from the pickle file
pipe_lr = joblib.load(open("C:\\Users\\meher\\OneDrive\\Desktop\\LOGGER\\emotion_classifier_pipe_lr_2.pkl", "rb"))

# Function to predict emotion based on collected keystrokes
def predict_emotion(text):
    return pipe_lr.predict([text])[0]

# Function to handle keystrokes
def on_press(key):
    global string_empty
    try:
        string_empty += str(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            string_empty += " "
        else:
            string_empty += " " + str(key) + " "

# Function to process keystrokes every 30 seconds
def report():
    global string_empty
    data = string_empty
    string_empty = ""  # Reset keystroke string after capturing it

    # Predict and display the emotion based on the keystrokes
    if data.strip():  # Avoid empty predictions
        emotion = predict_emotion(data)
        print(f"Keystrokes: {data}\nPredicted Emotion: {emotion}")
        
        # Wait for a short period to ensure output is seen, then clear Notepad content
        time.sleep(2)  # Adjust this delay if needed
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'x')
        data1 = "not "
        for i in range(len(data1)):
            pyautogui.press(data1[i])
        pyautogui.hotkey('ctrl', 'v')



    # Schedule the next report
    timer = threading.Timer(10, report)
    timer.start()

# Start the keyboard listener and periodic keystroke reporting
with keyboard.Listener(on_press=on_press) as listener:
    report()
    listener.join()
