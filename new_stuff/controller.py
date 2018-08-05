import Motor
import threading


class Control_Thread(threading.Thread):
    def __init__(self, m):
        threading.Thread.__init__(self)
        self.motor = m

    def run(self):
        y = int(input("Speed: "))

        while y >= 0:
            if y == 1:
               self.motor.enabled = True
            else:
               self.motor.enabled = False 
            y = int(input("Speed: "))




m1 = Motor.Motor(31, 33, 24)
m1_t = Motor.Motor_Thread(m1)

m1.b_enabled = True

c_t = Control_Thread(m1)

c_t.start()
m1_t.start()
c_t.join()
#m1_t.join()





