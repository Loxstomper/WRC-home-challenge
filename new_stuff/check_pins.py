# sets all the motor outputs to high

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

pins = [31, 33, 35, 37, 24, 26]

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

GPIO.cleanup()

