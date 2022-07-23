import numpy as np
import os
import cv2 as cv

# reading haar_face
haar_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

DIR = '/home/shubham/co_vision/face_mask_detector/images'

types = []
for i in os.listdir(DIR):
    types.append(i)
print(types)

features = np.load('features.npy', allow_pickle=True)
labels = np.load('labels.npy')

face_recognizer = cv.face.LBPHFaceRecognizer_create()       #to initiate the face recognizer
face_recognizer.read('face_mask_trained.yml')

video = cv.VideoCapture(0)
while True:
    ret, frame = video.read()
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # # Detect face in image
    faces_rect = haar_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=3)
    for x,y,w,h in faces_rect:
        cv.rectangle(frame, (x,y), (x+w, y+h), (255,255,255), 2)
        faces_roi = gray_frame[y:y+h, x:x+w]      #cropping
        label, confidence = face_recognizer.predict(faces_roi)
        print(f'Label= {types[label]} with a confidence= {confidence} ')

        if label == 0 and confidence < 70.0:
            label = 1

        if label == 1:
            cv.putText(frame, str(types[label]), (x, y-25), cv.FONT_HERSHEY_TRIPLEX, 1.0, (0,0,255), 2)
        else:
            cv.putText(frame, str(types[label]), (x, y-25), cv.FONT_HERSHEY_TRIPLEX, 1.0, (0,255,0), 2)

    cv.imshow("VIDEO FRAME", frame)

    keyPressed = cv.waitKey(1)
    if keyPressed == ord('q'):
        break
video.release()
cv.destroyAllWindows()
