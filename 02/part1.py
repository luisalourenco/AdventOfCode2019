filepath = 'input.txt' 

def add(a, b):
    return a + b

def mul(a, b):
    return a * b


with open(filepath) as fp: 	
    input = fp.readline().strip().split(',')
    input = [int(i) for i in input]
    print input
