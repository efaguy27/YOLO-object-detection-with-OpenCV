#!/usr/bin/env python

# Import required modules
import time
import RPi.GPIO as GPIO


def GPIO_setup():
    # Declare the GPIO settings
    GPIO.setmode(GPIO.BOARD)

    # set up GPIO pins
    GPIO.setup(7, GPIO.OUT) # PWM1
    M1 = GPIO.PWM(7, 1000)    
    GPIO.setup(18, GPIO.OUT) # PWM2
    M2 = GPIO.PWM(18, 1000) 
    
    GPIO.setup(11, GPIO.OUT) # DIR1
    GPIO.setup(15, GPIO.OUT) # DIR2

    return(M1, M2)
    
def foward(M1, M2, t):

    # Set the motor directions
    GPIO.output(11, GPIO.HIGH)

    GPIO.output(15, GPIO.LOW) 

    # Set the motor speeds
    M1.start(50)
    M2.start(50)

    time.sleep(t)
    
    M1.stop()
    M2.stop()
    
def turn_left(M1, M2, t):

    # Set the motor directions
    GPIO.output(11, GPIO.HIGH) 
    GPIO.output(15, GPIO.HIGH) 

    # Set the motor speeds
    M1.start(50)
    M2.start(50)

    time.sleep(t)
    
    M1.stop()
    M2.stop()
    
def turn_right(M1, M2, t):

    # Set the motor directions
    GPIO.output(11, GPIO.LOW)
    GPIO.output(15, GPIO.LOW) 

    # Set the motor speeds
    M1.start(50)
    M2.start(50)
    time.sleep(t)
    
    M1.stop()
    M2.stop()


def GPIO_clean():
    # Reset all the GPIO pins by setting them to LOW
    GPIO.output(11, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    GPIO.output(18, GPIO.LOW) 

    GPIO.cleanup() # cleanup all GPIO
    
