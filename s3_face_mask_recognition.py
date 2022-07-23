import numpy as np
import os
import cv2 as cv

##########Voice Output######
import pyttsx3
engine = pyttsx3.init()
speechRate = engine.getProperty('rate')
engine.setProperty('rate', speechRate + 50)

engine.say("Face Mask Detector Launched")
engine.runAndWait()

with_mask_count = 0
without_mask_count = 0
##########Voice Output######


baseFolder = '/home/shubham/co_vision/face_mask_detector/'
DIR = os.path.join(baseFolder, 'images')

# reading haar_face
haar_cascade = cv.CascadeClassifier(os.path.join(baseFolder, 'haarcascade_frontalface_default.xml'))

types = []
for i in os.listdir(DIR):
    types.append(i)
print(types)

features = np.load((os.path.join(baseFolder, 'features.npy')), allow_pickle=True)
labels = np.load((os.path.join(baseFolder, 'labels.npy')))

face_recognizer = cv.face.LBPHFaceRecognizer_create()       #to initiate the face recognizer
face_recognizer.read(os.path.join(baseFolder, 'face_mask_trained.yml'))

video = cv.VideoCapture(0)
while True:
    with_mask_count = 0
    without_mask_count = 0
    
    ret, frame = video.read()
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # # Detect face in image
    faces_rect = haar_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=3)
    for x,y,w,h in faces_rect:
        cv.rectangle(frame, (x,y), (x+w, y+h), (255,255,255), 2)
        faces_roi = gray_frame[y:y+h, x:x+w]      #cropping
        label, confidence = face_recognizer.predict(faces_roi)
        print(f'Label= {types[label]} with a confidence= {confidence} ')
        
        if label == 0:
            label = 1
        elif label == 1:
            label = 0

        if label == 1:
            cv.putText(frame, str(types[label]), (x, y-25), cv.FONT_HERSHEY_TRIPLEX, 1.0, (0,0,255), 2)
            without_mask_count += 1
        else:
            cv.putText(frame, str(types[label]), (x, y-25), cv.FONT_HERSHEY_TRIPLEX, 1.0, (0,255,0), 2)
            with_mask_count += 1

    cv.imshow("VIDEO FRAME", frame)
    
    if (with_mask_count > 0):
        engine.say("With Mask" + str(with_mask_count))
    if (without_mask_count > 0):
        engine.say("Without Mask" + str(without_mask_count))
    engine.runAndWait()

    keyPressed = cv.waitKey(1)
    if keyPressed == ord('q'):
        break
video.release()
cv.destroyAllWindows()
