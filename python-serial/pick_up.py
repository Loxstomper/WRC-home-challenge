import API
import cv2
from enum import Enum

class Direction(Enum):
    forward = 1
    left = 2
    right = 3
    backward = 4

green = ([40, 180, 20],[255, 255, 255])
blue = ([110,50,50], [130,255,255])
red = ([170,50,50], [180,255,255])

api = API("/dev/ttyACM0")

# thresholds pixel
thresholds = (40, 50)
width = 640
height = 480
screen_mid = (width // 2, height // 2)

direction = Direction.forward
api.wheels.forward(200)

def pick1():
    object = 0
    straight = 0
    finished = 0

    while(object == 0):
        api.collision()
        center = api.camera.locateColor(green)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

        # straight ahead
        if center is not None and center[0] in range(screen_mid[0] - thresholds[0], screen_mid[0] + thresholds[1]):
            if direction is not Direction.forward:
                api.stop()
                print("FORWARD")
                api.wheels.forward(200)

        elif center is not None and center[0] in range(0, screen_mid[0] - thresholds[0]):
            if direction is not Direction.right:
                api.stop()
                print("TURN RIGHT")
                api.send_message("SET:M:right:1:0:150")

        elif center is not None and center[0] in range(screen_mid[0] + thresholds[0], width):
            if direction is not Direction.left:
                api.stop()
                print("TURN LEFT")
                api.send_message("SET:M:left:1:0:150")

        elif api.us.get(center) < 10:
            object = 1

        else:
            print("CANT FIND TURNING LEFT")
            api.stop()
            api.send_message("SET:M:left:1:0:150")

    while(straight == 0):
        center = api.camera.locateColor(green)

        if center is not None and center[0] in range(0, screen_mid[0] - thresholds[0]):
            if direction is not Direction.right:
                api.stop()
                print("TURN RIGHT")
                api.send_message("SET:M:right:1:0:150")

        elif center is not None and center[0] in range(screen_mid[0] + thresholds[0], width):
            if direction is not Direction.left:
                api.stop()
                print("TURN LEFT")
                api.send_message("SET:M:left:1:0:150")
        else:
            straight = 1

    api.wheels.backwards_tiles(5)
    api.claw.drop_arm()
    api.wheels.forward_tiles(1)
    api.claw.grab()

    while(finished == 0):
        api.collision()
        color = api.cs.get(center)
        center = api.camera.locateColor(blue)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

        # straight ahead
        if center is not None and center[0] in range(screen_mid[0] - thresholds[0], screen_mid[0] + thresholds[1]):
            if direction is not Direction.forward:
                api.stop()
                print("FORWARD")
                api.wheels.forward(200)

        elif center is not None and center[0] in range(0, screen_mid[0] - thresholds[0]):
            if direction is not Direction.right:
                api.stop()
                print("TURN RIGHT")
                api.send_message("SET:M:right:1:0:150")

        elif center is not None and center[0] in range(screen_mid[0] + thresholds[0], width):
            if direction is not Direction.left:
                api.stop()
                print("TURN LEFT")
                api.send_message("SET:M:left:1:0:150")

        elif color > 200 and color < 300 :
            api.wheels.backwards_tiles(5)
            api.claw.drop_arm()
            finished = 1

        else:
            print("CANT FIND TURNING LEFT")
            api.stop()
            api.send_message("SET:M:left:1:0:150")
