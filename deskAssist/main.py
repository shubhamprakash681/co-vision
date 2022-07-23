import speech_recognition as sr
import datetime
import subprocess
import pywhatkit
import pyttsx3
import webbrowser

import os


engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
recognizer=sr.Recognizer()

def cmd():
    with sr.Microphone() as source:
        print("Clearing background noises...Pleasw wait")
        recognizer.adjust_for_ambient_noise(source,duration=0.5)
        a = 'Ask me anything....'
        engine.say(a)
        engine.runAndWait()
        print(a)
        recordedaudio=recognizer.listen(source)
    try:
        text=recognizer.recognize_google(recordedaudio,language='en_US')
        text=text.lower()
        print('Your message:',format(text))

    except Exception as ex:
        print(ex)
    if 'chrome'in text:
        a='Opening chrome..'
        engine.say(a)
        engine.runAndWait()
        fiPath = "C:\11LenDrive\11Drive\myCodes\openCv_computerVision\yolo_object_detection\main.py"

        # os.system('python hi.py')  # working perfectly
        os.system('python hi.py')  # working perfectly


    if 'time' in text:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        engine.say(time)
        engine.runAndWait()
    # if 'play' in text:
    #     a='opening youtube..'
    #     engine.say(a)
    #     engine.runAndWait()
    #     pywhatkit.playonyt(text)
    # if 'youtube' in text:
    #     b='opening youtube'
    #     engine.say(b)
    #     engine.runAndWait()
    #     webbrowser.open('C:\Program Files\Google\Chrome\Application\hi.py')
while True:
    cmd()


