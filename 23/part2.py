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


def IntCode(sequence, relative, inParam, queues, states, nat, idleVal, idle, init = False):
    # init positions
    comp = inParam

    #obtain state
    pc = states.get(comp)[0]
    sequence = states.get(comp)[1]
    #print("[" + str(comp)+"] PC: " +str(pc))

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
                    # wait 100 iterations before pausing
                    if sent >= 100:
                        sequence[a] = inParam 
                        print("Pausing computer [" + str(comp)+"] ")
                        print("================")
                        return (pc+2, sequence, queues)
                    else:
                        inParam = -1
                    sent +=1
                else:

                    if readX == None: # read X
                        packet = queue[0]
                        print(packet)
                        inParam = packet[0]
                        readY = packet[1]
                        readX = packet[0]                        
                    else: # read Y, remove packet from queue
                        print("<<< ========")
                        print("PACKET RECEIVED at computer [" + str(comp)+"]! ")
                        print("X: "+str(readX) +", Y: "+str(readY))
                        print("<<< ========")
                        print()
                        queue.pop(0)
                        inParam = readY
                        readX = None
            
            else:
                print("Booting computer [" + str(inParam)+"]")
                # init computer with its address
                comp = inParam
                # bootstrap
                sequence[a] = inParam 
                # sinalise the bootstrap is completed
                init = False                
                print("Bootstrap ended for computer "+ str(comp)+ ".")

                # return current state
                return (pc+2, sequence, queues)

            sequence[a] = inParam 

        elif opCode == 4:

            if dst == None:
                dst = a
            elif x == None:
                x = a
            elif y == None: 
                y = a
                # get destinatary queue
                q = queues.get(dst) 

                # if destinatary is NAT then replace value in queue
                if dst == 255: 
                    print("NAT PACKET: "+ str(y))
                    q = [(x,y)]   # only save last one  
                else:
                    q.append((x,y))
                queues[dst] = q

                print("======== >>>")
                print("PACKET SENT! ")
                print("Queue: "+str(dst))
                print("X: "+str(x))
                print("Y: "+str(y))
                print("======== >>>")
                print()
                sent += 1
                dst = None
                x = None
                y = None
                
                return (pc+2, sequence, queues)

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
    


filepath = 'input.txt' 
with open(filepath) as fp: 
    queues = {}
    states = {}
    oldStates = {}
    size = 50
    nat = set()
    idleMachines = {}

    relative = 0	
    myInput = fp.readline().strip().split(',')    
    myInput = [int(i) for i in myInput]
    myInput += [0]*10000

    # init vars
    for i in range(50):
        states[i] = (0, myInput.copy())
        queues[i] =  []   
        idleMachines[i] = 0   
    queues[255] =  []
    
    idle = False
    # bootstrap
    for addr in range(50):
        res, seq, q = IntCode(myInput.copy(), relative, addr, queues, states, nat, None, idle, True)
        states[addr] = (res, seq)
    print("===== END OF BOOTSTRAP =====")
    print()



    inParam = -1
    idleTimes = 0
    # iterations of machines executions
    for i in range(5000):

        # check if network is idle
        if sum(idleMachines.values()) == 50:
                natQueue = queues.get(255)
                if len(natQueue) != 0:
                    idleTimes += 1
                    if idleTimes == 100:
                        inParam = natQueue.pop(0)
                        print("Network is idle!")               
                        print(inParam)
                        idleTimes = 0
                        idle = True
                        print("Sending packet to 0 from NAT. Value " + str(inParam)+ "")
                        # send NAT packet to computer 0 queue
                        queues.get(0).append(inParam)
                        
        else:
            idleTimes = 0
        
        # run network
        for addr in range(50):
            print("Resuming computer "+ str(addr)+ ".")
           
            # save state
            oldStates[addr] = states.get(addr)
            oldState = oldStates.get(addr)
            # run program until stuck in reading 
            res, seq, q = IntCode(myInput.copy(), relative, addr, queues, states, nat, inParam, idle)  
            states[addr] = (res, seq)

            for i in range(50):
                if len(q.get(i)) != 0:
                    idleMachines[addr] = 0
                else:
                    idleMachines[addr] = 1

            
            print()
        #end for

    
      
    