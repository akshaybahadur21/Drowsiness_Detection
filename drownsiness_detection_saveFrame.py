from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
from moviepy.editor import VideoFileClip
import numpy as np

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

thresh = 0.25
frame_check = 20
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("D:/Judson_projetos/Drownsiness_detector2/Drowsiness_Detection/models/shape_predictor_68_face_landmarks.dat")  # Dat file is the crux of the code

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
flag = 0

def process_frame(frame):
    global flag
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)
    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)  # Converting to NumPy Array
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        if ear < thresh:
            flag += 1
            print(flag)
            if flag >= frame_check:
                cv2.putText(frame, "****************ALERT!****************", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "****************ALERT!****************", (10, 325),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                # print ("Drowsy")
        else:
            flag = 0
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

# Caminho para o vídeo de entrada
input_video_path = 'My video - Data (1).mp4'
# Caminho para o vídeo de saída
output_video_path = 'output_with_detections.mp4'

# Abre o vídeo de entrada com moviepy
clip = VideoFileClip(input_video_path)

# Processa cada frame do vídeo usando a função process_frame
processed_clip = clip.fl_image(process_frame)

# Salva o vídeo processado
processed_clip.write_videofile(output_video_path, codec='libx264')

print("Vídeo salvo com sucesso em", output_video_path)
