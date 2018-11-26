FRAMES = 10
class detector():
    def __init__(self,eyesNotVisibleTime=FRAMES,frame_check_time=FRAMES):
        import dlib
        import cv2
        from scipy.spatial import distance
        from imutils import face_utils
        import time

        self.eyesNotVisible = 0
        self.flag = 0
        self.tEyesNotVisible = eyesNotVisibleTime
        self.tFrame_check_time = frame_check_time

        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
        (self.rStart,self.rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

        self.thresh = 0.25
        self.frame_check = 20
        self.detect = dlib.get_frontal_face_detector()
        self.predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


    def eye_aspect_ratio(self,eye):
        from scipy.spatial import distance
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def isDistracted(self,frame,drawing):
        import cv2
        import dlib
        from imutils import face_utils

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = self.detect(gray, 0)
        if (len(subjects) == 0):
            self.eyesNotVisible+=1
            if self.eyesNotVisible >= self.tEyesNotVisible: # Distracted checker
                return True
        else:
            self.eyesNotVisible = 0
        return False

    def display_warnings(self,frame):
        import cv2
        cv2.putText(frame, "****************DISTRACTED!****************", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "****************DISTRACTED!****************", (10,325),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    def show(self,frame):
        import cv2
        cv2.imshow("Frame", frame)
