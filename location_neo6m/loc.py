import serial              
from time import sleep
import sys

port="/dev/ttyAMA0"
ser = serial.Serial (port)
try:
    while True:
        received_data = (str)(ser.readline()) #read NMEA string received
        print(received_data)
except KeyboardInterrupt:
    sys.exit(0)  