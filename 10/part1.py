

def countAsteroidsInLoS(xx, yy, map, size, width):
    x = xx
    y = yy
    count = 0
    asteroid = map[yy][xx]
    left = map[yy][0:xx].count("#")
    right = map[yy][xx:size].count("#")

    if left > 0:
        count += 1
    if right > 0:
        count += 1


    y = 0
    #count upwards
    for line in map:
        #count left
        left = map[y][0:xx].count("#")
        right = map[y][xx:size].count("#")
        count = count + left + right

          
        #end while x 
        y += 1
    return count



width = 0
filepath = 't.txt' 
with open(filepath) as fp: 	
    line = fp.readline().strip()
    map = []
    size = 1
    
    while line:
        map.append(list(line))
        line = fp.readline().strip()
        width = len(list(line))
        size += 1
    #end while
    
    print(width)
    dict = {} 
    x = 0
    y = 0
    # move downards y+
    for l in map:
        # move right x+
        for asteroid in l:
            if asteroid == '#':
                #print((x,y) )
                
                dict[(x,y)] = countAsteroidsInLoS(x, y, map, size, width)
            x+= 1
        #end for right
        y+= 1
        x = 0
    #end for downards
        

    print(size)
    
    n = max(dict.values())
    print(n)
    
            