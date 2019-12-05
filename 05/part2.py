filepath = 'input.txt' 

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
    else:
        return 2

# (opCode, a, b, res)
def treatInput(pc, sequence):
    instruction = str(sequence[pc])
    instruction = instruction.zfill(4)

    opCode = int(instruction[2:4])
    leftMode = int(instruction[1])
    rightMode = int(instruction[0])

    if opCode == 99:
        return (99, 0, 0, 0)
    if opCode == 5 or opCode == 6:
        a =  sequence[pc + 1]
        b =  sequence[pc + 2]
        if leftMode == 0:
            a = sequence[a]
        if rightMode == 0:
            b = sequence[b]
        return (opCode, a, b, 0)
    if opCode == 1 or opCode == 2 or opCode == 7 or opCode == 8:
        a =  sequence[pc + 1]
        b =  sequence[pc + 2]
        if leftMode == 0:
            a = sequence[a]
        if rightMode == 0:
            b = sequence[b]
        res = sequence[pc + 3]
        return (opCode, a, b, res)
    if opCode == 3 or opCode == 4:
        return (opCode, 0, 0, 0)


def IntCode(sequence):
    # init positions
    pc = 0
    opCode = sequence[pc]

    while opCode != 99:  

        (opCode, a, b, res) = treatInput(pc, sequence)

        if opCode == 1:
            sequence[res] = add(a, b)

        elif opCode == 2:
            sequence[res] = mul(a, b)
        
        elif opCode == 7:
            sequence[res] = lessThan(a, b)

        elif opCode == 8:
            sequence[res] = equals(a, b)

        elif opCode == 5:
            pc = jumpIfTrue(a, b, pc)
        
        elif opCode == 6:
            pc = jumpIfFalse(a, b, pc)
        
        #input
        elif opCode == 3:
            a = sequence[pc + 1]
            sequence[a] = 5

        elif opCode == 4:
            a = sequence[pc + 1]
            print(sequence[a])
        
        if  opCode != 6 and opCode != 5:
            pc += nextStep(opCode)

    return sequence

with open(filepath) as fp: 	
    input = fp.readline().strip().split(',')    
    input = [int(i) for i in input]
    
    input = IntCode(input)

    
