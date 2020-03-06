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

#Course Variables
course = [[0 for i in range(20)] for j in range(10)]
orient = 0

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
    
    return(touch, dist)

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

def navPointX(x, y):
    travDist(x)
    print('reached 1')
    if (y > 0):
        turn(90)
        print('reached 2')
    elif (y < 0):
        turn(-90)
        print('reached 3')
    print('reached 4')
    travDist(y)
    print('reached 5')
    if (y > 0):
        turn(-90)
        print('reached 6')
    elif (y < 0):
        turn(90)
        print('reached 7')
    pass

def navPointY(x, y):
    print('reached 1')
    if (y > 0):
        turn(90)
        print('reached 2')
    elif (y < 0):
        turn(-90)
        print('reached 3')
    print('reached 4')
    travDist(y)
    print('reached 5')
    if (y > 0):
        turn(-90)
        print('reached 6')
    elif (y < 0):
        turn(90)
        print('reached 7')
    travDist(x)
    pass

def navigate():
    dis = 25
    dis2 = 25
    side = 20
    while (True):
        travDist(40)
        data = getData()[1]
        if (data['f'] <= dis and data['r'] <= side and data['l'] <= side):
            turn(180)
            print('reached dead end')
        if (data['f'] <= dis and data['r'] > side and data['l'] <= side):
            turn(90)
            print('reached right turn')
        if (data['f'] <= dis and data['r'] <= side and data['l'] > side):
            turn(-90)
            print('reached left turn')
        if (data['f'] > dis and data['r'] > side and data['l'] > side):
            allStop()
            print('reached end')
            break
        if (data['f'] <= dis2 and data['r'] > side and data['l'] > side):
            turn(-90)
            print('reached t-junction')
    pass 

def printMap():
    for i in course:
        for j in i:
            print(str(j), end=" ")
        print()
    pass