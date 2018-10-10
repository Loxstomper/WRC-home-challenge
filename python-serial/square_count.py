import API
from time import sleep

speed = 100
api = API.API("/dev/ttyACM0")
count = 0

def forward_spaces(spaces, api):
    count = 0
    previous = api.cs.get("center")
    api.wheels.forward(speed)
    while spaces is not count:
        check_cs = api.cs.get("center")
        if(check_cs is not previous):
            count += 1
            previous = api.get("center")
    api.wheels.stop()

def backward_spaces(spaces, api):
    count = 0
    previous = api.cs.get("center")
    api.wheels.backward(speed)
    while spaces is not count:
        check_cs = api.cs.get("center")
        if(check_cs is not previous):
            count += 1
            previous = api.get("center")
    api.wheels.stop()




while True:
    try:
        print(api.cs.get_all())
        sleep(1)

    except KeyboardInterrupt:
        api.stop()
        sleep(1)
        api.ser.close()
        exit()