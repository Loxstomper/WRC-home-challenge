import cv2
import numpy as np
from collections import deque
import imutils
import serial
from time import sleep
from enum import Enum

camera = cv2.VideoCapture(0)

green_lower = np.array([40, 180, 20])
green_upper = np.array([255, 255, 255])
green = (green_lower, green_upper)

color_range = green

# the range of the color we want to find
lower = color_range[0]
upper = color_range[1]

center = (0,0)

# reading the camera
ret, frame = camera.read()

# creates a normal frame and a hsv frame
frame = imutils.resize(frame, width=600)
blurred = cv2.GaussianBlur(frame, (11, 11), 0)
hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

# mask
mask = cv2.inRange(hsv, lower, upper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)

# creates a frame that only shows the color we want to find
res = cv2.bitwise_and(frame, frame, mask=mask)

# find contours in the mask and initialize the current
# (x, y) center of the ball
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
center = None

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

print(center)

cv2.imshow('mask', mask)
cv2.imshow('res', res)
cv2.imshow('webcam', frame)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break