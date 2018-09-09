import Motor
import Wheels
import Robot
import Vision
import Ultrasonic_sensors
import threading
from time import sleep

class Drive():
    def __init__(self, robot):
        self.robot = robot


    def do_stuff(self):
        '''this is the logic'''
        l = 0
        c = 0
        r = 0
        threshold = 10
        current_state = ""

        while True:
            print(self.robot.sensor_vals)
            print(current_state)

            l = self.robot.sensor_vals['left']
            r = self.robot.sensor_vals['right']
            c = self.robot.sensor_vals['center']

            # clear path straight ahead
            if c > threshold:
                # maybe get rid of the duration?
                current_state = "Forward!"
                self.robot.forward(100, 1)
                continue

            sleep(1)
            


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

y = Drive(robot)
#z = Follow_Thread(y)
y.do_stuff ()
