from time import sleep

# wrapper around the Motors

# need to decide if I still want each motor to have a thread or should its container
class Wheels():
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def left(self, speed, duration):
        # enable right motor, disable left
        self.right.set_speed(speed)
        self.left.set_state(False)

        sleep(duration)
        self.right.set_state(False)

    def right(self, speed, duration):
        # enable right motor, disable left
        self.left.set_speed(speed)
        self.right.set_state(False)

        sleep(duration)
        self.left.set_state(False)

    def forward(self, speed, duration):
        self.left.set_speed(speed)
        self.right.set_speed(speed)

        sleep(duration)

        self.left.set_state(False)
        self.left.set_state(True)

    # figure out what im going to do here
    def reverse(self, speed, duration):
        pass
