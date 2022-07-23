import numpy as np
import os
import cv2 as cv

##########Voice Output######
import pyttsx3
engine = pyttsx3.init()
speechRate = engine.getProperty('rate')
engine.setProperty('rate', speechRate + 30)

engine.say("Face Recognizer Launched")
engine.say("Wait while model is loading")
engine.runAndWait()
##########Voice Output######

baseFolder = '/home/shubham/co_vision/faceRecognition/'
peopleDIR = os.path.join(baseFolder, 'Faces/', 'train')

# reading haar_face
haar_cascade = cv.CascadeClassifier(os.path.join(baseFolder, 'haar_face.xml'))
# DIR = '/home/shubham/co_vision/faceRecognition/Faces/train'
people = []
for i in os.listdir(peopleDIR):
    people.append(i)
people.append('Unknown')

features = np.load(os.path.join(baseFolder, 'features.npy'), allow_pickle=True)
labels = np.load(os.path.join(baseFolder, 'labels.npy'))

face_recognizer = cv.face.LBPHFaceRecognizer_create()       #to initiate the face recognizer
face_recognizer.read(os.path.join(baseFolder, 'face_trained.yml'))

engine.say("Model loaded successfully")
engine.runAndWait()
engine.setProperty('rate', speechRate + 50)

video = cv.VideoCapture(0)
while True:
    ret, frame = video.read()
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('Person', gray_frame)
    personsDetected = []    ##list to store result for audio op

    # Detect faces in a each frame
    faces_rect = haar_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=4)
    for (x,y,w,h) in faces_rect:
        faces_roi = gray_frame[y:y+h, x:x+w]      #cropping

        label, confidence = face_recognizer.predict(faces_roi)
        
        if confidence < 60:
            label = -1
            confidence = 100 - confidence
        
        personsDetected.append(str(people[label]))
        print(f'Label= {people[label]} with a confidence= {confidence} ')
        cv.putText(frame, str(people[label]), (x-20, y-20), cv.FONT_HERSHEY_SIMPLEX, 1.1, (0,255,0), 2)
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

    cv.imshow('Detected Face', frame)
    
    engine.say(personsDetected)
    engine.runAndWait()
    
    keyPressed = cv.waitKey(1)
    if keyPressed == ord('q'):
        break
        
video.release()
cv.destroyAllWindows()
