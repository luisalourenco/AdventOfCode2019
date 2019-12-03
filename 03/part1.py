import numpy as np

filepath = 'input.txt' 

def manhattanDistance(x, y):
    return x + y

def fillWithWire(matrix, wire, getResult):
    x , y = 100, 100
    for p in wire:
        direction = p[0]
        step = int(p[1:])

        if direction == 'D':
            y -= step
        elif direction == 'U':
            y += step
        elif direction == 'L':
            x -= step
        elif direction == 'R':
            x += step

        if not getResult:
            matrix[x][y] = '-'
        else:
            if matrix[x][y] == '-':
                matrix[x][y] = 'X'
            else:
                matrix[x][y] = '+'
        
        

with open(filepath) as fp: 	
    matrix = np.chararray((10000, 10000))
    matrix[:] = '.'

    wire1 = fp.readline().strip().split(',')
    wire2 = fp.readline().strip().split(',')

    fillWithWire(matrix, wire1, False)
    fillWithWire(matrix, wire2, True)


    print matrix
    
    
