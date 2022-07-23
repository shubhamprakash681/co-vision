import numpy as np
import os
import cv2 as cv

# reading haar_face
haar_cascade = cv.CascadeClassifier('haar_face.xml')
DIR = '/home/shubham/co_vision/faceRecognition/Faces/train'
people = []
for i in os.listdir(DIR):
    people.append(i)
print(people)

features = np.load('features.npy', allow_pickle=True)
labels = np.load('labels.npy')

face_recognizer = cv.face.LBPHFaceRecognizer_create()       #to initiate the face recognizer
face_recognizer.read('face_trained.yml')


img = cv.imread(r'/home/shubham/co_vision/faceRecognition/Faces/val/ben_afflek/2.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Person', gray)

# Detect face in image
faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
for (x,y,w,h) in faces_rect:
    faces_roi = gray[y:y+h, x:x+w]      #cropping

    label, confidence = face_recognizer.predict(faces_roi)
    print(f'Label= {people[label]} with a confidence= {confidence} ')
    cv.putText(img, str(people[label]), (20,20), cv.FONT_HERSHEY_SIMPLEX, 1.1, (0,255,0), 2)
    cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

cv.imshow('Detected Face', img)
cv.waitKey(0)
