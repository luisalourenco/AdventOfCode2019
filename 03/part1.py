import sys
filepath = 'input.txt' 

def manhattanDistance(px, py, x, y):
    return abs(px - x) + abs(py - y)

def intersection(list1, list2): 
    return set(list1).intersection(list2) 

def buildPoints(wire):
    points = []
    x, y = 0, 0
    for p in wire:
        direction = p[0]
        step = int(p[1:])
        if direction == 'D':
            for i in range(0, step):
                y -= 1
                points.append((x,y))    
        elif direction == 'U':
            for i in range(0, step):
                y += 1
                points.append((x,y))
        elif direction == 'L':
            for i in range(0, step):
                x -= 1
                points.append((x,y))
        elif direction == 'R':
            for i in range(0, step):
                x += 1
                points.append((x,y)) 
    #end for
    return points

with open(filepath) as fp: 	    
    port = (0,0)
    wire1 = fp.readline().strip().split(',')
    wire2 = fp.readline().strip().split(',')
    point1 = buildPoints(wire1)
    point2 = buildPoints(wire2)
    
    commonPoints = intersection(point1, point2)
    min = sys.maxsize
    for p in commonPoints:
        distance = manhattanDistance(port[0], port[1], p[0], p[1])
        if distance < min:
            min = distance
    print(min)
