import serial
from time import sleep

class API():
    def __init__(self, serial_port):
        self.ser = serial.Serial(serial_port, timeout=1)

    # new
    def stop_wheels(self):
        message = "SET:M:{0}:0:0:{1}"

        self.ser.write((message.format("left", 0)).encode())
        self.ser.write((message.format("right", 0)).encode())

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


    def get_sensor(self, sensor, name):
        message = "GET:{0}:{1}"

        self.ser.write((message.format(sensor, name)).encode())

        response = self.ser.readline()
        response = self.response.decode()

    def move_forward(self, speed):
        message = "SET:M:{0}:0:1:{1}"

        self.ser.write((message.format("left", speed)).encode())
        self.ser.write((message.format("right", speed)).encode())

    def move_backwards(self, speed):
        message = "SET:M:{0}:1:0:{1}"

        self.ser.write((message.format("left", speed)).encode())
        self.ser.write((message.format("right", speed)).encode())

    def stop(self):
        message = "STOP:ALL"
        self.ser.write(message.encode())





if __name__ == "__main__":
    api = API("/dev/ttyACM0")

    while True:
        api.move_forward(200)
        sleep(2)
        api.stop()
        sleep(2)


