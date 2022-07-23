import cv2 as cv
import numpy as np
import time

# Distance constants 
KNOWN_DISTANCE = 45 #INCHES
PERSON_WIDTH = 16 #INCHES
MOBILE_WIDTH = 3.0 #INCHES

# Object detector constant 
CONFIDENCE_THRESHOLD = 0.4
NMS_THRESHOLD = 0.3


categories = []
with open('coco.names', 'r') as f:
    for line in f.readlines():
        categories.append(line.strip())
# print(categories)

# load yolo
net = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')

net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

model = cv.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

# assigning unique color to each object in categories[]  --->  to draw rectangle of the unique color
colors = np.random.uniform(0, 255, size=(len(categories), 3))
my_font = cv.FONT_HERSHEY_PLAIN  # font used

# functions()


# loading video
video = cv.VideoCapture(0)
start_time = time.time()
frame_id = 0
while True:
    ret, frame = video.read()

    # object_detector
    classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    # creating empty list to add objects data
    data_list =[]
    for (classid, score, box) in zip(classes, scores, boxes):
        # print(classid, score, box)
        # define color of each, object based on its class id 
        color= colors[int(classid) % len(colors)]
    
        label = "%s : %f" % (categories[classid[0]], score)

        # draw rectangle on and label on object
        cv.rectangle(frame, box, color, 2)
        cv.putText(frame, label, (box[0], box[1]-14), my_font, 0.5, color, 2)

        

    cv.imshow('frame',frame)
    
    key = cv.waitKey(1)
    if key ==ord('q'):
        break

video.release()
cv.destroyAllWindows()
