import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM2', timeout=100)
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

    x = ser.readline().decode()

    print(x)

    if sensor == "US":
        # print()
        pass

    return int(ser.readline().decode())


colour_sensors = {
        "left": 0,
        "center": 0,
        "right": 0
        }

print("JUST A DEMO OF HOW THE PYTHON PROGRAM CAN INTERACT WITH THE ARDUINO\n\n\n");
print("GOES STRAIGHT FOR 5 tiles and then reverses")

n_tiles = 4 
n_tiles_so_far = 0

starting_colour = 0 if colour_val < 400 else 1
prev_val = starting_colour

while True:
    # forward
    move_forward(100)

    while n_tiles_so_far < n_tiles:
        new_val = 0 if get_sensor("CS", "center") < 400 else 1

        if new_val != prev_val:
            n_tiles_so_far += 1
            prev_val = new_val

    n_tiles_so_far = 0

    # backward
    move_forward(100)

    while n_tiles_so_far < n_tiles:
        new_val = 0 if get_sensor("CS", "center") < 400 else 1

        if new_val != prev_val:
            n_tiles_so_far += 1
            prev_val = new_val
