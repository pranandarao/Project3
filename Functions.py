from MPU9250 import MPU9250
from IMUFilters import AvgCali
import grovepi
import brickpi3
import math
import time

BP = brickpi3.BrickPi3()
mpu = MPU9250()

#Port Variables
one = BP.PORT_1 #TOUCH SENSOR
two = BP.PORT_2
three = BP.PORT_3
four = BP.PORT_4

A = BP.PORT_A #RIGHT
B = BP.PORT_B
C = BP.PORT_C
D = BP.PORT_D #LEFT

front = 7
right = 8
left = 4

#Speed and Time Variables 
speed = -720

#Setup
BP.set_sensor_type(one, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(two, BP.SENSOR_TYPE.TOUCH)

#Functions
def setPower(ports, power):
    BP.set_motor_power(ports, power)
    return()

def setDPS(ports, power):
    BP.set_motor_dps(ports, power)
    return()

def setSpeed(ports, speed):
    speed = speed * 27
    BP.set_motor_dps(ports, speed)
    return()

def allStop():
    BP.set_motor_power(A + B + C + D, 0)
    return()

def stop(ports):
    BP.set_motor_power(ports, 0)
    return()

def getData():
    touch = BP.get_sensor(one)
    dist = {'f':grovepi.ultrasonicRead(front), 'r':grovepi.ultrasonicRead(right), 'l':grovepi.ultrasonicRead(left)}
    
    temp = AvgCali(mpu, 5, 0.01)
    
    acc = {'x':temp[0], 'y':temp[1], 'z':temp[3]}
    gyro = {'x':temp[4], 'y':temp[5], 'z':temp[6]}
    mag = {'x':temp[7], 'y':temp[8], 'z':temp[9]}
    
    #mag = mpu.readMagnet()
    #gyro = mpu.readGyro()
    #acc = mpu.readAccel()
    
    return(touch, dist, mag, gyro)

def checkDist(dataIn):
    if (dataIn[1] <= 10):
        allStop()
        powerMode = False
    return()

def travDist(dist):
    t = (dist / 10.5) / 2
    setDPS(A + D, speed)
    time.sleep(t)
    allStop()
    return()

def turn(deg):
    circ = math.pi * 18.5
    temp = (abs(deg) / 360) * circ
    t = (temp / 10.5) / 2
    if (deg < 0):
        setDPS(A, speed)
        setDPS(D, -speed)
    elif (deg >= 0):
        setDPS(A, -speed)
        setDPS(D, speed)
    time.sleep(t)
    allStop()
    return()