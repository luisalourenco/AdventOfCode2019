import time
import random
from multiprocessing import Process, Queue

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
        a = sequence[pc + 1]
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

def wait(sequence, a, inParam, pc, comp):
    sequence[a] = inParam 
    print("switching computer for "+ str(comp))
    return (pc+2, sequence)

def IntCode(sequence, relative, inParam, queues, states, nat, idle, init = False):
    # init positions
    comp = inParam

    #obtain state
    pc = states.get(comp)[0]
    sequence = states.get(comp)[1]
    print("[" + str(comp)+"] PC: " +str(pc))

    opCode = sequence[pc]
    
    x = None
    y = None

    dst = None
    readX = None
    readY = None
    sent= 0

    while opCode != 99:         
        
        (opCode, a, b, res) = treatInput(pc, sequence, relative)        

        if opCode == 1:
            sequence[res] = add(a, b)

        elif opCode == 2:
            sequence[res] = mul(a, b)
            
        #input
        elif opCode == 3:    

            if not init:
                # read queue for this computer
                queue = queues.get(comp)

                if len(queue) == 0:
                    if sent >= 30:
                        sequence[a] = inParam 
                        print("[" + str(comp)+"] Switching computer")
                        print("================")
                        return (pc+2, sequence)
                    if idle and comp == 0:
                        inParam = inParam
                    else:
                        inParam = -1
                    sent +=1
                else:

                    if readX == None: # read X
                        packet = queue[0]
                        inParam = packet[0]
                        readY = packet[1]
                        readX = packet[0]                        
                    else: # read Y, remove packet from queue
                        print("PACKET RECEIVED! ")
                        print("Queue: "+str(comp))
                        print("X: "+str(readX))
                        print("Y: "+str(readY))
                        print("=====")
                        queue.pop(0)
                        inParam = readY
                        readX = None
            
            else:
                print("booting: "+str(inParam))
                # init computer with its address
                comp = inParam
                # bootstrap
                sequence[a] = inParam 
                # sinalise the bootstrap is completed
                init = False                
                print("bootstrap ended for "+ str(comp))

                # return current state
                return (pc+2, sequence)

            sequence[a] = inParam 

        elif opCode == 4:

            if dst == None:
                dst = a
            elif x == None:
                x = a
            elif y == None: 
                y = a
                
                if dst == 255:
                    print("YYYY: "+ str(y))

                    if (x,y) in nat and idle: #repeating 255
                        return (pc+2, sequence)
                    nat.add((x,y))

                q = queues.get(dst)             
               
                q.append((x,y))
                queues[dst] = q
                
                print("PACKET SENT! ")
                print("Queue: "+str(dst))
                print("X: "+str(x))
                print("Y: "+str(y))
                print("=====")
                sent += 1
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
    queues = {}
    states = {}
    size = 50
    nat = set()
    idleMachines = {}

    relative = 0	
    myInput = fp.readline().strip().split(',')    
    myInput = [int(i) for i in myInput]
    myInput += [0]*10000

    for i in range(50):
        states[i] = (0, myInput.copy())
        queues[i] =  []   
        idleMachines[i] = 0   
    queues[255] =  []
    
    idle = False
    # bootstrap
    for addr in range(50):
        res, seq = IntCode(myInput.copy(), relative, addr, queues, states, nat, idle, True)
        states[addr] = (res, seq)

    exit = False    
    # run network
    for i in range(100):
        if exit:
            break
        if sum(idleMachines.values()) == 50:
            if len(queues.get(255)) != 0:
                inParam = queues.get(255)[0]
                idle = True

        for addr in range(50):
            res, seq = IntCode(myInput.copy(), relative, addr, queues, states, nat, idle)  
            idle = False          
            oldState = states.get(addr)
            if oldState == (res, seq):
                idleMachines[addr] = 1
            else:
                idleMachines[addr] = 0
            states[addr] = (res, seq)

            queue = queues.get(255)
            # solution is the first Y value that the NAT *sends* twice.
            #if len(queue) != 0:
            #    if queue[0] in nat:
            #        exit = True
            #        break
            #    else:
            #        nat.add(queue[0])
                
                
    #print(queues)
    
    
      
    