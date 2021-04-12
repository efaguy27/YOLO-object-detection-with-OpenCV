#!/usr/bin/env python

import numpy as np
import time
import cv2
from picamera import PiCamera
from time import sleep


def detect_func(search_object, detection_count):
    camera = PiCamera()

    camera.resolution = (1920, 1080)
    camera.start_preview()
    sleep(1) # Give camera sensor time to warm up
    camera.capture('/home/pi/41xx/YOLO-object-detection-with-OpenCV/PiCam Detection/images/capture.jpg')
    print("[INFO] Picture taken")
    camera.stop_preview()
    camera.close()
    
    labelsPath = '..//yolo-coco//coco.names'
    LABELS = open(labelsPath).read().strip().split("\n")
    weightsPath = '..//yolo-coco//yolov3.weights'
    configPath = '..//yolo-coco//yolov3.cfg'
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    min_confidence = 0.5
    threshold = 0.3

    pos_result = None
    size_result = None
    object_found = False


    
    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
    dtype="uint8")

    # load our input image and grab its spatial dimensions
    image = cv2.imread("images/capture.jpg")
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
                if (label == search_object):
                    item = image[y:y+h, x:x+w]
   
                    pos_result = (x+(w/2))-(1920/2)
                    size_result = w*h
                    object_found = True
    # ensure at least one detection exists
    if len(idxs) > 0:
	# loop over the indexes we are keeping
	    for i in idxs.flatten():
		# extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                if (LABELS[classIDs[i]] in items):
                    # draw a bounding box rectangle and label on the image
                    color = [int(c) for c in COLORS[classIDs[i]]]
                    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                    cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, color, 2)

    # save the output image
    cv2.imwrite(f'output//Image{detection_count}.png', image)
    return(object_found, pos_result, size_result)

