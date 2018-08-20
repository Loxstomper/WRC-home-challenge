import Motor
import Wheels
import Robot
import Vision
import Ultrasonic_sensors
import threading

class Follow():
    def __init__(self):
        pass

    def follow(self):
        '''this is the logic'''

        while True:
        # find out where the object is in the screen

        # treat 0 as the centre
        # if in theshold
        #  if out of distance threshold from ultrasonic go forward

        # if val < 0 - threshold go left
        # if valu > 0 + threashold go right
            pass


class Follow_Thread():
    def __init__(self, follow):
        pass

    def run():
        pass

# setting up the components
left_motor   = Motor.Motor(31, 33, 24)
left_motor_t = Motor.Motor_Thread(left_motor)

right_motor   = Motor.Motor(35, 37, 26)
right_motor_t = Motor.Motor_Thread(right_motor)

wheels = Wheels.Wheels(left_motor, right_motor)

sensor_values = dict()
sensor_rate = 1
Ultrasonic_sensors.setup(rate, sensor_values)

robot = Robot.Robot(wheels, sensor_values)
