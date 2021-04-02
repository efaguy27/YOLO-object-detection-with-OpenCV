#!/usr/bin/env python

import numpy as np
import argparse
import time
import cv2
import os
from picamera import PiCamera
from time import sleep
import glob

def detect_func():
    camera = PiCamera()

    camera.resolution = (640, 360)
    #camera.start_preview()
    sleep(1)
    camera.capture('/home/pi/41xx/YOLO-object-detection-with-OpenCV/PiCam Detection/images/test.jpg')
    print("[INFO] Picture taken")
    camera.close()
    #camera.stop_preview()
    
    labelsPath = '..//yolo-coco//coco.names'
    LABELS = open(labelsPath).read().strip().split("\n")
    weightsPath = '..//yolo-coco//yolov3.weights'
    configPath = '..//yolo-coco//yolov3.cfg'
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    min_confidence = 0.1
    threshold = 0.3
    items = ['cup', 'fork', 'knife', 'spoon', 'bowl']
    
    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
    dtype="uint8")

    # load our input image and grab its spatial dimensions
    image = cv2.imread("images/test.jpg")
    (H, W) = image.shape[:2]

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
        swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    # [,frame,no of detections,[classid,class score,conf,x,y,h,w]
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))
    
    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    files = glob.glob('output//*')
    for f in files:
        os.remove(f)

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > min_confidence:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                if x < 0:
                    x = 0
                if y < 0:
                    y = 0

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence,
        threshold)

    for i in range(len(boxes)):
            if i in idxs:
                direction = []
                x, y, w, h = boxes[i]
                label = str(LABELS[classIDs[i]])
                if (label in items):
                    item = image[y:y+h, x:x+w]
                    if h > image.shape[0]/2:
                        direction.append('center')
                    elif y < image.shape[0]/3:
                        direction.append('top')
                    elif y < image.shape[0]/2:
                        direction.append('center')
                    else:
                        direction.append('bottom')
    
                    if w > image.shape[1]/2:
                        direction.append('center')
                    elif x > image.shape[1]/3:
                        direction.append('right')
                    elif x > image.shape[1]/2:
                        direction.append('center')
                    else:
                        direction.append('left')
    
                    print(label)
                    print(direction)
                    print(x,y,w,h)
                    print("\n")
                    return(direction)
    return(0)
 
    
if __name__ == '__main__':
    detect_func()
