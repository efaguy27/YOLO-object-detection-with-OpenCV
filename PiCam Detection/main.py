#!/usr/bin/env python
import drive
import detection
import time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--size", required=True,
	help="length of area being searched in meters")
ap.add_argument("-o", "--object", required=True,
	help="label of object being searched for")    #cup, fork, knife, spoon, bowl are the supported objects
    
if (args['object'] == 'bowl'):
    object_size = 350000
elif (args['object'] == 'cup'):
    object_size = 450000
elif (args['object'] == 'fork' || args['object'] == 'knife' || args['object'] == 'spoon'):
    object_size = 200000
else:
    print("Invalid object entered\n")
    quit()
    
area_searched = 0
 
(M1, M2) = drive.GPIO_setup()
detection_count = 1
(object_found, pos_result, size_result) = detection.detect_func(args['object'], 0)

while (1):
    if (object_found == False): 
        #Check if entire area has been searched
        if (area_searched >= args['size']):
            print("Entire area searched, no objects found\n")
            break
            
        #Nothing found. Move to next search location
        drive.turn_right(M1, M2, 1.5) #Turn right 90 degrees
        time.sleep(0.5)
        drive.foward(M1, M2, 1) # Move foward 0.22 meters
        area_searched = area_searched + 0.22
        time.sleep(0.5)
        drive.turn_left(M1, M2, 1.5) #Turn left 90 degrees

    elif (size_result > object_size):
        print(f'Done, {object_found} found in {detection_count} detections\n')
        break
    elif (abs(pos_result) < 200): #Directly ahead move forward
        rel_size = object_size/size_result
        drive.foward(M1, M2, (rel_size/2.5))

    elif (pos_result > 0): #Offcentre right, turn right and move foward
        rel_pos = pos_result-200
        rel_size = object_size/size_result
        drive.turn_right(M1, M2, rel_pos/1000)
        drive.foward(M1, M2, (rel_size/2.5))

    elif (pos_result < 0): #Offcentre left, turn left and move foward
        rel_pos = abs(pos_result)-200
        rel_size = object_size/size_result
        drive.turn_left(M1, M2, rel_pos/1000)
        drive.foward(M1, M2, (rel_size/2.5))
        
    (object_found, pos_result, size_result) = detection.detect_func(args['object'], detection_count)
    detection_count = detection_count + 1    

drive.GPIO_clean()
