import cv2 as cv
import os, shutil
import pytesseract as pt

path = '/home/shubham/co_vision/text_recognition/images/'
# pt.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

# video = cv.VideoCapture(0, cv.CAP_DSHOW)
video = cv.VideoCapture(0)
count = 0
while True:
    ret, frame = video.read()
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    cv.imshow("VIDEO FRAME", frame)

    keyPressed = cv.waitKey(1)
    if keyPressed == ord('c'):
        cv.imwrite(os.path.join(path, 'Frame' + str(count) + '.jpg'), frame)
        count += 1
    elif keyPressed == ord('q'):
        break

video.release()
cv.destroyAllWindows()

# img = cv.imread('bkpImg/img1.png')
imgName = os.path.join(path, 'Frame' + str(count-1) + '.jpg')
print(imgName)
img = cv.imread(imgName)
cv.imshow('Last Image', img)

# preprocessing method
resized = cv.resize(img, (720, 560), interpolation=cv.INTER_CUBIC)
gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)

# decrease block-size(2nd last param) to reduce noise
# increase block-size to increase accuracy
adaptive_threshold = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 85, 11)
text1 = pt.image_to_string(adaptive_threshold)
# print(text1)
cv.imshow('Adaptive Threshold Img', adaptive_threshold)

# OCR settings method
config = "--psm 1"
text2 = pt.image_to_string(adaptive_threshold, config=config)
print(text2)
cv.waitKey(0)


# deleting all captured images when program ends
for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
