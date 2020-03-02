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
    pass

def setDPS(ports, power):
    BP.set_motor_dps(ports, power)
    pass

def setSpeed(ports, speed):
    speed = speed * 27
    BP.set_motor_dps(ports, speed)
    pass

def allStop():
    BP.set_motor_power(A + B + C + D, 0)
    pass

def stop(ports):
    BP.set_motor_power(ports, 0)
    pass

def getData():
    touch = BP.get_sensor(one)
    dist = {'f':grovepi.ultrasonicRead(front), 'r':grovepi.ultrasonicRead(right), 'l':grovepi.ultrasonicRead(left)}
    
    #temp = AvgCali(mpu, 5, 0.01)
    #acc = {'x':temp[0], 'y':temp[1], 'z':temp[2]}
    #gyro = {'x':temp[3], 'y':temp[4], 'z':temp[5]}
    #mag = {'x':temp[6], 'y':temp[7], 'z':temp[8]}
    
    mag = mpu.readMagnet()
    gyro = mpu.readGyro()
    acc = mpu.readAccel()
    
    return(touch, dist, gyro)

def checkDist(dataIn):
    if (dataIn[1] <= 10):
        allStop()
        powerMode = False
    pass

def travDist(dist):
    t = (dist / 10.5) / 2
    setDPS(A + D, speed)
    time.sleep(t)
    allStop()
    pass

def turn(deg):
    circ = math.pi * 19.0
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
    pass

def navPoint(p1):
    travDist(p1[0])
    if (p1[1] > 0):
        turn(90)
    elif (p1[1] < 0):
        turn(-90)
    travDist(p1[1])
    pass