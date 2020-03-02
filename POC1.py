from MPU9250 import MPU9250
from Functions import setDPS, setPower, setSpeed, allStop, stop, getData, checkDist, travDist, turn, navPointX, navPointY, navigate 
import grovepi
import brickpi3
import time
import math

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

#Failsafes and Modes
lineMode = True
powerMode = False
cargoMode = False

#Setup
BP.set_sensor_type(one, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(two, BP.SENSOR_TYPE.TOUCH)
#BP.set_sensor_type(four, BP.SENSOR_TYPE.CUSTOM, [(BP.SENSOR_CUSTOM.PIN1_ADC)])

#Main Area
allStop()
powerMode = False
initTime = time.time()

try:
    while True:
        try:
            #Control Logic
            data = getData()
            print(data)
            
            if (data[0] == 1):
                navPointY(100,50)
            
            #checkDist(data)

        except brickpi3.SensorError as error:
            print(error)
except KeyboardInterrupt:
    allStop()
