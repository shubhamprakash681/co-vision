import os
import cv2 as cv
import numpy as np

# reading haar_face
haar_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# training
DIR = '/11LenDrive/11Drive/myCodes/openCv_computerVision/face_mask_detector/images'
# print(os.listdir(DIR))

types = []
for i in os.listdir(DIR):
    types.append(i)
print(types)

# # training set
features = []
labels = []

def create_train():
    for model_type in types:
        path = os.path.join(DIR, model_type)
        label = types.index(model_type)
        for img in os.listdir(path):
            img_path = os.path.join(path, img)

            img_array = cv.imread(img_path)
            gray_img = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            faces_rect = haar_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=4)

            for (x,y,w,h) in faces_rect:
                faces_roi = gray_img[y:y+h, x:x+w]  #cropping face from whole image
                features.append(faces_roi)
                labels.append(label)


create_train()      #running the function
print(f'Length of features[] = {len(features)}')
print(f'Length of labels[] = {len(labels)}')
print(f'------------TRAINING DONE------------')

face_recognizer = cv.face.LBPHFaceRecognizer_create()       #to initiate the face recognizer

# #trainnimg the recognizer on the features list and the labels list
features = np.array(features, dtype='object')       #converting to numpy arrays
labels = np.array(labels)
face_recognizer.train(features, labels)

# # saving the trained model
np.save('features.npy', features)
np.save('labels.npy', labels)
face_recognizer.save('face_mask_trained.yml')