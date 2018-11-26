from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
camera.framerate=32
camera.resolution=(640,480)

rawCapture = PiRGBArray(camera,size=(640,480))

time.sleep(0.1)

""" Single Shot CAMERA
camera.capture(rawCapture, format = "bgr")
image = rawCapture.array

cv2.imshow("Image",image)
cv2.waitKey(0)
"""

for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    image = frame.array
    cv2.imshow("Frame", image)
    key=cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key==ord("q"):
        break
