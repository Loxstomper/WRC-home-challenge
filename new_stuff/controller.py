import Motor
import Wheels
import Robot
import threading
from time import sleep


class Control_Thread(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot

    def run(self):
        print("DIR = {F, R, L, R}")

        while True:
            z = input("DIR SPEED TIME").split()

            if z[0] == 'F':
                self.robot.move_forward(int(z[1]), int(z[2]))
            if z[0] == 'R':
                self.robot.move_backward(int(z[1]), int(z[2]))
            if z[0] == 'L':
                self.robot.turn_left(int(z[1]), int(z[2]))
            if z[0] == 'R':
                self.robot.turn_right(int(z[1]), int(z[2]))


left_motor = Motor.Motor(31, 33, 24)
left_motor_t = Motor.Motor_Thread(left_motor)

right_motor = Motor.Motor(35, 37, 26)
right_motor_t = Motor.Motor_Thread(right_motor)

#wheels = Wheels.Wheels(left_motor, right_motor)




#robot = Robot.Robot(wheels)

#c_t = Control_Thread(robot)

# start threads
#c_t.start()
left_motor_t.start()
#right_motor_t.start()

# join the control thread
#c_t.join()
left_motor_t.join()

left_motor.enabled = True
left_motor.a_enabled = True

left_motor.set_speed(100)
sleep(20)



