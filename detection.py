from __future__ import division

from scipy.spatial import distance
from imutils import face_utils
import imutils
from imutils.video import VideoStream
import dlib
global cv2
import cv2
import math
from pyaudio import PyAudio
import argparse

import time
import datetime


def arg_conv(str):
    if str.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif str.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Please enter a boolean value like true or false!')

def isDistracted(frame,drawing = True):
    global eyesNotVisible,flag
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)
    if (len(subjects) == 0):
        eyesNotVisible+=1
        if eyesNotVisible >= framesEyesNotVisible: # Distracted checker
            return True
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
        if args["display"]:
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        if ear < thresh: # Drowsiness Detector
            flag += 1
            if flag >= frame_check:
                return True
        else:
            flag = 0
            return False



ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=arg_conv, default=False,
	help="whether or not the Raspberry Pi camera should be used")

ap.add_argument("-d", "--display", type=arg_conv, default=False,
    help="whether or not to display the image")

ap.add_argument("-a", "--analytics", type=arg_conv, default=False,
    help="whether or not analytics will be tracked")

ap.add_argument("-b", "--debug", type=arg_conv, default=False,
    help="whether or not debugger is active")

ap.add_argument("-s", "--sound", type=arg_conv, default=False,
    help="whether or not sound is active")
args = vars(ap.parse_args())

videoStream = None

if args["sound"]:
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(1), # 8bit
                channels=2, # mono
                rate=22050,
                output=True)

flag = 0
eyesNotVisible = 0
framesEyesNotVisible = 5

frameRate = 0
initial_time = datetime.datetime.now()
""" DETECT CARD NUMBER FOR AUDIO
for i in range (p.get_device_count()):
	dev=p.get_device_info_by_index(i)
	print((i,dev['name'],dev['maxInputChannels']))
"""


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

eyesNotVisible = 0

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]


VideoStream = None
if args['picamera']:
    from PiCameraVideoStream import PiCameraVideoStream
    VideoStream = PiCameraVideoStream()
else:
    isRaspberryPi = 0
    from WebCamVideoStream import WebCamVideoStream
    VideoStream = WebCamVideoStream()

while (True):
    frame = VideoStream.getFrame()
    frameRate+=1
    time = (datetime.datetime.now() - initial_time).total_seconds()
    print(frameRate/time)

    frame = imutils.resize(frame, width=450)
    distracted= isDistracted(frame)

    if distracted:
        if args["sound"]:
            play_sound()
        if args["display"]:
            cv2.putText(frame, "****************DISTRACTED!****************", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "****************DISTRACTED!****************", (10,325),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if (args["display"]):
        cv2.imshow("Frame", frame)
    
    VideoStream.reset()

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
    	break

#stream.stop_stream()
#stream.close()
VideoStream.close()

cv2.destroyAllWindows()

