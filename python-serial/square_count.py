import API 
from time import sleep

api = API.API("/dev/ttyACM0")
count = 0;

while True:
    try:
        print(api.cs.get_all())
        sleep(1)
        # print("FORWARD")
        # ap.wheels.forward(200)
        # sleep(3)
        # print("STOP")
        # ap.wheels.stop()
        # sleep(3)
        # print("BACKWARDS")
        # ap.wheels.backwards(200)
        # sleep(3)
        # print("STOP")
        # ap.wheels.stop()
        # sleep(3)
        # # print("LEFT")
        # # api.wheels.left(200)
        # # sleep(2)
        # # print("RIGHT")
        # # api.wheels.right(200)
        # # sleep(2)
    except KeyboardInterrupt:
        ap.stop()
        sleep(1)
        ap.ser.close()
        exit()