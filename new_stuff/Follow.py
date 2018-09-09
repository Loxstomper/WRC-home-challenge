import Motor
import Wheels
import Robot
import Vision
import Ultrasonic_sensors
import threading
from time import sleep

class Follow():
    def __init__(self, robot):
        print("CRETED A FOLLOW")
        self.robot = robot

    def follow(self):
        '''this is the logic'''

        while True:
        # find out where the object is in the screen

        # treat 0 as the centre
        # if in theshold
        #  if out of distance threshold from ultrasonic go forward

        # if val < 0 - threshold go left
        # if valu > 0 + threashold go right

            print(self.robot.sensor_vals)
            sleep(1)
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

print("CREATED WHEELS")

sensor_values = dict()
sensor_rate = 1
sensors = Ultrasonic_sensors.setup(sensor_rate, sensor_values)

print("CREATED sensors")
robot = Robot.Robot(wheels, sensor_values)
print("Created robot")

y = Follow(robot)
#z = Follow_Thread(y)
y.follow()
