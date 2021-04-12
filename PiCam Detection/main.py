#!/usr/bin/env python
import drive
import detection
import time

(MA, MB) = drive.GPIO_setup()
    
found = False

#object_size = 0
(object_found, pos_result, size_result) = detection.detect_func()
print(pos_result)
print(size_result)

while (1):
    if (object_found == None):
        if (found == True):
            print("Lost object\n")
            break
        print("Nothing found. Moving down\n")
        
        drive.turn_right(MA, MB, 1.6)
        time.sleep(0.5)
        drive.foward(MA, MB, 1)
        time.sleep(0.5)
        drive.turn_left(MA, MB, 1.45)
    
        (object_found, pos_result, size_result) = detection.detect_func()
        if (object_found != None):
            found = True
            #if (object_found == 'bowl'):
             #   object_size = 350000
            #elif (object_found == 'cup'):
             #   object_size = 
        print(pos_result)
        print(size_result)
    elif (size_result > 350000):
        print('Done')
        break
    elif (abs(pos_result) < 200):
        rel_size = 850000/size_result
        drive.foward(MA, MB, (rel_size/7))
        (object_found, pos_result, size_result) = detection.detect_func()
        print(pos_result)
        print(size_result)
    elif (pos_result > 0):
        print("Offcentre right\n")
        rel_pos = pos_result-200
        rel_size = 850000/size_result
        drive.turn_right(MA, MB, rel_pos/1000)
        drive.foward(MA, MB, (rel_size/7))
        (object_found, pos_result, size_result) = detection.detect_func()
        print(pos_result)
        print(size_result)
    elif (pos_result < 0):
        print("Offcentre left\n")
        rel_pos = abs(pos_result)-200
        rel_size = 850000/size_result
        drive.turn_left(MA, MB, rel_pos/1000)
        drive.foward(MA, MB, (rel_size/7))
        (object_found, pos_result, size_result) = detection.detect_func()
        print(pos_result)
        print(size_result)
        

drive.GPIO_clean()
