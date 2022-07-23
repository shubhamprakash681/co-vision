import cv2 as cv
import numpy as np

# load yolo
net = cv.dnn.readNet('yolov3.weights', 'yolov3.cfg')
classes = []
with open('coco.names', 'r') as f:
    for line in f.readlines():
        classes.append(line.strip())
# print(classes)
layer_names = net.getLayerNames()
# output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
# --> this was working before opencv-python releases 55 (3.4.15.55)
output_layers = []
for i in net.getUnconnectedOutLayers():
    output_layers.append(layer_names[i-1])
print(output_layers)

# assigning unique color to each object in classes[]  --->  to draw rectangle of the unique color
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# loading images
img = cv.imread('room_ser.jpg')
img = cv.resize(img, None, fx=0.4,  fy=0.4)

height, width, channel = img.shape

# detecting object
# blob conversion
# --> YOLO can process only blob of the image
blob = cv.dnn.blobFromImage(img, scalefactor=0.00392, size=(416, 416), mean=(0, 0, 0), swapRB=True, crop=False)

# for b in blob:
#     for n, img_blob in enumerate(b):
#         cv.imshow(str(n), img_blob)

net.setInput(blob)
outs = net.forward(output_layers)
# print(outs)

# showing informations on the screen
boxes = []
confidences = []
distances = []
class_ids = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # object detected here
            # detecting details of the detected object
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - (w/2))
            y = int(center_y - (h/2))
            # Distance measuring in Inch
            distance = (2 * 3.14 * 180) / (w + h * 360) * 1000 + 3
            distances.append(distance)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# printing details of the detected objects
print(len(boxes))
indexes = cv.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)
# function to tine the object detection
# change values of score_threshold, nms_threshold, if getting multiple detection of same object
# or if any object is not detected properly
print(indexes)

for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        # print(label)
        color = colors[class_ids[i]]
        distance = distances[i] * 2.54
        cv.rectangle(img, (x, y), (x+w, y+h), color, 2)
        cv.putText(img, (label + "  " + str(round(distance, 2)) + 'cm'), (x, y+20), cv.FONT_HERSHEY_PLAIN, 2, color, 3)

cv.imshow('Image', img)
cv.waitKey(0)
cv.destroyAllWindows()
