

def countAsteroidsInLoS(xx, yy, map, vectors):
    
    list = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '#':
                vx = x - xx
                vy = y - yy                   
                list.append((vx, vy))

    vectors[(xx,yy)] = list
    print(len((list)))
    print (vectors.get((xx,yy)))
    return len(set(list))



width = 0
filepath = 't.txt' 
with open(filepath) as fp: 	
    line = fp.readline().strip()
    map = []
    
    while line:
        map.append(list(line))
        line = fp.readline().strip()
        width = len(list(line))
    #end while
    
    #points dictionary
    dict = {} 
    vectors = {} 

    # move downards y+
    for y in range(len(map)):
        # move right x+
        for x in range(len(map[y])):
            if map[y][x] == '#':
                print((x,y) )
                #dict[(x,y)] = countAsteroidsInLoS(x, y, map, vectors)

        #end for right

    #end for downards

    print(countAsteroidsInLoS(6, 3, map, vectors))
    #n = max(dict.values())
    #print(n)
    
            