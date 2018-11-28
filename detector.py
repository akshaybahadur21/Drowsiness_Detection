# import dlib
import cv2
from scipy.spatial import distance
from imutils import face_utils
import time

FRAMES = 10

class Detector():
    def __init__(self, eyesNotVisibleTime=FRAMES, frame_check_time=FRAMES):
        self.eyesNotVisible = 0
        self.flag = 0
        self.tEyesNotVisible = eyesNotVisibleTime
        self.tFrame_check_time = frame_check_time

        self.thresh = 0.25
        self.frame_check = 20
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    def isDistracted(self, frame, drawing):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = self.eye_cascade.detectMultiScale(gray)
        if len(eyes) > 1:
            self.eyesNotVisible = 0
        else:
            self.eyesNotVisible+=1
            # print(self.eyesNotVisible)
            if self.eyesNotVisible >= self.tEyesNotVisible: # Distracted checker
                print("DISTRACTED")
                return True
        return False

    def display_warnings(self, frame):
        cv2.putText(frame, "****************DISTRACTED!****************", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "****************DISTRACTED!****************", (10,325),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    def show(self, frame):
        cv2.imshow("Frame", frame)
