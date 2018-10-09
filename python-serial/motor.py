import serial
from time import sleep

motorLst = ["left", "right", "claw", "first", "second"]

# new
def stop():
    message = "SET:M:{0}:0:0:{1}"

    ser.write((message.format("left", 0)).encode())
    ser.write((message.format("right", 0)).encode())


def turn_left(speed):
    messageLW = "SET:M:{0}:0:1:{1}"
    messageRW = "SET:M:{0}:1:0:{1}"

    ser.write((messageLW.format("left", speed)).encode())
    ser.write((messageRW.format("right", speed)).encode())


def turn_right(speed):
    messageLW = "SET:M:{0}:1:0:{1}"
    messageRW = "SET:M:{0}:0:1:{1}"

    ser.write((messageLW.format("left", speed)).encode())
    ser.write((messageRW.format("right", speed)).encode())


def open_claw(speed):
    message = "SET:M:{0}:1:0:{1}"

    ser.write((message.format("claw", speed)).encode())


def close_claw(speed):
    message = "SET:M:{0}:0:1:{1}"

    ser.write((message.format("claw", speed)).encode())


def extend_elbow(speed):
    message = "SET:M:{0}:1:0:{1}"

    ser.write((message.format("second", speed)).encode())


def bend_elbow(speed):
    message = "SET:M:{0}:0:1:{1}"

    ser.write((message.format("second", speed)).encode())


def raise_arm():
    messageStart = "SET:M:{0}:1:0:{1}"
    messageStop = "SET:M:{0}:0:0:{1}"
    ser.write((messageStart.format("first", 200)).encode())
    sleep(2)
    ser.write((messageStop.format("first", 0)).encode())



def drop_arm(speed):
    message = "SET:M:{0}:0:1:{1}"

    ser.write((message.format("first", speed)).encode())


def crash():
    message = "SET:M:{0}:0:0:{1}"
    for motor in motorLst:
        ser.write((message.format(motor, 0)).encode())


if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM0', timeout=1)
    while True:
        raise_arm(200)
        sleep(5)
        drop_arm(200)
        sleep(5)

        crash()

