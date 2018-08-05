import threading
import time
import RPi.GPIO as GPIO

class Motor():
    def __init__(self, a, b, enable):
        # pins
        self.a_pin      = a
        self.b_pin      = b
        self.enable_pin = enable

        # setup pins
        GPIO.setmode(self.a_pin, GPIO.OUT)
        GPIO.setmode(self.b_pin, GPIO.OUT)
        GPIO.setmode(self.enable_pin, GPIO.OUT)

        # just in case set to LOW
        GPIO.output(self.a_pin, GPIO.LOW)
        GPIO.output(self.b_pin, GPIO.LOW)
        GPIO.output(self.enable_pin, GPIO.LOW)

        # logic
        self.a_enabled = False
        self.b_enabled = False
        self.enabled   = False

        self.speed = 0



class Motor_Thread(threading.Thread):
    def __init__(self, motor):
        Thread.__init__(self)
        self.motor = motor

    def run():
        # just controls the enable pin - emulating hardware PWM

        while True:
            # update the A/B pins
            if self.a_enabled:
                GPIO.output(self.motor.a_pin, GPIO.HIGH)
            else:
                GPIO.output(self.motor.a_pin, GPIO.LOW)

            if self.b_enabled:
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
                sleep(self.motor.speed / 100)
                GPIO.output(self.motor.enable_pin, GPIO.LOW)
                sleep(self.motor.speed / 100)

                


