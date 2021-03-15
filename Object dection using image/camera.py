from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.resolution = (640, 360)
camera.start_preview()
sleep(2)
camera.capture('/home/pi/41xx/YOLO-object-detection-with-OpenCV/Object dection using image/images/test.jpg')
camera.stop_preview()