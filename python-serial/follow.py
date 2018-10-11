import API
import cv2
import numpy as np
from collections import deque
import imutils
from enum import Enum

class Direction(Enum):
    forward = 1
    left = 2
    right = 3
    backward = 4

class Color(Enum):
    blue = 1
    green = 2
    red = 3

api = API.API("/dev/ttyACM0")
direction = Direction.forward

# open cv setup

webcam = cv2.VideoCapture(0)
pts = deque(maxlen=1000)
center = (0, 0)

# thresholds pixel
thresholds = (40, 50)
width = 640
height = 480
screen_mid = (width // 2, height // 2)

# color thresholds
green_lower = np.array([40, 180, 20])
green_upper = np.array([255, 255, 255])

while True:
    # open cv logic
    ret, frame = webcam.read()

    # probably need to rezie the frame
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # mask
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

        pts.appendleft(center)

        cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        cv2.imshow('webcam', frame)

        # end of cv

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # straight ahead
        if center is not None and center[0] in range(screen_mid[0] - thresholds[0], screen_mid[0] + thresholds[1]):
            if direction is not Direction.forward:
                print("FORWARD")
                direction = Direction.forward
                api.wheels.forward()
            continue

        elif center is not None and center[0] in range(0, screen_mid[0] - thresholds[0]):
            if direction is not Direction.left:
                print("TURN LEFT")
                direction = Direction.left
                # api.wheels.left()
            continue

        elif center is not None and center[0] in range(screen_mid[0] + thresholds[0], width):
            if direction is not Direction.right:
                print("TURN RIGHT")
                direction = Direction.right
                api.wheels.right()
            continue

        else:
            if direction is not Direction.left:
                print("CANT FIND TURNING LEFT")
                direction = Direction.left
                api.wheels.left()
            continue

webcam.release()
cv2.destroyAllWindows()