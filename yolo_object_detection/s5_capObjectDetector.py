import cv2 as cv
import numpy as np
import time

# load yolo
net = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')
classes = []
with open('coco.names', 'r') as f:
    for line in f.readlines():
        classes.append(line.strip())

layer_names = net.getLayerNames()

output_layers = []
for i in net.getUnconnectedOutLayers():
    output_layers.append(layer_names[i - 1])

# assigning unique color to each object in classes[]  --->  to draw rectangle of the unique color
colors = np.random.uniform(0, 255, size=(len(classes), 3))
my_font = cv.FONT_HERSHEY_PLAIN  # font used

# loading video
video = cv.VideoCapture(0)

start_time = time.time()
frame_id = 0
while True:
    _, frame = video.read()
    frame_id += 1

    height, width, channel = frame.shape

    blob = cv.dnn.blobFromImage(frame, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
    # reduced size to increase FPS

    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes = []
    confidences = []
    distances = []
    class_ids = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # object detected here
                # detecting details of the detected object
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - (w / 2))
                y = int(center_y - (h / 2))
                # Distance measuring in Inch
                distance = (2 * 3.14 * 180) / (w + h * 360) * 1000 + 3
                distances.append(distance)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # printing details of the detected objects
    # print(len(boxes))
    indexes = cv.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)
    # function to tine the object detection
    # change values of score_threshold, nms_threshold, if getting multiple detection of same object
    # or if any object is not detected properly
    # print(indexes)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])

            color = colors[class_ids[i]]
            distance = distances[i] * 2.54
            cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv.putText(frame, (label + "  " + str(round(distance, 2)) + 'cm'), (x, y + 20), my_font, 2, color, 3)

    elapsed_time = time.time() - start_time
    fps = frame_id / elapsed_time
    cv.putText(frame, ('FPS: ' + str(round(fps, 2))), (10, 20), my_font, 1, (0, 0, 255), 1)
    cv.imshow('VIDEO FRAME', frame)
    keyPressed = cv.waitKey(1)
    if keyPressed == ord('q'):
        break

video.release()
cv.destroyAllWindows()
