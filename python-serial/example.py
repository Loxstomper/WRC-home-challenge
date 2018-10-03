import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM2')
print(ser)



def move_forward(speed):
    message = "SET:M:{0}:1:1:{1}"

    ser.write((message.format("left", speed)).encode())
    ser.write((message.format("right", speed)).encode())


def move_backward(speed):
    message = "SET:M:{0}:0:1:{1}"

    ser.write((message.format("left", speed)).encode())
    ser.write((message.format("right", speed)).encode())


def get_sensor(sensor, name):
    message = "GET:{0}:{1}"

    ser.write((message.format(sensor, name)).encode())
    sleep(1)

    x = ser.readline().decode()

    print(x)

    if sensor == "US":
        # print()
        pass

    return int(ser.readline().decode())


ultrasonic_sensors = {
        "left": 0,
        "center": 0,
        "right": 0
        }

colour_sensors = {
        "left": 0,
        "center": 0,
        "right": 0
        }

print("JUST A DEMO OF HOW THE PYTHON PROGRAM CAN INTERACT WITH THE ARDUINO\n\n\n");

while True:
    print("Colour sensors");

    # colour_sensors["left"] = get_sensor("CS", "left")
    # colour_sensors["left"] = get_sensor("CS", "center")
    # colour_sensors["left"] = get_sensor("CS", "right")
    # ser.write(input().encode())
    # print(ser.readline().decode())

    get_sensor("CS", "left")

    print(colour_sensors)

    print("Ultrasonic sensors");

    # ultrasonic_sensors["left"] = get_sensor("US", "left")
    # ultrasonic_sensors["left"] = get_sensor("US", "center")
    # ultrasonic_sensors["left"] = get_sensor("US", "right")

    print(ultrasonic_sensors)

    print("\n")




