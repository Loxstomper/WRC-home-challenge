import threading
from time import sleep
import RPi.GPIO as GPIO

class Motor():
    def __init__(self, a, b, enable):
        # pins
        self.a_pin      = a
        self.b_pin      = b
        self.enable_pin = enable

        # setup pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.a_pin, GPIO.OUT)
        GPIO.setup(self.b_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)

        # just in case set to LOW
        GPIO.output(self.a_pin, GPIO.LOW)
        GPIO.output(self.b_pin, GPIO.LOW)
        GPIO.output(self.enable_pin, GPIO.LOW)

        # logic
        self.a_enabled = False
        self.b_enabled = False
        self.enabled   = False

        # speed settings
        self.speed = 0
        self.pulse_width = 0.1 # 0.1 second
        self.pulse_high = 0
        self.pulse_low = 0

    def set_speed(self, speed):
        # should really clamp the speed from 0...100

        # can play with this threshold
        if speed < 0:
            self.enabled = False
        else:
            self.speed = speed
            # calculates percentage then gets the actual value
            self.pulse_high = (speed / 100) * self.pulse_width
            # check for precision
            self.pulse_low = self.pulse_width - self.pulse_high
            self.enabled = True

            print("Pulse Width: {}\nPulse High: {}\nPulse Low: {}\n".format(self.pulse_width, self.pulse_high, self.pulse_low))


    def set_a(self, state):
        self.a_enabled = state

    def set_b(self, state):
        self.b_enabled = state

    def get_a(self):
        return self.a_enabled

    def get_b(self):
        return self.b_enabled


class Motor_Thread(threading.Thread):
    def __init__(self, motor):
        threading.Thread.__init__(self)
        self.motor = motor

    def run(self):
        # just controls the enable pin - emulating hardware PWM
        GPIO.setmode(GPIO.BOARD)

        while True:
            # update the A/B pins
            if self.motor.a_enabled:
                GPIO.output(self.motor.a_pin, GPIO.HIGH)
            else:
                GPIO.output(self.motor.a_pin, GPIO.LOW)

            if self.motor.b_enabled:
                GPIO.output(self.motor.b_pin, GPIO.HIGH)
            else:
                GPIO.output(self.motor.b_pin, GPIO.LOW)
            # not sure if above is required


            # think of a better way - dont think this is needed tbh
            # because below loop always disables
            if not self.motor.enabled:
                GPIO.output(self.motor.enable_pin, GPIO.LOW)

            # speed control
            if self.motor.enabled:
                GPIO.output(self.motor.enable_pin, GPIO.HIGH)
                sleep(self.motor.pulse_high)
                GPIO.output(self.motor.enable_pin, GPIO.LOW)
                sleep(self.motor.pulse_low)
