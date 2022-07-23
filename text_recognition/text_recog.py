import cv2 as cv
import numpy as np
import pytesseract as pt

pt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = cv.imread('bkpImg/img1.png')
resized = cv.resize(img, (720,560), interpolation=cv.INTER_CUBIC)
# to improve accuracy, two methods:
# 1. image preprocessing, 2.OCR settings adjustment

# preprocessing method
gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
# decrease block-size(2nd last param) to reduce noise
# increase block-size to increase accuracy
adaptive_threshold = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 85, 11)
text1 = pt.image_to_string(adaptive_threshold)
# print(text1)
cv.imshow('Adaptive Threshold Img', adaptive_threshold)

# OCR settings method
config="--psm 1"
text2 = pt.image_to_string(adaptive_threshold, config=config)
print(text2)
cv.waitKey(0)
