from logging import exception
from setuptools import Command
import speech_recognition as sr
import datetime
import subprocess
import pywhatkit
import pyttsx3
import webbrowser

engine = pyttsx3.init()
# voices = engine.getProperty('voices')
speechRate = engine.getProperty('rate')
engine.setProperty('rate', speechRate-10)
# engine.setProperty('voice', voices[2].id)

recognizer = sr.Recognizer()

welcomeNote = 'CO-VISION'
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

        elif 'stop now' in newCommand:
            print('Stopping Now')
            engine.say("Stopping Now")
            engine.runAndWait()
            break

        else:
            engine.say("Can't help you with ")
            engine.say(newCommand)
            engine.runAndWait()

        