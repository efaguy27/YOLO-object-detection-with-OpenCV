#!/usr/bin/env python

# Import required modules
import time
import RPi.GPIO as GPIO

import detection

def GPIO_setup():
    # Declare the GPIO settings
    GPIO.setmode(GPIO.BOARD)

    # set up GPIO pins
    GPIO.setup(7, GPIO.OUT) # Connected to PWMA
    MA = GPIO.PWM(7, 100)    
    GPIO.setup(18, GPIO.OUT) # Connected to PWMB
    MB = GPIO.PWM(18, 100) 
    
    GPIO.setup(11, GPIO.OUT) # Connected to DIRA
    GPIO.setup(15, GPIO.OUT) # Connected to DIRB

    return(MA, MB)
def backward(MA, MB):
    # Drive the robot foward
    # Motor A:
    GPIO.output(11, GPIO.LOW) # Set AIN2
    # Motor B:
    GPIO.output(15, GPIO.HIGH) # Set BIN1

    # Set the motor speed
    # Motor A:
    MA.start(50)
    # Motor B:
    MB.start(50)

    # Wait 1 seconds
    time.sleep(1)
    
    # Motor A:
    MA.stop()
    # Motor B:
    MB.stop()
    
def foward(MA, MB, t):

    # Drive the robot backward
    # Motor A:
    GPIO.output(11, GPIO.HIGH) # Set AIN2
    # Motor B:
    GPIO.output(15, GPIO.LOW) # Set BIN1

    # Set the motor speed
    # Motor A:
    MA.start(50)
    # Motor B:
    MB.start(50)

    # Wait 1 seconds
    time.sleep(t)
    
    # Motor A:
    MA.stop()
    # Motor B:
    MB.stop()
    
def turn_left(MA, MB, t):

     # Drive the robot backward
    # Motor A:
    GPIO.output(11, GPIO.HIGH) # Set AIN2
    # Motor B:
    GPIO.output(15, GPIO.HIGH) # Set BIN1

    # Set the motor speed
    # Motor A:
    MA.start(45)
    # Motor B:
    MB.start(45)

    # Wait 1 seconds
    time.sleep(t)
    
    # Motor A:
    MA.stop()
    # Motor B:
    MB.stop()
    
def turn_right(MA, MB, t):

     # Drive the robot backward
    # Motor A:
    GPIO.output(11, GPIO.LOW) # Set AIN2
    # Motor B:
    GPIO.output(15, GPIO.LOW) # Set BIN1

    # Set the motor speed
    # Motor A:
    MA.start(60)
    # Motor B:
    MB.start(60)

    # Wait 1 seconds
    time.sleep(t)
    
    # Motor A:
    MA.stop()
    # Motor B:
    MB.stop()


def GPIO_clean():
    # Reset all the GPIO pins by setting them to LOW
    GPIO.output(11, GPIO.LOW) # Set AIN2
    GPIO.output(7, GPIO.LOW) # Set PWMA
    GPIO.output(15, GPIO.LOW) # Set BIN1
    GPIO.output(18, GPIO.LOW) # Set PWMB

    GPIO.cleanup() # cleanup all GPIO
    
if __name__ == '__main__':
    (MA, MB) = GPIO_setup()
    #(object_found, pos_result, size_result) = detection.detect_func(0)
    turn_right(MA, MB, 1.7)
    time.sleep(0.5)
    foward(MA, MB, 1)
    time.sleep(0.5)
    turn_left(MA, MB, 1.5)
    #(object_found, pos_result, size_result) = detection.detect_func(1)
    time.sleep(30)
   
    turn_right(MA, MB, 0.3)
    foward(MA, MB, 2)
    time.sleep(31)
    turn_left(MA,MB,0.3)
    foward(MA,MB, 0.4)
    

    #time.sleep(32)
    
    #turn_right(MA, MB, 1.6)
    GPIO_clean()
