#!python3

import cv2
import numpy as np
from collections import deque
import imutils
import threading
import Motor
import Wheels
import Robot
import Ultrasonic_sensors
from time import sleep

class Vision():
    def __init__(self, colour_pos):
        self.webcam = cv2.VideoCapture(0)

        # hsv
        self.green_lower = np.array([40, 180, 20])
        self.green_upper = np.array([255, 255, 255])

        # thresholds pixel
        self.thresholds = (40, 50)
        self.width = 600
        self.height = 480
        self.screen_mid = (self.width // 2, self.height // 2)

        self.colour_pos = None

    def do_stuff(self):
        pts = deque(maxlen=1000)

        ret, frame = self.webcam.read()

        # frame wasnt capture, frame=None
        if not frame:
            return

        # probably need to rezie the frame
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # masks
        mask = cv2.inRange(hsv, self.green_lower, self.green_upper)
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

            self.center = center

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # update the points queue
        pts.appendleft(center)

        # we are doing a 680x480 video

        # straight ahead
        if center is not None and center[0] in range(self.screen_mid[0] - self.thresholds[0], self.screen_mid[0] + self.thresholds[1]):
            # print("FORWRD")
            # self.colour_pos = 0
            return 0

        elif center is not None and center[0] in range(0, self.screen_mid[0] - self.thresholds[0]):
            print("TURN RIGHT")
            # self.colour_pos = 1 
            return 1

        elif center is not None and center[0] in range(self.screen_mid[0] + self.thresholds[0], self.width):
            print("TURN LEFT")
            # self.colour_pos = -1 
            return -1
        
        else:
            print("CANT FIND TURNING LEFT")
            # self.colour_pos = -2
            return -2


class Vision_Thread(threading.Thread):
    def __init__(self, vis, robot):
        threading.Thread.__init__(self)
        self.vis = vis
        self.robot = robot

    def run(self):
        while True:
            direction = self.vis.do_stuff()

            if direction == 0:
                print("Object is in front")
                self.robot.move_forward(100, 1)
                
            elif direction == 1:
                print("Object is at right")
                self.robot.turn_right(100, 1)

            elif direction == -1:
                print("Object is at left")
                self.robot.turn_left(100, 1)

            elif direction == -2:
                print("Couldnt find object turning left")
                self.robot.turn_left(100, 1)
                


class Logic_Thread(threading.Thread):
    def __init__(self, robot, color_pos):
        threading.Thread.__init__(self)
        self.colour_pos = colour_pos

    def run(self):
        print("COLOUR POS: ", self.colour_pos)
        sleep(1)


left_motor   = Motor.Motor(31, 33, 24)
left_motor_t = Motor.Motor_Thread(left_motor)

right_motor   = Motor.Motor(35, 37, 26)
right_motor_t = Motor.Motor_Thread(right_motor)

wheels = Wheels.Wheels(left_motor, right_motor)

print("CREATED WHEELS")

sensor_values = dict()
sensor_rate = 1
# sensors = Ultrasonic_sensors.setup(sensor_rate, sensor_values)

print("CREATED sensors")
robot = Robot.Robot(wheels, sensor_values)
print("Created robot")

colour_pos = 0
v = Vision(colour_pos)
v_t = Vision_Thread(v, robot)
v_t.start()
