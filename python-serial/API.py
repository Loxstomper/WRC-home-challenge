import serial
from time import sleep

class API():
    def __init__(self, serial_port):
        self.ser = serial.Serial(serial_port, timeout=1)

    # new
    def stop(self):
        message = "SET:M:{0}:0:0:{1}"

        self.ser.write((message.format("left", 0)).encode())
        self.ser.write((message.format("right", 0)).encode())


    def turn_left(self, speed):
        messageLW = "SET:M:{0}:0:1:{1}"
        messageRW = "SET:M:{0}:1:0:{1}"

        self.ser.write((messageLW.format("left", speed)).encode())
        self.ser.write((messageRW.format("right", speed)).encode())


    def turn_right(self, speed):
        messageLW = "SET:M:{0}:1:0:{1}"
        messageRW = "SET:M:{0}:0:1:{1}"

        self.ser.write((messageLW.format("left", speed)).encode())
        self.ser.write((messageRW.format("right", speed)).encode())


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

if __name__ == "__main__":
    api = API("/dev/ttyACM0")
    api.raise_arm(200)
    sleep(5)
    api.drop_arm(200)
    sleep(5)


