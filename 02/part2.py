filepath = 'input.txt' 

def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def IntCode(sequence):
    # init positions
    pc = 0
    noun = sequence[pc + 1]
    verb = sequence[pc + 2]
    res = sequence[pc + 3]

    while sequence[pc] != 99:       
        if sequence[pc] == 1:
            sequence[res] = add(sequence[noun], sequence[verb])
        elif sequence[pc] == 2:
            sequence[res] = mul(sequence[noun], sequence[verb])
        pc = pc + 4
        noun = sequence[pc + 1]
        verb = sequence[pc + 2]
        res = sequence[pc + 3]
    return sequence

with open(filepath) as fp: 	
    input = fp.readline().strip().split(',')
    input = [int(i) for i in input]
    found = False

    for noun in range(0, 99):
        for verb in range(0, 99):
            cycle = input.copy()            
            cycle[1] = noun
            cycle[2] = verb

            cycle = IntCode(cycle)
            if cycle[0] == 19690720:
                print(noun)
                print(verb)
                found = True
                break
        if found:
            break


    
