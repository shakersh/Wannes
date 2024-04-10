from picamera2 import Picamera2
import cv2
piCam = Picamera2()
piCam.preview_configuration.main.size = (480, 360)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()
# body_classifier = cv2.CascadeClassifier('resources/haarcascade_fullbody.xml')
faces_classifier1 = cv2.CascadeClassifier('resources/haarcascade_frontalface_alt.xml')
upper_classifier = cv2.CascadeClassifier('resources/haarcascade_upperbody.xml')

while True:
	frame = piCam.capture_array()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# bodies = body_classifier.detectMultiScale(gray, 1.05, 3)
	faces1 = faces_classifier1.detectMultiScale(gray, 1.05, 3)
	upper = upper_classifier.detectMultiScale(gray, 1.05, 3)
	
	# Extract bounding boxes for any bodies identified
	# for (x, y, w, h) in bodies:
		# cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # yellow
		
	for (x, y, w, h) in faces1:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (102, 0, 255), 2)  # pink
		print(faces1)

	for (x, y, w, h) in upper:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 247, 0), 2)  # cyan
		
	cv2.imshow('img', frame)
	if cv2.waitKey(30) & 0xff == 27:
		break
