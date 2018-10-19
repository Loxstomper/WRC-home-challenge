import RPi.GPIO as GPIO
import serial
import motion_detection
from time import sleep

#ser = serial.Serial("/dev/ttyACM0", timeout=1)
ser = None

def menu_colour():
    global ser
    print("MENU COLOUR")

    # green
    message = "LED:0:255:0:"
    ser.write(message.encode())

def pick_demo():
    global ser
    print("PICK DEMO")
    message = "DEMO:"
    ser.write(message.encode())
    print(message.encode())
    GPIO.output(7, GPIO.HIGH)
    sleep(1)
    GPIO.output(7, GPIO.LOW)

def security_demo():
    print("SECURITY DEMO")
    motion_detection.start_program()
    sleep(5)

def one_colour():
    global ser
    print("one colour")

    # red
    message = "LED:255:0:0:"
    ser.write(message.encode())


def two_colour():
    global ser
    print("two colour")

    # blue
    message = "LED:0:0:255:"
    ser.write(message.encode())


def three_colour():
    global ser
    print("three colour")

    # purple
    message = "LED:255:0:255:"
    ser.write(message.encode())


def four_colour():
    global ser
    print("four colour")

    # yellow
    message = "LED:255:255:0:"
    ser.write(message.encode())

def clear_colour():
    global ser

    message = "LED:0:0:0:"
    ser.write(message.encode())


def main():
    # clear LED
    # clear_colour()
    pins = {"one": 3, "two":5}

    # pin states
    states = {"one":0, "two":0}

    # function pointers
    programs = {"one":pick_demo, "two":security_demo}

    # program colours
    colours = {"menu":menu_colour, "one":one_colour, "two":two_colour, "three":three_colour, "four":four_colour}

    GPIO.setmode(GPIO.BOARD)

    for pin in pins:
        GPIO.setup(pins[pin], GPIO.IN)

    GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)


    #colours["menu"]()

    while True:
        print(states)
        for pin in pins:
            # button press is a 0 not a 1
            states[pin] = not GPIO.input(pins[pin])

            if states[pin]:
                colours[pin]()
                programs[pin]()
                colours["menu"]()
                sleep(1)


if __name__ == "__main__":
    main()
