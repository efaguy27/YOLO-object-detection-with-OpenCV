import numpy as np
import argparse
import time
import cv2
import os
from picamera import PiCamera
from time import sleep
import glob
x=0
y=800
w=1866
h= 450

image = cv2.imread("fake.jpg")
color = [156,21,112]
cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
text = "{}: {:.4f}".format('bowl', 0.5436)
cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, color, 2)
cv2.imwrite(f'Image.png', image)