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

def moveForward(robot, direction):
    x = robot[0]
    y = robot[1]
    # north
    if direction == '1':
        return (x, y - 1)
    # east        
    elif direction == '4':
        return (x + 1, y)  
    # south  
    elif direction == '2':
        return (x, y + 1)
    # west     
    elif direction == '3':
        return (x - 1, y)    
    
def pickDirection(map, x, y):
    # if unexplored, go!
    
    if map[y - 1][x] == ' ':
        return 1
    if map[y + 1][x] == ' ':
        return 2
    if map[y][x - 1] == ' ':
        return 3
    if map[y][x + 1] == ' ':
        return 4

    return random.randint(1,4)

def IntCode(sequence, relative, inParam, map):
    # init positions
    pc = 0
    opCode = sequence[pc]

    x = 21
    y = 21
    map[21][21] = 'D'
    steps = 0
    explored = 0
    while opCode != 99:         

        (opCode, a, b, res) = treatInput(pc, sequence, relative)        
        
        if opCode == 1:
            sequence[res] = add(a, b)

        elif opCode == 2:
            sequence[res] = mul(a, b)
            
        #input
        elif opCode == 3:
            #inParam = int(input())
            inParam = pickDirection(map, x, y)
            sequence[a] = inParam           

        elif opCode == 4:            
            coords = moveForward((x,y), str(inParam))
            xx = coords[0]
            yy = coords[1]

            if map[yy][xx] == ' ':
                explored += 1

            #hit a wall
            if a == 0:              
                map[yy][xx] = '#'
                xx = x
                yy = y
            # ok
            elif a == 1:
                map[y][x] = '.'
                map[yy][xx] = 'D'
                x = xx
                y = yy
            elif a == 2:
                map[y][x] = '.'     
                map[yy][xx] = 'O'
                #print( str(x) +", "+ str(y)  )
                break
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

    map[21][21] = 'D'
    
    return (map, explored)


def printMap(map, fileMode = True):
    if fileMode:
        file1 = open("MyFileAll.txt","w") 
    
        for l in map:
            for j in range(len(l)):
                file1.write(l[j])
            file1.write("\n")
        file1.close()
    

def buildGraph(map):
    graph = {}

    for y in range(1,40):
        for x in range(1,40):
            if map[y][x] == ' ':
                map[y][x] = '#'

            east = (x+1, y)
            west = (x-1, y)
            north = (x, y-1)
            south = (x, y+1)
            
            neighbours = []
            if map[east[1]][east[0]] == '.':
                neighbours.append(east)
            if map[west[1]][west[0]] == '.':
                neighbours.append(west)
            if map[north[1]][north[0]] == '.':
                neighbours.append(north)
            if map[south[1]][south[0]] == '.':
                neighbours.append(south)
            
            graph[(x,y)] = neighbours
    return graph

def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if graph[start] == None:
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths


def bfs(graph, start):
    explored = []
    queue = [start]
    steps = 0
    
    while queue:
        node = queue.pop(0)

        if node not in explored:
            explored.append(node)
            neighbours = graph.get(node)

            # add neighbours of node to queue
            for neighbour in neighbours:
                queue.append(neighbour)

    return steps


filepath = 'input.txt' 
with open(filepath) as fp: 
    # 200 by 200 map
    map = [ [ (' ') for i in range(41) ] for j in range(41) ] 
    

    relative = 0	
    myInput = fp.readline().strip().split(',')    
    myInput = [int(i) for i in myInput]
    myInput += [0]*300
    
    (map, steps) = IntCode(myInput, relative, 1, map)
  
    graph = buildGraph(map)
    oxygen = (36,33)

    steps = 0
    for y in range(1, 40):
        for x in range(1, 40):
            s = find_all_paths(graph, (x,y), oxygen)
            
            for p in s:
                #print(p)                
                if len(p) > steps:
                    steps = len(p)  


    #print(neighbours)

    print(steps)

