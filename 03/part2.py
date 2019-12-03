import sys
filepath = 'input.txt' 

def intersection(list1, list2): 
    return set(list1).intersection(list2) 

def computeSteps(x, y, step, steps):
    # build dictionary with steps for each point
    curr = 0
    if (x,y) in steps:
        curr = steps.get((x,y))       
    steps[(x,y)] = step + curr

    
def buildPoints(wire, steps):
    points = []
    x, y = 0, 0
    s = 0
    for p in wire:
        direction = p[0]
        step = int(p[1:])
        if direction == 'D':
            for i in range(0, step):
                y -= 1
                points.append((x,y)) 
                s += 1  
                computeSteps(x, y, s, steps)                                 
        elif direction == 'U':
            for i in range(0, step):
                y += 1
                points.append((x,y)) 
                s += 1  
                computeSteps(x, y, s, steps) 
        elif direction == 'L':
            for i in range(0, step):
                x -= 1
                points.append((x,y))
                s += 1  
                computeSteps(x, y, s, steps)   
        elif direction == 'R':
            for i in range(0, step):
                x += 1
                points.append((x,y))
                s += 1  
                computeSteps(x, y, s, steps)   
 
    #end for
    return points

with open(filepath) as fp: 	 
    steps = {}   
    port = (0,0)
    wire1 = fp.readline().strip().split(',')
    wire2 = fp.readline().strip().split(',')
    point1 = buildPoints(wire1, steps)
    point2 = buildPoints(wire2, steps)
    
    commonPoints = intersection(point1, point2)

    min = sys.maxsize
    for k in commonPoints:
        val = steps.get(k)
        if val < min:
            min = val
   
    print(min)
    
