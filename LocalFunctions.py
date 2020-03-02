course = [[0 for i in range(20)] for j in range(10)]

def printMap():
    for i in course:
        for j in i:
            print(str(j), end=" ")
        print()
    pass