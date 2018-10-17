# author: Jayden Thomson
# purpose: follows a black cylinder
import API
import cv2
from enum import Enum

class Direction(Enum):
    forward = 1
    left = 2
    right = 3
    backward = 4

BLACK_HSV = ()
api = API("/dev/ttyACM0")

# thresholds pixel
thresholds = (40, 50)
width = 640
height = 480
screen_mid = (width // 2, height // 2)

direction = Direction.forward

while(1):
    location = api.camera.locateColor(BLACK_HSV)

    # straight ahead
    if location is not None and location[0] in range(screen_mid[0] - thresholds[0], screen_mid[0] + thresholds[1]):
        if direction is not Direction.forward:
            api.wheels
        print("FORWARD")
        api.wheels.forward(200)


    elif location is not None and location[0] in range(0, screen_mid[0] - thresholds[0]):
        print("TURN RIGHT")
        api.send_message("SET:M:right:1:0:150")


    elif location is not None and location[0] in range(screen_mid[0] + thresholds[0], width):
        print("TURN LEFT")
        api.send_message("SET:M:left:1:0:150")

    else:
        print("CANT FIND TURNING LEFT")
        api.send_message("SET:M:left:1:0:150")


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
