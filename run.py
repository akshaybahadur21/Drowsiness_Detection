import subprocess
import time
import argparse

proc = None
moving = True


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

while moving:
    if moving and proc is None:
        proc = subprocess.Popen(['python3', 'detection.py', '-p', str(isRaspberryPi)])
        time.sleep(20) # remove this line -- used for debugging
        moving = False
    elif not moving and not proc is None:
        proc.terminate()
        proc = None
        moving = False

