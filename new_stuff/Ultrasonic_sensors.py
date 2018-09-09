#!/bin/python3

''' 
    Author: Lochie Ashcroft

    Multithreaded ultrasonic sensors
    Reads sensor config from sensors.cfg
    Distance values are stored in a dictionary {id:value}
'''


import time
import random
import threading

import RPi.GPIO as GPIO

class Ultrasonic_Sensor():
    def __init__(self, ID, trig, echo, threshold):
        GPIO.setmode(GPIO.BOARD)
        self.ID = ID
        self.trig = trig
        self.echo = echo
        self.threshold = threshold # would like to use the theshold but probably better to use that externally

        print("\nInitializing Ultrasonic Sensor \n{}".format(self.get_info()))

        # setup the sr04 ultrasonic sensor
        print("TRIG: ", self.trig)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trig, GPIO.LOW)
        time.sleep(2)
        print("Initialization complete")


    def get_distance(self):
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        # seing a 10us pulse to trigger pin
        GPIO.output(self.trig, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trig, GPIO.LOW)

        pulse_start = 0

        # getting start time
        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()

        # getting end time
        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()

        duration = pulse_end - pulse_start
        # duration = random.uniform(0, 1) * 0.1

        # calculating distance: speed = d/t, need to divide by 2 as well because we just want to know single distance
        # speed is the speed of sound, also getting the distance in CM may change to MM
        distance = duration * 17150

        # decide if any rounding should be done, probably takes longer to round it and not worth

        # reset i/o
        #GPIO.cleanup()
        return distance


    def get_info(self):
        return "ID: {} TRIG: {} Echo: {} Threshold: {}".format(self.ID, self.trig, self.echo, self.threshold)


class Ultrasonic_Sensor_Thread(threading.Thread):
    def __init__(self, sensor, sensor_values, rate):
        threading.Thread.__init__(self)
        self.sensor = sensor
        self.sensor_values = sensor_values
        self.rate = 1 / rate


    def run(self):
        while True:
            self.sensor_values[self.sensor.ID] = self.sensor.get_distance()
            time.sleep(self.rate)


class Main_Thread(threading.Thread):
    def __init__(self, sensor_values):
        while True:
            print("Main:")
            for k in sensor_values:
                print(k, ":", sensor_values[k])
            print()
            time.sleep(1)


# Globals
# sensor_info = dict()
# hopefully this dictionary wont be a problem with the GIL, this is more convient to use but can be changed
#sensor_values = dict()


# Functions
def get_sensor_info():
    sensor_info = dict()

    with open("sensors.cfg", "r") as f:
        for line in f:
            if not line.startswith('#'):
                tmp = line.split()
                sensor_info[tmp[0]] = [int(tmp[i]) for i in range(1, len(tmp))]

    return sensor_info


def setup(rate, sensor_values):
    rate = 4
    sensors = []
    threads = []
    # replace this with loading from file
    print("Getting sensor info\n")
    sensor_info = get_sensor_info()

    # should i initalise the sensor_values dict? maybe with a -1 and use that as a check later on??

    print("Setting up sensors\n")
    for sensor in sensor_info:
        print(sensor)
        trig, echo, threshold = sensor_info[sensor]
        # this is serial... slow startup time, oh well..
        sensors.append(Ultrasonic_Sensor(sensor, trig, echo, threshold))

    print("Setting up threads\n")

    try:
        for sensor in sensors:
            threads.append(Ultrasonic_Sensor_Thread(sensor, sensor_values, rate))
            threads[-1].start()
    except Error as e:
        print("Error: unable to start threads\n", e)

    #x = Main_Thread(sensor_values)
    print("Starting threads")
    #x.start()
    #x.join()

    # i think this should be removed, but idk
    #for thread in threads:
        #thread.join()

    return threads





if __name__ == "__main__":
    z = dict()
    setup(1, z)
