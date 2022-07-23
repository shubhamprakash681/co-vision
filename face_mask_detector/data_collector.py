import cv2 as cv

video=cv.VideoCapture(0)

facedetect=cv.CascadeClassifier('haarcascade_frontalface_default.xml')

count=0

while True:
	ret,frame=video.read()
	gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	faces=facedetect.detectMultiScale(gray_frame,1.1, 3)
	for x,y,w,h in faces:
		count=count+1
		name='./images/face_without_mask/'+ str(count) + '.jpg'
		print("Creating Images........." +name)
		cv.imwrite(name, frame[y:y+h,x:x+w])
		cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
	cv.imshow("VIDEO FRAME", frame)
	cv.waitKey(1)
	if count>500:
		break
video.release()
cv.destroyAllWindows()