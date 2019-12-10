import math

def countAsteroidsInLoS(xx, yy, map, angles):
    angleList = []
    list = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '#':
                vx = x - xx
                vy = y - yy 
                angle = math.atan2(vx, vy)
       
                elem = ((x,y), angle)    
                angleList.append(elem)                             
                
                list.append(angle)

    angles[(xx,yy)] = list
    
    return len(set(list))



station = (30, 34)
filepath = 't.txt' 
with open(filepath) as fp: 	
    line = fp.readline().strip()
    map = []
    
    while line:
        map.append(list(line))
        line = fp.readline().strip()

    #end while
    
    dict = {} 
    angles = {} 

    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '#':
                dict[(x,y)] = countAsteroidsInLoS(x, y, map, angles)

    n = max(dict.values())
    print(n)

    #print(dict)
    #print(angles)
    #visibleAsteroids = dict.get(station)
    
            