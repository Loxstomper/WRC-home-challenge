# highest level encapsulation

import Motor
import Wheels

class Robot():
    '''
    Wrapper around the whole system.
    The Robot object is interacted with which in turn interacts with the sub components
    '''

    '''

    NEED TO DO SENSOR CHECKS HERE SO DONT CRASH

    '''


    # will be arm and sensors too
    def __init__(self, wheels, sensor_vals):
        self.wheels = wheels 
        self.sensor_vals = sensor_vals

    def move_forward(self, speed, duration):
        self.wheels.forward(speed, duration)

    def move_backward(self, speed, duration):
        pass

    def turn_left(self, speed, duration):
        self.wheels.turn_left(speed, duration)

    def turn_right(self, speed, duration):
        self.wheels.turn_right(speed, duration)

    def get_sensor_vals(self):
        return self.sensor_vals


