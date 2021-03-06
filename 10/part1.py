import math

def countAsteroidsInLoS(xx, yy, map, vectors):
    
    list = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '#':
                vx = x - xx
                vy = y - yy                                 
                list.append(math.atan2(vx, vy))

    vectors[(xx,yy)] = list
    
    return len(set(list))




filepath = 'input.txt' 
with open(filepath) as fp: 	
    line = fp.readline().strip()
    map = []
    
    while line:
        map.append(list(line))
        line = fp.readline().strip()
    #end while
    
    #points dictionary
    dict = {} 
    vectors = {} 

    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '#':
                dict[(x,y)] = countAsteroidsInLoS(x, y, map, vectors)

    n = max(dict.values())
    print(n)
    for a in dict:
        if dict.get(a) == n:
            print(a)
    
            