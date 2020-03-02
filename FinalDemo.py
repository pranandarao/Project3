from MPU9250 import MPU9250
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

ranger = 3
leftLine = 2
rightLine = 7

#Speed and Time Variables
clawHoldPower = 20
clawDropPower = 10
clawDropTime = 0.2      
speed = 15
lineTime = 0.2
lineWaitTime = 1
dropDist = 2

#Course Variables
magNum = 3
magNeed = 0
splitNum = 0
leftTurn = False
dropZone = 'A' #SET TO A, B, OR C DEPENDING ON ZONE

if (dropZone == 'A'):
    magNeed = 2
elif (dropZone == 'B'):
    magNeed = 3
elif (dropZone == 'C'):
    magNeed = 4

#Failsafes and Modes
lineMode = True
powerMode = False
cargoMode = False

#Setup
BP.set_sensor_type(one, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(two, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(four, BP.SENSOR_TYPE.CUSTOM, [(BP.SENSOR_CUSTOM.PIN1_ADC)])

grovepi.pinMode(leftLine, "INPUT")
grovepi.pinMode(rightLine, "INPUT")

#Functions
def setPower(ports, power):
    BP.set_motor_power(ports, power)
    return()

def setSpeed(ports, speed):
    speed = speed * 27
    BP.set_motor_dps(ports, speed)
    return()

def allStop():
    BP.set_motor_power(A + B + C + D, 0)
    return()

def hallRead(data):
    if(data == 0):
        return(False)
    elif(data > 175):
        return(True)
    else:
        return(False)

def stop(ports):
    BP.set_motor_power(ports, 0)
    return()

def clawGrab():
    setPower(B + C, clawHoldPower)
    return()

def clawDrop():
    setPower(B + C, -clawDropPower)
    time.sleep(clawDropTime)
    return()

def cargoDrop(dataIn):
    if (dataIn[4]):
        setPower(A + D, speed)
        time.sleep(dropDist)
        clawDrop()
        time.sleep(1)
        setPower(A + D, speed)
    return()

def getData():
    mag = mpu.readMagnet()
    mag_x = mag['x']
    mag_y = mag['y']
    mag_z = mag['z']

    touch = BP.get_sensor(one)
    left = grovepi.digitalRead(leftLine)
    right = grovepi.digitalRead(rightLine)
    dist = grovepi.ultrasonicRead(ranger)
    imuData = math.sqrt(pow(mag_x, 2) + pow(mag_y, 2) + pow(mag_z, 2))
    
    return(touch, left, right, dist, hallRead(imuData), imuData)

def checkDist(dataIn):
    if (dataIn[3] <= 10):
        allStop()
        powerMode = False
    return(not powerMode)

#Main Area
allStop()
clawDrop()

initTime = time.time()

try:
    while True:
        try:
            #Control Logic
            data = getData()
            print(data)
            
            currTime = time.time()

            if (data[0] == 1):
                print('STARTING RUN')
                time.sleep(1)
                clawGrab()
                cargoMode = True
                setSpeed(A + D, speed)
                time.sleep(2)
                data = getData()
                print('\nMade it here\n')

            while (data[3] <= 10):
                currTime = time.time()
                allStop()
                data = getData()
                if (data[3] > 10):
                    setSpeed(speed)
            
            currTime = time.time()
            
            if (data[4] and currTime - initTime > 3):
                initTime = time.time()
                magNum += 1
                if (magNum == magNeed):
                    cargoDrop()
                    currTime = time.time()
                if (magNum == magNeed - 1):
                    data = getData()
                    setPower(A, 50)
                    setPower(D, -50)
                    time.sleep(lineWaitTime)
                    setSpeed(A + D, speed)

            if (data[4] and magNum > magNeed):
                allStop()
                powerMode = False

            #Line Finding
            if (data[1] == 1): #Left Line Finder
                while(powerMode):
                    currTime = time.time()
                    setPower(A, 50)
                    setPower(D, -50)
                    data = getData()
                    
                    if (data[1] == 1 and data[2] == 1 and not leftTurn):
                        data = getData()
                        setPower(A, -50)
                        setPower(D, 50)
                        time.sleep(lineWaitTime)
                        setSpeed(A + D, speed)
                        if (not cargoMode):
                            leftTurn = not leftTurn

                    if (data[1] == 1 and data[2] == 1 and (leftTurn or cargoMode)):
                        data = getData()
                        setPower(A, 50)
                        setPower(D, -50)
                        time.sleep(lineWaitTime)
                        setSpeed(A + D, speed)
                        if (not cargoMode):
                            leftTurn = not leftTurn

                    if (checkDist(data)):
                        break

                    if (data[4] and currTime - initTime > 3):
                        initTime = time.time()
                        magNum += 1
                        if (magNum == magNeed):
                            cargoDrop()
                            currTime = time.time()
                        if (magNum == magNeed - 1):
                            data = getData()
                            setPower(A, 50)
                            setPower(D, -50)
                            time.sleep(lineWaitTime)
                            setSpeed(A + D, speed)

                    if (data[1] == 0):
                        time.sleep(lineTime)
                        setSpeed(A + D, speed)
                        break

            if (data[2] == 1): #Right Line Finder
                while(powerMode):
                    currTime = time.time()
                    setPower(A, -50)
                    setPower(D, 50)
                    data = getData()
                    if (data[1] == 1 and data[2] == 1 and not leftTurn):
                        data = getData()
                        setPower(A, -50)
                        setPower(D, 50)
                        time.sleep(lineWaitTime)
                        setSpeed(A + D, speed)
                        if (not cargoMode):
                            leftTurn = not leftTurn

                    if (data[1] == 1 and data[2] == 1 and (leftTurn or cargoMode)):
                        data = getData()
                        setPower(A, 50)
                        setPower(D, -50)
                        time.sleep(lineWaitTime)
                        setSpeed(A + D, speed)
                        if (not cargoMode):
                            leftTurn = not leftTurn

                    if (checkDist(data)):
                        break
                    
                    if (data[4] and currTime - initTime > 3):
                        initTime = time.time()
                        magNum += 1
                        if (magNum == magNeed):
                            cargoDrop()
                            currTime = time.time()

                    currTime = time.time()
                    if (data[2] == 0):
                        time.sleep(lineTime)
                        setSpeed(A + D, speed)
                        break

        except brickpi3.SensorError as error:
            print(error)
except KeyboardInterrupt:
    allStop()