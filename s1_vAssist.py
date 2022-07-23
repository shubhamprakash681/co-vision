from logging import exception
from setuptools import Command
import speech_recognition as sr
import datetime
import subprocess
import pywhatkit
import pyttsx3
import webbrowser
import wikipedia
import os

engine = pyttsx3.init()
# voices = engine.getProperty('voices')
speechRate = engine.getProperty('rate')
engine.setProperty('rate', speechRate-25)
# engine.setProperty('voice', voices[2].id)

recognizer = sr.Recognizer()

hour = int(datetime.datetime.now().hour)
greet = ""
if hour>=0 and hour<12:
    greet = "Good Morning"

elif hour>=12 and hour<18:
    greet = "Good Afternoon"

else:
    greet = "Good Evening"
    
welcomeNote = 'CO-VISION'
engine.say(greet)
engine.say(welcomeNote)
engine.runAndWait()


while True:
    with sr.Microphone() as source:
        print('Removing Background Noises..Wait....')
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        a = 'Ask me now'
        engine.say(a)
        engine.runAndWait()
        print(a)
        recordedAudio = recognizer.listen(source)
        try:
            newCommand = " "
            newCommand = recognizer.recognize_google(recordedAudio)
            newCommand=newCommand.lower()
            print('Your message:',format(newCommand))

        except Exception as exc:
            print(exc)

        if 'time' in newCommand:
            currentTime = datetime.datetime.now().strftime('%I : %M %p')
            print(currentTime)
            engine.say('The time is ')
            engine.say(currentTime)
            engine.runAndWait()

        elif 'date' in newCommand:
            currentDate = datetime.date.today().strftime("%B %d, %Y")
            print("Today's date:", currentDate)
            engine.say("Today's date is ")
            engine.say(currentDate)
            engine.runAndWait()
            
        elif 'wikipedia' in newCommand:
            engine.say('Searching Wikipedia...')
            newCommand = newCommand.replace("wikipedia", "")
            results = wikipedia.summary(newCommand, sentences=2)
            engine.say("According to Wikipedia")
            print(results)
            engine.say(results)
            engine.runAndWait()
            
        elif 'location' in newCommand:
            engine.say('Running Location Share...')
            engine.runAndWait()
            os.system('python s6_locGoogle.py')

        elif 'ocr' in newCommand:
            msg = "Running Text Recognizer"
            print(msg)
            engine.say(msg)
            engine.runAndWait()
            os.system('python s2_capTextRecog.py')

        elif 'mask' in newCommand:
            msg = "Running Face Mask Detector"
            print(msg)
            engine.say(msg)
            engine.runAndWait()
            os.system('python s3_face_mask_recognition.py')

        elif 'face record' in newCommand:
            msg = "Running Face Recognizer"
            print(msg)
            engine.say(msg)
            engine.runAndWait()
            os.system('python s4_faceRecognition.py')

        elif 'object' in newCommand:
            msg = "Running Object Recognizer"
            print(msg)
            engine.say(msg)
            engine.runAndWait()
            os.system('python s5_capObjectDetector.py')
            
        #elif 'stick' in newCommand:
        #    msg = "Activating Your Smart Stick"
        #    print(msg)
        #    engine.say(msg)
        #    engine.runAndWait()
        #    os.system('python s7_stick.py')
            
        elif 'stick ir' in newCommand:
            msg = "Activating Your Smart Stick"
            print(msg)
            engine.say(msg)
            engine.runAndWait()
            os.system('python s8_stickIR.py')

        elif 'stop now' in newCommand:
            print('Stopping Now')
            engine.say("Stopping Now")
            engine.runAndWait()
            break
            
        elif 'reboot now' in newCommand:
            print('Rebooting CO_VISION')
            engine.say("Rebooting CO_VISION")
            engine.runAndWait()
            os.system('sudo reboot')
            break
            
        elif 'shutdown now' in newCommand:
            print('Shuting Downn CO_VISION')
            engine.say("Shuting Downn CO_VISION")
            engine.runAndWait()
            os.system('sudo shutdown -h now')
            break

        else:
            engine.say("Can't help you with ")
            engine.say(newCommand)
            engine.runAndWait()

        
