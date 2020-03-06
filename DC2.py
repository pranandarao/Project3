from MPU9250 import MPU9250
from IMUFilters import AvgCali
import grovepi
import brickpi3
import time
import math

BP = brickpi3.BrickPi3()
mpu = MPU9250()

#Port Variables
one = BP.PORT_1 
two = BP.PORT_2
three = BP.PORT_3
four = BP.PORT_4

A = BP.PORT_A #RIGHT
B = BP.PORT_B
C = BP.PORT_C
D = BP.PORT_D #LEFT

#Setup
BP.set_sensor_type(one, BP.SENSOR_TYPE.TOUCH)

#Functions
def setPower(ports, power):
    BP.set_motor_power(ports, power)
    return()

def setDPS(ports, speed):
    BP.set_motor_dps(ports, speed)
    return()

def allStop():
    BP.set_motor_power(A + B + C + D, 0)
    return()

def stop(ports):
    BP.set_motor_power(ports, 0)
    return()

def getData():
    gyro = mpu.readGyro()
    gx = gyro['x']
    gy = gyro['y']
    gz = gyro['z']
    touch = BP.get_sensor(one)
    x,y,z = AvgCali(mpu, 5, 0.1)

    gyro = {'x':(gx - x), 'y':(gy - y), 'z':(gz - z)}

    return(touch, gyro)

#Main Area
allStop()

try:
    while True:
        try:
            #Control Logic
            data = getData()
            print(data)
            initial = BP.get_motor_encoder(C)
            initial2 = BP.get_motor_encoder(B)
            print(initial, initial2)
            BP.set_motor_position(B, initial2)
            if (data[0] == 1):
                while True:
                    curr = BP.get_motor_encoder(C)
                    BP.set_motor_position(B, initial2 + (initial - curr))
        except brickpi3.SensorError as error:
            print(error)
except KeyboardInterrupt:
    allStop()
