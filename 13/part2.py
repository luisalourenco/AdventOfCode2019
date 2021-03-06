#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def jumpIfTrue(a, b, pc):
    if a != 0:
        return b
    else:
        return pc + 3

def jumpIfFalse(a, b, pc):
    if a == 0:
        return b
    else: 
        return pc + 3

def lessThan(a, b):
    if a < b:
        return 1
    else:
        return 0

def equals(a, b):
    if a == b:
        return 1
    else:
        return 0

def nextStep(opCode):
    if opCode == 1 or opCode == 2 or opCode == 7 or opCode == 8:
         return 4
    elif opCode == 3 or opCode == 4 or opCode == 9:
        return 2
    else:
        return 0

def getParameterValue(parameterMode, val, sequence, relative, writeMode = False):
    if parameterMode == 0 and writeMode:
        return val
    if parameterMode == 2 and writeMode:
        return relative + val

    if parameterMode == 0:
        return sequence[val] 
    elif parameterMode == 1:
        return val
    elif parameterMode == 2:
        return sequence[relative + val]


# (opCode, a, b, res)
def treatInput(pc, sequence, relative):
    instruction = str(sequence[pc])
    instruction = instruction.zfill(5)
    #print(instruction)

    opCode = int(instruction[3:5])
    resMode = int(instruction[0])
    leftMode = int(instruction[2])
    rightMode = int(instruction[1])    
    

    #print(opCode)
    #print(leftMode)
    #print(rightMode)
    #print(resMode)

    if opCode == 99:
        return (99, 0, 0, 0)

    if opCode == 9:
        a = sequence[pc + 1] 
        a = getParameterValue(leftMode, a, sequence, relative)

        return (opCode, a, 0, 0)
    if opCode == 5 or opCode == 6:
        a =  sequence[pc + 1]
        b =  sequence[pc + 2]
        a = getParameterValue(leftMode, a, sequence, relative)
        b = getParameterValue(rightMode, b, sequence, relative)
        
        return (opCode, a, b, 0)
    if opCode == 1 or opCode == 2 or opCode == 7 or opCode == 8:
        a =  sequence[pc + 1]
        b =  sequence[pc + 2]
        res = sequence[pc + 3]
        
        a = getParameterValue(leftMode, a, sequence, relative)
        b = getParameterValue(rightMode, b, sequence, relative)
        res = getParameterValue(resMode, res, sequence, relative, True)

        return (opCode, a, b, res)
    if opCode == 3 or opCode == 4:       
        a =  sequence[pc + 1]
        a = getParameterValue(leftMode, a, sequence, relative, opCode == 3)

        return (opCode, a, 0, 0)


def newDirection(direction, out):
    if out == 0: # turn left
        if direction == 'U':
            return 'L'
        elif direction == 'L':
            return  'D'
        elif direction == 'D':
            return  'R'
        elif direction == 'R':
            return  'U'
    else: # turn right
        if direction == 'U':
            return  'R'
        elif direction == 'R':
            return 'D'
        elif direction == 'D':
            return  'L'
        elif direction == 'L':
            return  'U'

def moveForward(robot, direction):
    x = robot[0]
    y = robot[1]
    if direction == 'U':
        return (x, y - 1)        
    elif direction == 'R':
        return (x + 1, y)    
    elif direction == 'D':
        return (x, y + 1)     
    elif direction == 'L':
        return (x - 1, y)    
    

def getBallPosition(map):
    for line in map:
        for x in range(len(line)):
            if line[x] == '.':
                return x
    return -1

def getPaddlePosition(map):
    for line in map:
        for x in range(len(line)):
            if line[x] == '_':
                return x
    return -1

def IntCode(sequence, relative, inParam, map):
    # init positions
    pc = 0
    opCode = sequence[pc]
    xOut = True
    yOut = False
    idOut = False
    allOut = False
    score = 0
    x = 0
    y = 0

    while opCode != 99:  
        (opCode, a, b, res) = treatInput(pc, sequence, relative)
        
        
        if opCode == 1:
            #print("res pos: "+str(res))
            sequence[res] = add(a, b)

        elif opCode == 2:
            sequence[res] = mul(a, b)
            
        #input
        elif opCode == 3:
            printMap(map)
            printMap(map,True)
            ball = getBallPosition(map)
            paddle = getPaddlePosition(map)
            
            if ball < paddle:
                inParam = -1
            elif ball == paddle:
                inParam = 0
            elif ball > paddle:
                inParam = 1
            #inParam = int(input())
            sequence[a] = inParam           

        elif opCode == 4:
            
            if xOut:
                x = a
                xOut = False
                yOut = True
                idOut = False
            elif yOut:
                y = a
                xOut = False
                yOut = False
                idOut = True
            elif idOut:
                id = a
                xOut = True
                yOut = False
                idOut = False
                allOut = True
            
            if allOut:
                allOut = False

                if x == -1 and y == 0:
                    score = a
                    print("Score: " + str(id))
                else:
                    if id == 0:
                        map[y][x] = ' '
                    if id == 1:
                        map[y][x] = '*'
                    #block
                    if id == 2:
                        map[y][x] = '#'
                    if id == 3:
                        map[y][x] = '_'
                    if id == 4:
                        map[y][x] = '.'         
            #print(a)

            
        elif opCode == 5:
            pc = jumpIfTrue(a, b, pc)
            
        elif opCode == 6:
            pc = jumpIfFalse(a, b, pc)

        elif opCode == 7:
            sequence[res] = lessThan(a, b)

        elif opCode == 8:
            sequence[res] = equals(a, b)            

        elif opCode == 9:
            relative += a                
           
        
        if  opCode != 6 and opCode != 5:
            pc += nextStep(opCode)
        #print("pc: "+str(pc))
        #print(sequence)

    
    return score


def printMap(map, fileMode = False):
    if fileMode:
        file1 = open("MyFile.txt","a") 
    
        for l in map:
            for j in range(len(l)):
                file1.write(l[j])
            file1.write("\n")
        file1.close()
    else:
        for l in map:
            for j in range(len(l)):
                print(l[j], end = '')
            print()



filepath = 'input.txt' 
with open(filepath) as fp: 
    # 200 by 200 map
    map = [ [ (' ') for i in range(100) ] for j in range(100) ] 


    relative = 0	
    myInput = fp.readline().strip().split(',')    
    myInput = [int(i) for i in myInput]
    myInput += [0]*300

    #quarters
    myInput[0] = 2

    maxScore = 0
    score = IntCode(myInput, relative, 1, map)
        
    print(score)

    #printMap(map, True)
    #printMap(map)


    #print(count)
    
