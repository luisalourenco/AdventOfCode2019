filepath = 'input.txt' 

def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def IntCode(sequence):
    # init positions
    pc = 0
    a = sequence[pc + 1]
    b = sequence[pc + 2]
    res = sequence[pc + 3]

    while sequence[pc] != 99:       
        if sequence[pc] == 1:
            sequence[res] = add(sequence[a], sequence[b])
        elif sequence[pc] == 2:
            sequence[res] = mul(sequence[a], sequence[b])
        pc = pc + 4
        a = sequence[pc + 1]
        b = sequence[pc + 2]
        res = sequence[pc + 3]
    return sequence

with open(filepath) as fp: 	
    input = fp.readline().strip().split(',')
    input = [int(i) for i in input]
    # replace position 1 with value 12, and replace position 2 with value 2.
    input[1] = 12
    input[2] = 2
    
    input = IntCode(input)
    print(input[0])

    
