#!/usr/bin/env python

# Import required modules
import time
import RPi.GPIO as GPIO

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
    
def foward(MA, MB):

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
    time.sleep(1)
    
    # Motor A:
    MA.stop()
    # Motor B:
    MB.stop()
    
def turn_left(MA, MB):

     # Drive the robot backward
    # Motor A:
    GPIO.output(11, GPIO.HIGH) # Set AIN2
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
    
def turn_right(MA, MB):

     # Drive the robot backward
    # Motor A:
    GPIO.output(11, GPIO.LOW) # Set AIN2
    # Motor B:
    GPIO.output(15, GPIO.LOW) # Set BIN1

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


def GPIO_clean():
    # Reset all the GPIO pins by setting them to LOW
    GPIO.output(11, GPIO.LOW) # Set AIN2
    GPIO.output(7, GPIO.LOW) # Set PWMA
    GPIO.output(15, GPIO.LOW) # Set BIN1
    GPIO.output(18, GPIO.LOW) # Set PWMB

    GPIO.cleanup() # cleanup all GPIO
    
if __name__ == '__main__':
    (MA, MB) = GPIO_setup()
    foward(MA, MB)
    time.sleep(1)
    turn_right(MA, MB)
    time.sleep(1)
    backward(MA, MB)
    time.sleep(1)
    turn_left(MA, MB)
    GPIO_clean()
