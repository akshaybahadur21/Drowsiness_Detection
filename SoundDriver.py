from pyaudio import PyAudio
import math

class SoundDriver():
    def __init__(self,eyesNotVisibleTime=2000,frame_check_time=2000):
        self.p = PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(1), # 8bit
                channels=2, # mono
                rate=22050,
                output=True)

    def play_sound(self,frequency=440, duration=0.2, volume=1):
        n_samples = int(22050 * duration)
        restframes = n_samples % 22050
        s = lambda t: volume * math.sin(2 * math.pi * frequency * t / 22050)
        samples = (int(s(t) * 0x7f + 0x80) for t in range(n_samples))
        self.stream.write(bytes(bytearray(samples)))
