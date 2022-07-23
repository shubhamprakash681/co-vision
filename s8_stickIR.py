import RPi.GPIO as IO
import time
IO.setwarnings(False)
IO.setmode(IO.BCM)

##########Voice Output######
import pyttsx3
engine = pyttsx3.init()
speechRate = engine.getProperty('rate')
engine.setProperty('rate', speechRate+10)
engine.say("Smart Stick Activated")
engine.runAndWait()
##########Voice Output######

IO.setup(2,IO.OUT) #GPIO 2 -> Red LED as output
IO.setup(3,IO.OUT) #GPIO 3 -> Green LED as output
IO.setup(16,IO.IN) #GPIO 14 -> IR sensor as input

while 1:

    if(IO.input(16)==True): #object is far away
        IO.output(2,True) #Red led ON
        IO.output(3,False) # Green led OFF
        print("No Object")
    
    if(IO.input(16)==False): #object is near
        IO.output(3,True) #Green led ON
        IO.output(2,False) # Red led OFF
        print("Object")
        engine.say("Alert")
        engine.runAndWait()


GPIO.cleanup()
