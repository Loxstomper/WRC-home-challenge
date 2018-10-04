import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0', timeout=1)
print(ser)



def move_forward(speed):
    message = "SET:M:{0}:0:1:{1}"


    ser.write((message.format("left", speed)).encode())
    ser.write((message.format("right", speed)).encode())


def move_backward(speed):
    message = "SET:M:{0}:1:0:{1}"

    ser.write((message.format("left", speed)).encode())
    ser.write((message.format("right", speed)).encode())


def get_sensor(sensor, name):
    message = "GET:{0}:{1}"

    ser.write((message.format(sensor, name)).encode())

    response = ser.readline()
    response = response.decode()

    if not response:
        return -1

    if sensor == "US":
        return float(response)
    else:
        return int(response)


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


# while True:
#     print("move forward")
#     move_forward(100)
#     # get_sensor("US", "left")
#     sleep(3)
#     print("stop")
#     move_forward(0)
#     sleep(1)
#     print("backward")
#     move_backward(100)
#     sleep(3)
#     print("stop")
#     move_backward(0)
#     sleep(1)


i = 0

while True:
    print("Colour sensors");

    x = get_sensor("CS", "left")
    print(i)
    print("VAL: ", x)
    i += 1

    # print(get_sensor("CS", "left"))

    # colour_sensors["left"] = get_sensor("CS", "left")
    # colour_sensors["left"] = get_sensor("CS", "center")
    # colour_sensors["left"] = get_sensor("CS", "right")
    # print(colour_sensors)

    # print("Ultrasonic sensors")

    # ultrasonic_sensors["left"] = get_sensor("US", "left")
    # ultrasonic_sensors["left"] = get_sensor("US", "center")
    # ultrasonic_sensors["left"] = get_sensor("US", "right")

    # print(ultrasonic_sensors)





