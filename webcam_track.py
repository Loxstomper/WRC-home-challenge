#!python3

import cv2
import numpy as np
from collections import deque
import imutils

webcam = cv2.VideoCapture(0)
pts = deque(maxlen=1000)
center = (0, 0) 

# BRG
# green_lower = np.array([120, 80, 20])
# green_upper = np.array([120, 140, 20])
# green_lower = np.array([180, 60, 40])
green_lower = np.array([40, 180, 20])
green_upper = np.array([255, 255, 255])

# thresholds pixel
thresholds = (40, 50)
width = 640
height = 480
screen_mid = (width // 2, height // 2)

while True:
    ret, frame = webcam.read()

    # probably need to rezie the frame
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



    # masks
    # mask = cv2.inrange(hsv, green_lower, green_upper)
    mask = cv2.inRange(hsv, green_lower, green_upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    res = cv2.bitwise_and(frame, frame, mask=mask)


    # find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None
 
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # print(center)
        
 
	# update the points queue
    pts.appendleft(center)

    cv2.imshow('webcam', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    # we are doing a 680x480 video

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # straight ahead
    if center is not None and center[0] in range(screen_mid[0] - thresholds[0], screen_mid[0] + thresholds[1]):
        print("FORWRD")
        continue

    elif center is not None and center[0] in range(0, screen_mid[0] - thresholds[0]):
        print("TURN RIGHT")
        continue

    elif center is not None and center[0] in range(screen_mid[0] + thresholds[0], width):
        print("TURN LEFT")
        continue
    
    else:
        print("CANT FIND TURNING LEFT")
        continue

webcam.release()
cv2.destroyAllWindows()