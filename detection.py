from __future__ import division

from scipy.spatial import distance
from imutils import face_utils
import imutils
from imutils.video import VideoStream
import dlib
import cv2
import math
from pyaudio import PyAudio
import argparse

from picamera import PiCamera
from picamera.array import PiRGBArray
import time


def arg_conv(str):
    if str.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif str.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Please enter a boolean value like true or false!')

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=arg_conv, default=False,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
isRaspberryPi = 1 if args['picamera'] else 0

p = PyAudio()
""" DETECT CARD NUMBER FOR AUDIO
for i in range (p.get_device_count()):
	dev=p.get_device_info_by_index(i)
	print((i,dev['name'],dev['maxInputChannels']))
"""
stream = p.open(format=p.get_format_from_width(1), # 8bit
                channels=2, # mono
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

camera=PiCamera()
camera.resolution=(640,480)
camera.framerate=32
rawCapture=PiRGBArray(camera,size=(640,480))
time.sleep(0.1)
flag = 0
eyesNotVisible = 0
framesEyesNotVisible = 50



for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image=frame.array
	play_sound()
	frame = imutils.resize(image, width=450)
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
	rawCapture.truncate()
	rawCapture.seek(0)


	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

#stream.stop_stream()
#stream.close()
p.terminate()

cv2.destroyAllWindows()
cap.stop()

