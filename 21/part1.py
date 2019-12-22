import time
import random

def timer(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    f = func(*args, **kwargs)
    print(f'The function ran for {time.time() - start} s')
    return f
  return wrapper
  

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

def IntCode(sequence, relative, completeProgram, map):
    # init positions
    pc = 0
    opCode = sequence[pc]

    #print("(" +str(x) +", "+ str(y)+ ")")
    while opCode != 99:         
        
        (opCode, a, b, res) = treatInput(pc, sequence, relative)        

        if opCode == 1:
            sequence[res] = add(a, b)

        elif opCode == 2:
            sequence[res] = mul(a, b)
            
        #input
        elif opCode == 3:    
            sequence[a] = (completeProgram.pop(0))
            #sequence[a] = ord(completeProgram.pop(0))
            #sequence[a] = inParam           

        elif opCode == 4:
            if a > 255:
                return print(a)
            else:
                print(chr(a), end="")
            
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

    
    return a


def printMap(map, fileMode = True):
    if fileMode:
        file1 = open("MyFileAll.txt","w") 
    
        for l in map:
            for j in range(len(l)):
                file1.write(l[j])
            file1.write("\n")
        file1.close() 


def printMap2(map, fileMode = True):
    if fileMode:
        file1 = open("MyFileAll.txt","w") 
    
        for l in map:
            for j in range(len(l)):
                file1.write(str(l[j]))
            file1.write("\n")
        file1.close() 




filepath = 'input.txt' 
with open(filepath) as fp: 
    # 200 by 200 map
    map = [ [ 0 for i in range(50) ] for j in range(50) ] 
    mapFile = open("output.txt","w") 

    relative = 0	
    myInput = fp.readline().strip().split(',')    
    myInput = [int(i) for i in myInput]
    myInput += [0]*10000


    with open('program.txt') as prog:   
        program = "" 
        line = prog.readline().strip()  
        completeProgram = []
        while line:
            program += line
            line = prog.readline().strip()  
            completeProgram.append(line)
        #print(program)
        #completeProgram = list(program)

        # ((!A | !B | !C) && D ) 
        part1 = "NOT A J\n" + \
             "NOT B T\n" + \
            "OR T J\n" + \
            "NOT C T\n" + \
            "OR T J\n" + \
            "AND D J\n" + \
            "WALK\n"

        # ((!A | !B | !C) && D ) && (E | H)
        part2 = "NOT A J\n" + \
            "NOT B T\n" + \
            "OR T J\n" + \
            "NOT C T\n" + \
            "OR T J\n" + \
            "AND D J\n" + \
            "NOT E T\n" + \
            "NOT T T\n" + \
            "OR H T\n" + \
            "AND T J\n" + \
            "RUN\n"


        print(part2)
        p  = [ord(char) for char in part1]

        #completeProgram= list('NOT A J\nNOT B J\nAND T J\nNOT C J\nAND T J\nNOT A J\nAND B T\nNOT C J\nAND T J\nNOT D J\nAND T J\nNOT A T\nOR T J\nWALK\n')
        res = IntCode(myInput.copy(), relative, p, map)
    

    