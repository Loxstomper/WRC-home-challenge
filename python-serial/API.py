import serial
from time import sleep

class Wheels():
    def __init__(self, ser):
        self.ser = ser

    def stop(self):
        message = "SET:M:{0}:0:0:{1}"
        self.ser.write((message.format("left", 0)).encode())
        self.ser.write((message.format("right", 0)).encode())

    def forward(self, speed):
        message = "FORWARD:{0}"
        self.ser.write((message.format(speed)).encode())

    def backwards(self, speed):
        message = "SET:M:{0}:1:0:{1}"

        self.ser.write((message.format("left", speed)).encode())
        self.ser.write((message.format("right", speed)).encode())

    def left(self, speed):
        messageLW = "SET:M:{0}:0:1:{1}"
        messageRW = "SET:M:{0}:1:0:{1}"

        self.ser.write((messageLW.format("left", speed)).encode())
        self.ser.write((messageRW.format("right", speed)).encode())

    def right(self, speed):
        messageLW = "SET:M:{0}:1:0:{1}"
        messageRW = "SET:M:{0}:0:1:{1}"

        self.ser.write((messageLW.format("left", speed)).encode())
        self.ser.write((messageRW.format("right", speed)).encode())


class Claw():
    def __init__(self, ser):
        self.ser = ser

    def open_claw(self, speed):
        message = "SET:M:{0}:1:0:{1}"
        self.ser.write((message.format("claw", speed)).encode())

    def close_claw(self, speed):
        message = "SET:M:{0}:0:1:{1}"
        self.ser.write((message.format("claw", speed)).encode())

    def extend_elbow(self, speed):
        message = "SET:M:{0}:1:0:{1}"

        self.ser.write((message.format("second", speed)).encode())

    def bend_elbow(self, speed):
        message = "SET:M:{0}:0:1:{1}"

        self.ser.write((message.format("second", speed)).encode())


    def raise_arm(self, speed):
        message = "SET:M:{0}:1:0:{1}"

        self.ser.write((message.format("first", speed)).encode())

    def drop_arm(self, speed):
        message = "SET:M:{0}:1:0:{1}"

        self.ser.write((message.format("first", speed)).encode())


class CS():
    def __init__(self, ser, names):
        self.ser = ser
        self.names = names

    def get(self, name):
        message = "GET:CS:{0}"
        self.ser.write((message.format(name)).encode())
        response = self.ser.readline()
        response = self.response.decode()

class US():
    def __init__(self, ser, names):
        self.ser = ser
        self.names = names

    def get(self, name):
        message = "GET:US:{0}"
        self.ser.write((message.format(name)).encode())
        response = self.ser.readline()
        response = self.response.decode()


class API():
    def __init__(self, serial_port):
        self.ser = serial.Serial(serial_port, timeout=1)
        self.CS_names = ["left", "center", "right"]
        self.US_names = ["left", "center", "right"]
        self.wheels = Wheels(self.ser)
        self.claw = Claw(self.ser)
        self.cs = CS(self.ser, self.CS_names)
        self.us = US(self.ser, self.US_names)

    def stop(self):
        message = "STOP:ALL"
        self.ser.write(message.encode())


if __name__ == "__main__":
    api = API("/dev/ttyACM0")

    while True:
        api.wheels.forward(200)
        sleep(2)
        api.wheels.backwards(200)
        sleep(2)
