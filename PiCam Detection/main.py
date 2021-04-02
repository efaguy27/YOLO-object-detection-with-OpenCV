#!/usr/bin/env python
import drive
import detection
import time

(MA, MB) = drive.GPIO_setup()
    

#test = detection.detect_func()
#print(test)


drive.turn_left(MA, MB)
time.sleep(0.5)
drive.backward(MA, MB)
#test = detection.detect_func()
#print(test)

drive.GPIO_clean()
