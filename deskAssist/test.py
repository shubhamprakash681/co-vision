from logging import exception
from numpy import rate
from setuptools import Command
import speech_recognition as sr
import datetime
import subprocess
import pywhatkit
import pyttsx3
import webbrowser

engine = pyttsx3.init()
voices = engine.getProperty('voices')
currrentrate = engine.getProperty('rate')
engine.setProperty('rate', currrentrate+50)
for voice in voices:
    print(voice, voice.id)
    engine.say('Hello World!')
    engine.runAndWait()
engine.stop()