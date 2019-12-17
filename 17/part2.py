import time
import random

def timer(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    f = func(*args, **kwargs)
    print(f'The function ran for {time.time() - start} s')
    return f
  return wrapper


@timer
def part1():
    return 0
  

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
    x = 0
    y = 0
    newline = False
    finishedMain = False
    finishedA = False
    finishedB = False
    finishedC = False
    lastPhase = False
    while opCode != 99:         

        (opCode, a, b, res) = treatInput(pc, sequence, relative)        
        
        if opCode == 1:
            sequence[res] = add(a, b)

        elif opCode == 2:
            sequence[res] = mul(a, b)
            
        #input
        elif opCode == 3:
            # max 20 chars
            # A 65, B 66, C, 67, D, 68
            # R 82, L 76
            # A 44 A 44 B 44 C 44 B 44 C 44 B 44 C 10
            # 10 44 L 44 8 44 R 44 6 10
            # y or n
            
            sequence[a] = ord(completeProgram.pop(0))

        elif opCode == 4:

 
            print(a)
            
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

    
    return map


def printMap(map, fileMode = True):
    if fileMode:
        file1 = open("MyFileAll.txt","w") 
    
        for l in map:
            for j in range(len(l)):
                file1.write(l[j])
            file1.write("\n")
        file1.close() 

def isIntersection(map, x, y):
    return map[y-1][x] == '#' and map[y + 1][x] == '#' and map[y][x -1] == '#' and map[y][x + 1] == '#'

def findRobot(map):
    for y in range(50):
        for x in range(50):
            if map[y][x] == '^':
                return (x,y)

def moveForward(robot, direction):
    x = robot[0]
    y = robot[1]
    # north
    if direction == 'U':
        return (x, y - 1)
    # east        
    elif direction == 'R':
        return (x + 1, y)  
    # south  
    elif direction == 'D':
        return (x, y + 1)
    # west     
    elif direction == 'L':
        return (x - 1, y)

def canMoveForward(robot, direction):
    x = robot[0]
    y = robot[1]
    # north
    if direction == 'U':
        if y > 0:
            return map[y - 1][x] == "#"
        else:
            return False    
    # east        
    if direction == 'R':
        if x < 50:
            return map[y][x + 1] == "#"
        else:
            return False
    # south  
    if direction == 'D':
        if y < 50:
            return map[y + 1][x] == "#"
        else:
            return False
    # west     
    if direction == 'L':
        if x > 0:
            return map[y][x - 1] == "#"
        else:
            return False

# rotate always R first
def rotatePosition(robot, direction):
    
    # up
    if direction == 'U':
        if canMoveForward(robot, 'R'):
            return 'R', 'R'
        elif canMoveForward(robot, 'L'):
            return 'L', 'L'
    # right        
    if direction == 'R':
        if canMoveForward(robot, 'D'):
            return 'D', 'R'
        elif canMoveForward(robot, 'U'):
            return 'U', 'L'
    # down  
    if direction == 'D':
        if canMoveForward(robot, 'R'):
            return 'R', 'L'
        elif canMoveForward(robot, 'L'):
            return 'L', 'R'
    # left     
    if direction == 'L':
        if canMoveForward(robot, 'D'):
            return 'D', 'L'
        elif canMoveForward(robot, 'U'):
            return 'U', 'R'
    return None, None

def findPath(map):
    (x,y) = findRobot(map)
    pos = "U"
    path = []
    positions = 0
    total = 0

    while True :

        canMove = canMoveForward((x,y), pos)
        if canMove:
            (xx, yy) = moveForward((x,y), pos)
            positions += 1
            total += 1    
            x = xx
            y = yy   
        else:
            path.append(str(positions))
            positions = 0
            pos, listPost = rotatePosition((x,y), pos)
            if pos == None:
                break
            path.append(listPost)        
        
    return (map, path)

filepath = 'input.txt' 

mainProg = list('A,B,A,B,C,B,C,A,B,C\n')
funA = list('R,4,R,10,R,8,R,4\n')
funB = list('R,10,R,6,R,4\n')
funC = list('R,4,L,12,R,6,L,12\n')

completeProgram = mainProg + funA + funB + funC + list('n\n')

with open(filepath) as fp: 
    # 200 by 200 map
    map = [ [ (' ') for i in range(50) ] for j in range(50) ] 
    

    relative = 0	
    myInput = fp.readline().strip().split(',')    
    myInput = [int(i) for i in myInput]
    myInput += [0]*10000
    
    #map = IntCode(myInput, relative, 1, map)
    
    #map[0][10] = '#'

    #(map, path) = findPath(map)
    #printMap(map)
    #print( ", ".join(path) )

    #Main: A,B,A,B,C,B,C,A,B,C
    #A: R,4,R,10,R,8,R,4
    #B: R,10,R,6,R,4
    #C: R,4,L,12,R,6,L,12
    
    # ord
    myInput[0] = 2
    map = IntCode(myInput, relative, 1, map)

   
   


    