from time import sleep 

# i dont think i need to make a thread for this
# can just halt movement while the arm is working

# maybe use encoders instead

class Arm():
    '''
    Wrapper around 3 motors, a, b, and a claw
    '''
    def __init__(self, a, b, claw):
        # motors
        self.a = a
        self.b = b
        self.claw = claw

    def extend_arm(self):
        self.extend_a()
        self.extend_b()

    def retract_arm(self):
        self.retract_b()
        self.retract_a()

    def extend_a(self):
        self.a.set_speed(50)
        sleep(5)
        self.a.set_state(false)

    def extend_b(self):
        self.b.set_speed(50)
        sleep(5)
        self.b.set_state(False)

    def grip(self):
        self.claw.set_speed(50)
        sleep(2)
        self.claw.set_state(False)

    def un_grip(self):
        self.claw.set_speed(-50)
        sleep(2)
        self.claw.set_state(False)

    def retract_a(self):
        self.a.set_speed(-50)
        sleep(5)
        self.a.set_state(False)

    def retract_b(self):
        self.b.set_speed(-50)
        sleep(5)
        self.b.set_state(False)
