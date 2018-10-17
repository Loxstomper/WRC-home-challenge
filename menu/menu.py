import Rpi.GPIO as GPIO

def main():
    button_pin = 2
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(button_pin, GPIO.IN)

    state = False

    while True:
        print(GPIO.input(button_pin))


if __name__ == "__main__":
    main()
