import time
import random
from multiprocessing import Process

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

def IntCode(sequence, relative, inParam, map, computers):
    # init positions
    pc = 0
    opCode = sequence[pc]
    comp = inParam
    x = None
    y = None

    dst = None
    readX = None
    readY = None
    #print("(" +str(x) +", "+ str(y)+ ")")
    init = True
    while opCode != 99:         
        
        (opCode, a, b, res) = treatInput(pc, sequence, relative)        

        if opCode == 1:
            sequence[res] = add(a, b)

        elif opCode == 2:
            sequence[res] = mul(a, b)
            
        #input
        elif opCode == 3:    

            print(computers)        
            if not init:
                # read queue for this computer
                queue = computers.get(comp)
                if queue == None or len(queue) == 0:
                    inParam = -1
                else:
                    if readX == None:
                        packet = queue.pop(0)
                        inParam = packet[0]
                        readY = packet[1]
                        readX = packet[0]
                    else:
                        print("PACKET RECEIVED! ")
                        print("Queue: "+str(comp))
                        print("X: "+str(readX))
                        print("Y: "+str(readY))
                        print("=====")
                        inParam = readY
                        readX = None
            
            else:
                print("booting: "+str(inParam))
                comp = inParam
                init = False

            sequence[a] = inParam 

        elif opCode == 4:


            if dst == None:
                dst = a
            elif x == None:
                x = a
            elif y == None:
                y = a
                
                if dst == 255:
                    print("Y: "+ str(y))

                q = computers.get(dst)              

                if q == None:
                    computers[dst] = [(x,y)]

                    print("PACKET SENT FROM " + str(comp))
                    print("Queue: "+str(dst))
                    print("X: "+str(x))
                    print("Y: "+str(y))
                    print("=====")
                else: 
                    q.append((x,y))
                    computers[dst] = q

                    print("PACKET SENT! ")
                    print("Queue: "+str(dst))
                    print("X: "+str(x))
                    print("Y: "+str(y))
                    print("=====")

                    dst = None
                    x = None
                    y = None
                

            #print("COMP: " + str(comp) + ", out: "+ str(a))

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
    computers = {}
    size = 50
    # 200 by 200 map
    map = [ [ 0 for i in range(size) ] for j in range(size) ] 
    mapFile = open("MyMap.txt","w") 

    relative = 0	
    myInput = fp.readline().strip().split(',')    
    myInput = [int(i) for i in myInput]
    myInput += [0]*10000


    for addr in range(50):
        p = Process(target=IntCode, args =[myInput.copy(), relative, addr, map, computers] ) 
        #res = IntCode(myInput.copy(), relative, addr, map, computers)
        p.start()
        #print(res)

    