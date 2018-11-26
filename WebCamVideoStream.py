import cv2

class WebCamVideoStream:
	def __init__(self):
		self.cap = cv2.VideoCapture(0)
		
	def getFrame(self):
		ret,frame = self.cap.read()
		return frame

	def reset(self):
		return

	def close(self):
		self.cap.release()
		return
