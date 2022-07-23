import serial              
from time import sleep
import sys
import webbrowser
import smtplib

##########Voice Output######
import pyttsx3
engine = pyttsx3.init()
speechRate = engine.getProperty('rate')
engine.setProperty('rate', speechRate-10)

engine.say("Location Share Launched")
engine.runAndWait()
##########Voice Output######

port="/dev/ttyAMA0"
ser = serial.Serial (port)
gpgga_info = "$GPGGA,"
GPGGA_buffer = 0
NMEA_buff = 0
GPGGA_data_available = ""

def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

received_data = (str)(ser.read(200)) #read NMEA string received
GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string
if (GPGGA_data_available>0):
    GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after “$GPGGA,” string
    NMEA_buff = (GPGGA_buffer.split(','))
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]
    print("NMEA Time: ", nmea_time,'\n')
    lat = (float)(nmea_latitude)
    lat = convert_to_degrees(lat)
    longi = (float)(nmea_longitude)
    longi = convert_to_degrees(longi)
    print ("NMEA Latitude:", lat,"NMEA Longitude:", longi,'\n')
    map_link = 'http://maps.google.com/?q=' + lat + ',' + longi
    print(map_link)
    #webbrowser.open(map_link)
    
    ###Email sending###
    # list of email_id to send the mail
    mail_list = ['shubhamprakash681@gmail.com', 'shubhamprakash444@ug.cusat.ac.in', 'sameer.smiley123@gmail.com', 'gautamanand30@gmail.com', 'istevefaisal@gmail.com', 'khanshimaila18@gmail.com']

    from cred import psk

    for dest in mail_list:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("covisionteam@gmail.com", psk)
        message = 'Hi There! \n My Current Location is: ' + lat + ',' + longi + '\n Click the link below to get my current location on map: \n https://maps.google.com/?q=' + lat + ',' + longi + '\nThanks.'
        print(message)
        s.sendmail("covisionteam@gmail.com", dest, message)
        s.quit()
    ###Email sending###
    
engine.say("Location Sent")
engine.runAndWait()
sys.exit(0)
