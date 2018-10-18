import API
from enum import Enum

class Direction(Enum):
    forward = 1
    left = 2
    right = 3
    backward = 4

api = API("/dev/ttyACM0")

direction = Direction.forward
api.wheels.forward(200)

def guide1():
    while(1):
        api.collision()
        api.wheels.forward(200)

def guide3():
    pass