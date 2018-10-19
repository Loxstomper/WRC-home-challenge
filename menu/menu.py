import RPi.GPIO as GPIO
import serial
import a
from time import sleep

#ser = serial.Serial("/dev/ttyACM0", timeout=1)
ser = None

def menu_colour():
    global ser
    print("MENU COLOUR")

    # green
    message = "LED:0:255:0:"
    #ser.write(message.encode())


def one_colour():
    global ser
    print("one colour")

    # red
    message = "LED:255:0:0:"
    #ser.write(message.encode())


def two_colour():
    global ser
    print("two colour")

    # blue
    message = "LED:0:0:255:"
    #ser.write(message.encode())


def three_colour():
    global ser
    print("three colour")

    # purple
    message = "LED:255:0:255:"
    #ser.write(message.encode())


def four_colour():
    global ser
    print("four colour")

    # yellow
    message = "LED:255:255:0:"
    #ser.write(message.encode())


def main():
    #pins = {"one": 3, "two":5, "three":7, "four":11}
    pins = {"one": 3}

    # pin states
    states = {"one":0, "two":0, "three":0, "four":0}

    # function pointers
    programs = {"one":a.start}

    # program colours
    colours = {"menu":menu_colour, "one":one_colour, "two":two_colour, "three":three_colour, "four":four_colour}

    GPIO.setmode(GPIO.BOARD)

    for pin in pins:
        GPIO.setup(pins[pin], GPIO.IN)

    colours["menu"]()

    while True:
        for pin in pins:
            # button press is a 0 not a 1
            states[pin] = not GPIO.input(pins[pin])

            if states[pin]:
                colours[pin]()
                programs[pin]()
                colours["menu"]()
                sleep(1)
        print(states)


if __name__ == "__main__":
    main()
