import Motor
import threading


class Control_Thread(threading.Thread):
    def __init__(m):
        Thread.__init__(self)
        self.motor = m

    def run():
        y = int(input("Speed: "))

        while y > 0:
            self.motor.speed = y




m1 = Motor.Motor(31, 33, 24)
m1_t = Motor.Motor_Thread(m1)

c_t = Control_thread(m1)

c_t.join()
c_t.start()

m1_t.join()
m1_t.start()





