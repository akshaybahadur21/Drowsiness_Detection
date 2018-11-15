class PiCameraVideoStream:
	def __init__(self):
		from picamera import PiCamera
		from picamera.array import PiRGBArray
		import time
		self.camera = PiCamera()
		self.camera.framerate=32
		self.camera.resolution=(640,480)
		self.rawCapture = PiRGBArray(self.camera,size=(640,480))
		time.sleep(0.1)
	def getFrame(self):
		for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
			return frame.array
		return None

	def reset(self):
		self.rawCapture.truncate()
		self.rawCapture.seek(0)
		return

	def close(self):
		return

