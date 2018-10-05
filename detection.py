from __future__ import division

from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2

import math

from pyaudio import PyAudio

p = PyAudio()
stream = p.open(format=p.get_format_from_width(1), # 8bit
                channels=1, # mono
                rate=22050,
                output=True)

def play_sound(frequency=440, duration=0.2, volume=1):
    n_samples = int(22050 * duration)
    restframes = n_samples % 22050
    s = lambda t: volume * math.sin(2 * math.pi * frequency * t / 22050)
    samples = (int(s(t) * 0x7f + 0x80) for t in range(n_samples))
    stream.write(bytes(bytearray(samples)))

def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear

thresh = 0.25
frame_check = 20
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
cap=cv2.VideoCapture(0)
flag = 0
eyesNotVisible = 0
framesEyesNotVisible = 50
while True:
	ret, frame=cap.read()
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	subjects = detect(gray, 0)
	if (len(subjects) == 0):
		eyesNotVisible+=1
		if eyesNotVisible >= framesEyesNotVisible: # Distracted checker
			play_sound()
			cv2.putText(frame, "****************DISTRACTED!****************", (10, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			cv2.putText(frame, "****************DISTRACTED!****************", (10,325),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			play_sound(volume=0)
	else:
		eyesNotVisible = 0
	for subject in subjects:
		shape = predict(gray, subject)
		shape = face_utils.shape_to_np(shape)#converting to NumPy Array
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		ear = (leftEAR + rightEAR) / 2.0
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		if ear < thresh: # Drowsiness Detector
			flag += 1
			#print (flag)
			if flag >= frame_check:
				cv2.putText(frame, "****************ALERT!****************", (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				cv2.putText(frame, "****************ALERT!****************", (10,325),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				#print ("Drowsy")
		else:
			flag = 0
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

stream.stop_stream()
stream.close()
p.terminate()

cv2.destroyAllWindows()
cap.release()
