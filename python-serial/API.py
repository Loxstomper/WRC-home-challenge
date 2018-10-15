import cv2
import numpy as np
from collections import deque
import imutils
import serial
from time import sleep
from enum import Enum
import sys


class Direction(Enum):
    forward = 1
    left = 2
    right = 3
    backward = 4

class Camera():
    def __init__(self):
        try:
            self.camera = cv2.VideoCapture(0)
        except:
            print("Cannot get camera")
            self.camera = None

    def locateColor(self, color_range):
        # the range of the color we want to find
        lower = color_range[0]
        upper = color_range[1]

        center = (0,0)

        # reading the camera
        ret, frame = self.camera.read()

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

            cv2.imshow('mask', mask)
            cv2.imshow('res', res)
            cv2.imshow('webcam', frame)

        return center


class Wheels():
    def __init__(self, ser, names):
        self.ser = ser
        self.names = names

    def stop(self):
        message = "FORWARD:{0}"  # forward because less code and characters
        self.ser.write((message.format(0)).encode())

    def forward(self, speed):
        message = "FORWARD:{0}"
        self.ser.write((message.format(speed)).encode())

    def backward(self, speed):
        message = "BACKWARDS:{0}"
        self.ser.write((message.format(speed)).encode())

    def left(self, speed):
        message = "LEFT:{0}"
        self.ser.write((message.format(speed)).encode())

    def right(self, speed):
        message = "RIGHT:{0}"
        self.ser.write((message.format(speed)).encode())

    def forward_tiles(self, spaces):
        count = 0
        previous = api.cs.get("centre")
        colour = 1 if previous <= 500 else 0
        new_colour = None
        val = None

        print("STARTING ON: ", colour)

        self.forward(100)

        while spaces > count:
            val = api.cs.get("centre")
            new_colour = 1 if val <= 500 else 0

            print("COLOUR: ", new_colour)

            if new_colour != colour:
                count += 1
                colour = new_colour

            sleep(0.1)

        self.stop()

    def backward_tiles(self, spaces):
        count = 0
        previous = api.cs.get("centre")
        colour = 1 if previous <= 500 else 0
        new_colour = None
        val = None

        print("STARTING ON: ", colour)

        self.backward(100)

        while spaces > count:
            val = api.cs.get("centre")
            new_colour = 1 if val <= 500 else 0

            print("COLOUR: ", new_colour)

            if new_colour != colour:
                count += 1
                colour = new_colour

            sleep(0.1)

        self.stop()

    def diagnose(self):
        print("Forward")
        self.forward(100)
        sleep(2)
        self.stop()
        
        print("Backward")
        self.backward(100)
        sleep(2)
        self.stop()

        print("Left")
        self.left(100)
        sleep(2)
        
        print("Right")
        self.right(100)
        sleep(2)

        print("Stop")
        self.stop()

        # for name in names
            # print("Running {0} wheel".format(name))
            # message = "SET:M:{0}:1:0:100"
            # self.ser.write((message.format(name)).encode())
            # sleep(2)
            # message = "SET:M:{0}:0:1:100"
            # self.ser.write((message.format(name)).encode())
            # sleep(2)
            # print("Stopping {0} wheel".format(name))
            # self.stop()


class Claw():
    def __init__(self, ser, names):
        self.ser = ser
        self.names = names

    def extend_claw(self, speed):
        message = "E:C:{0}:"
        self.ser.write((message.format(speed)).encode())

    def bend_claw(self, speed):
        message = "B:C:{0}:"
        self.ser.write((message.format(speed)).encode())

    def extend_elbow(self, speed):
        message = "E:E:{0}:"
        self.ser.write((message.format(speed)).encode())

    def bend_elbow(self, speed):
        message = "B:E:{0}:"
        self.ser.write((message.format(speed)).encode())

    def extend_arm(self, speed):
        message = "E:A:{0}:"
        self.ser.write((message.format(speed)).encode())

    def bend_arm(self, speed):
        message = "B:A:{0}:"
        self.ser.write((message.format(speed)).encode())

    def drop_arm(self):
        message = "DROP:"
        self.ser.write((message.format().encode()))

    def grab(self):
        message = "GRAB:"
        self.ser.write((message.format().encode()))

    def diagnose(self):
        pass
        # for name in self.names:
        #     print("Running {0} motor".format(name))
        #     message = "SET:M:{0}:1:0:50"
        #     self.ser.write((message.format(name)).encode())
        #     sleep(2)
        #     message = "SET:M:{0}:0:1:50"
        #     self.ser.write((message.format(name)).encode())
        #     sleep(2)
        #     print("Stopping {0} motor".format(name))
        #     self.stop()


class CS():
    def __init__(self, ser, names):
        self.ser = ser
        self.names = names

    def get(self, name):
        message = "GET:CS:{0}:"
        self.ser.write((message.format(name)).encode())
        response = self.ser.readline()

        if not response:
            return -1

        return int(response.decode())

    def get_all(self):
        res = {}
        for name in self.names:
            res["CS "+name] = self.get(name)
            sleep(0.5)
        return res


class US():
    def __init__(self, ser, names):
        self.ser = ser
        self.names = names

    def get(self, name):
        message = "GET:US:{0}"
        self.ser.write((message.format(name)).encode())
        response = self.ser.readline()

        if not response:
            return -1
        return float(response.decode())

    def get_all(self):
        res = {}
        for name in self.names:
            res["US"+ name] = self.get(name)
            sleep(0.5)
        return res


class API():
    def __init__(self, serial_port):
        print("API being created")
        self.ser = serial.Serial(serial_port, timeout=1)
        self.wheel_names = ["right", "left"]
        self.claw_names = ["first", "second", "claw"]
        self.CS_names = ["left", "center", "right"]
        self.US_names = ["left", "center", "right"]
        self.wheels = Wheels(self.ser, self.wheel_names)
        self.claw = Claw(self.ser, self.claw_names)
        self.cs = CS(self.ser, self.CS_names)
        self.us = US(self.ser, self.US_names)
        self.camera = Camera()
        self.direction = Direction.forward
        sleep(2)
        print("API created")

    def stop(self):
        message = "STOP:ALL:"
        self.ser.write(message.encode())

    def diagnostics(self):
        print("Running Diagnostic")

        print("Colour Sensor Values")
        print(self.cs.get_all())

        print("Ultrasonic Sensor values")
        print(self.us.get_all())

        print("Wheels")
        self.wheels.diagnose()

        print("Claw")
        self.claw.diagnose()

    def alert_leds(self):
        message = "L:"
        self.ser.write(message.encode())


if __name__ == "__main__":
    api = API("/dev/ttyACM0")
    print("START")
    print("DIAGONSTIC")

    api.diagnostics()

    green_lower = np.array([40, 180, 20])
    green_upper = np.array([255, 255, 255])
    green = (green_lower, green_upper)
    api.camera.locateColor(green)

    while True:
        try:
            pass
        except KeyboardInterrupt:
            api.stop()
            sleep(1)
            api.ser.close()
            exit()

