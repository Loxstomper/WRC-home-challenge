import serial

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

    if sensor == "us":
        return float(ser.readline().decode())
    else:
        return int(ser.readline().decode())





ultrasonic_sensors = {
        "left": 0,
        "center": 0,
        "right": 0
        }

colour_sensor = {
        "left": 0,
        "center": 0,
        "right": 0
        }

while True:
    user_input = input("> ")

    forward(int(user_input))

    print(ser.readline().decode())





