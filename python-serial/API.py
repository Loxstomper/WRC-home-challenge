import serial
from time import sleep
import sys


class Wheels():
    def __init__(self, ser, names):
        self.ser = ser
        self.names = names

    def stop(self):
        message = "FORWARD:{0}"  # forward because less code and characters
        self.ser.write((message.format(0)).encode())

    def forward(self, speed):
        message = "FORWARD:{0}"
        self.ser.write((message.format(speed)).encode())

    def backward(self, speed):
        message = "BACKWARDS:{0}"
        self.ser.write((message.format(speed)).encode())

    def left(self, speed):
        message = "LEFT:{0}"
        self.ser.write((message.format(speed)).encode())

    def right(self, speed):
        message = "RIGHT:{0}"
        self.ser.write((message.format(speed)).encode())

    def forward_tiles(self, spaces):
        count = 0
        previous = api.cs.get("centre")
        colour = 1 if previous <= 500 else 0
        new_colour = None
        val = None

        print("STARTING ON: ", colour)

        self.forward(100)

        while spaces > count:
            val = api.cs.get("centre")
            new_colour = 1 if val <= 500 else 0

            print("COLOUR: ", new_colour)

            if new_colour != colour:
                count += 1
                colour = new_colour

            sleep(0.1)

        self.stop()

    def backward_tiles(self, spaces):
        count = 0
        previous = api.cs.get("centre")
        colour = 1 if previous <= 500 else 0
        new_colour = None
        val = None

        print("STARTING ON: ", colour)

        self.backward(100)

        while spaces > count:
            val = api.cs.get("centre")
            new_colour = 1 if val <= 500 else 0

            print("COLOUR: ", new_colour)

            if new_colour != colour:
                count += 1
                colour = new_colour

            sleep(0.1)

        self.stop()

    def diagnose(self):
        for name in self.names:
            print("Running {0} wheel".format(name))
            message = "SET:M:{0}:1:0:100"
            self.ser.write((message.format(name)).encode())
            sleep(2)
            message = "SET:M:{0}:0:1:100"
            self.ser.write((message.format(name)).encode())
            sleep(2)
            print("Stopping {0} wheel".format(name))
            self.stop()




class Claw():
    def __init__(self, ser, names):
        self.ser = ser
        self.names = names

    def extend_claw(self, speed):
        message = "E:C:{0}:"
        self.ser.write((message.format(speed)).encode())

    def bend_claw(self, speed):
        message = "B:C:{0}:"
        self.ser.write((message.format(speed)).encode())

    def extend_elbow(self, speed):
        message = "E:E:{0}:"
        self.ser.write((message.format(speed)).encode())

    def bend_elbow(self, speed):
        message = "B:E:{0}:"
        self.ser.write((message.format(speed)).encode())

    def extend_arm(self, speed):
        message = "E:A:{0}:"
        self.ser.write((message.format(speed)).encode())

    def bend_arm(self, speed):
        message = "B:A:{0}:"
        self.ser.write((message.format(speed)).encode())

    def diagnose(self):
        for name in self.names:
            print("Running {0} motor".format(name))
            message = "SET:M:{0}:1:0:50"
            self.ser.write((message.format(name)).encode())
            sleep(2)
            message = "SET:M:{0}:0:1:50"
            self.ser.write((message.format(name)).encode())
            sleep(2)
            print("Stopping {0} motor".format(name))
            self.stop()



class CS():
    def __init__(self, ser, names):
        self.ser = ser
        self.names = names

    def get(self, name):
        message = "GET:CS:{0}:"
        self.ser.write((message.format(name)).encode())
        response = self.ser.readline()

        if not response:
            return -1

        return int(response.decode())

    def get_all(self):
        res = {}
        for name in self.names:
            res["CS "+name] = self.get(name)
            sleep(0.5)
        return res


class US():
    def __init__(self, ser, names):
        self.ser = ser
        self.names = names

    def get(self, name):
        message = "GET:US:{0}"
        self.ser.write((message.format(name)).encode())
        response = self.ser.readline()

        if not response:
            return -1
        return float(response.decode())

    def get_all(self):
        res = {}
        for name in self.names:
            res["US"+ name] = self.get(name)
            sleep(0.5)
        return res


class API():
    def __init__(self, serial_port):
        print("API being created")
        self.ser = serial.Serial(serial_port, timeout=1)
        self.wheel_names = ["right", "left"]
        self.claw_names = ["first", "second", "claw"]
        self.CS_names = ["left", "center", "right"]
        self.US_names = ["left", "center", "right"]
        self.wheels = Wheels(self.ser, self.wheel_names)
        self.claw = Claw(self.ser, self.claw_names)
        self.cs = CS(self.ser, self.CS_names)
        self.us = US(self.ser, self.US_names)
        sleep(2)
        print("API created")

    def stop(self):
        message = "STOP:ALL:"
        self.ser.write(message.encode())

    def diagnostics(self):
        print("Running Diagnostic")
        print("Sensor Values")
        res = self.cs.get_all()
        res.update(self.us.get_all())
        print(res)
        print("Motors")
        self.wheels.diagnose()
        self.claw.diagnose()





if __name__ == "__main__":
    api = API("/dev/ttyACM0")
    print("START")

    while True:

        try:
            # print(api.cs.get_all())
            # sleep(1)
            # api.claw.bend_arm(200)
            # sleep(2)
            # api.claw.bend_arm(0)
            # sleep(2)
            print("FORWARD")
            api.wheels.forward(255)
            sleep(3)
            print("STOP")
            api.wheels.stop()
            sleep(3)
            print("BACKWARDS")
            api.wheels.backwards(255)
            sleep(3)
            print("STOP")
            api.wheels.stop()
            sleep(3)
            # print("LEFT")
            # api.wheels.left(200)
            # sleep(2)
            # print("RIGHT")
            # api.wheels.right(200)
            # sleep(2)
        except KeyboardInterrupt:
            api.stop()
            sleep(1)
            api.ser.close()
            exit()

