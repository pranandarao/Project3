course = [[0 for i in range(20)] for j in range(10)]

def printMap():
    for i in course:
        for j in i:
            print(str(j), end=" ")
        print()
    pass


    initAngle = getData()[2]
    currAngle = getData()[2]
    speedt = -200
    if (deg < 0):
        setDPS(A, speedt)
        setDPS(D, -speedt)
    elif (deg >= 0):
        setDPS(A, -speedt)
        setDPS(D, speedt)
    while (abs(deg) - 7 >= abs(initAngle - currAngle)):
        if getData()[2] != 0:
            currAngle = getData()[2]
    allStop()