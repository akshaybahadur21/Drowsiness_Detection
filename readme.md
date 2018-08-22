# Drowsiness Detection OpenCV [![](https://img.shields.io/github/license/sourcerer-io/hall-of-fame.svg?colorB=ff0000)](https://github.com/akshaybahadur21/Drowsiness_Detection/blob/master/LICENSE.txt)  [![](https://img.shields.io/badge/Akshay-Bahadur-brightgreen.svg?colorB=ff0000)](https://akshaybahadur.com)
This code can detect your eyes and alert when the user is drowsy.

### Sourcerer
[![](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/images/0)](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/links/0)[![](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/images/1)](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/links/1)[![](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/images/2)](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/links/2)[![](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/images/3)](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/links/3)[![](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/images/4)](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/links/4)[![](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/images/5)](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/links/5)[![](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/images/6)](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/links/6)[![](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/images/7)](https://sourcerer.io/fame/akshaybahadur21/akshaybahadur21/Drowsiness_Detection/links/7)

## Applications
This can be used by riders who tend to drive for a longer period of time that may lead to accidents


### Code Requirements
The example code is in Python ([version 2.7](https://www.python.org/download/releases/2.7/) or higher will work). 

### Dependencies

1) import cv2
2) import immutils
3) import dlib
4) import scipy


### Description

A computer vision system that can automatically detect driver drowsiness in a real-time video stream and then play an alarm if the driver appears to be drowsy.

### Algorithm

Each eye is represented by 6 (x, y)-coordinates, starting at the left-corner of the eye (as if you were looking at the person), and then working clockwise around the eye:.

<img src="https://github.com/akshaybahadur21/Drowsiness_Detection/blob/master/eye1.jpg">

### Condition

It checks 20 consecutive frames and if the Eye Aspect ratio is lesst than 0.25, Alert is generated.

#### Relationship

<img src="https://github.com/akshaybahadur21/Drowsiness_Detection/blob/master/eye2.png">

#### Summing up

<img src="https://github.com/akshaybahadur21/Drowsiness_Detection/blob/master/eye3.jpg">


For more information, [see](https://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv/)

### Working Example

<img src="https://github.com/akshaybahadur21/Drowsiness_Detection/blob/master/drowsy.gif">



### Execution
To run the code, type `python Drowsiness_Detection.py`

```
python Drowsiness_Detection.py
```
