import API
from time import sleep



def forward_spaces(spaces, speed, api):
    count = 0
    previous = api.cs.get("centre")
    colour = 1 if previous <= 500 else 0
    new_colour = None
    val = None

    print("STARTING ON: ", colour)

    api.wheels.forward(speed)
    while spaces > count:
        val = api.cs.get("centre")
        new_colour = 1 if val <= 500 else 0

        print("COLOUR: ", new_colour)

        if new_colour != colour:
            count += 1
            colour = new_colour

        sleep(0.1)

    api.wheels.stop()

def backward_spaces(spaces, api):
    count = 0
    previous = api.cs.get("center")
    api.wheels.backward(speed)
    while spaces >= count:
        check_cs = api.cs.get("center")
        if check_cs is not previous:
            count += 1
            previous = api.get("center")
    api.wheels.stop()

speed = 100
api = API.API("/dev/ttyACM0")
count = 0

forward_spaces(4, speed, api)


# while True:
#     try:
#         print(api.cs.get_all())
#         sleep(1)
#
#     except KeyboardInterrupt:
#         api.stop()
#         sleep(1)
#         api.ser.close()
#         exit()
