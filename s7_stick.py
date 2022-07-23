import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

##########Voice Output######
import pyttsx3
engine = pyttsx3.init()
speechRate = engine.getProperty('rate')
engine.setProperty('rate', speechRate-10)
engine.say("Smart Stick Activated")
engine.runAndWait()
##########Voice Output######

TRIG = 23 
ECHO = 24
BUZZ = 25

GPIO.setup(BUZZ,GPIO.OUT)
GPIO.output(BUZZ, False)
while 1:
    print ("Distance Measurement In Progress")
    
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    
    GPIO.output(TRIG, False)
    print ("Waiting For Sensor To Settle")
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print ("Distance:",distance,"cm")
    #if distance <= 10:
    #    GPIO.output(BUZZ, True)
    #    engine.say("Alert")
    #    engine.runAndWait()
    #    time.sleep(2)
    #else:
    #    GPIO.output(BUZZ, False)
    
    
GPIO.cleanup()
