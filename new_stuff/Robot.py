# highest level encapsulation

import Motor
import Wheels

class Robot():
    # will be arm and sensors too
    def __init__(self, wheels):
        self.wheels = wheels 

    def move_forward(self, speed, duration):
        self.wheels.forward(speed, duration)

    def move_backward(self, speed, duration):
        pass

    def turn_left(self, speed, duration):
        self.wheels.turn_left(speed, duration)

    def turn_right(self, speed, duration):
        self.wheels.turn_right(speed, duration)


