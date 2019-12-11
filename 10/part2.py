import math

def countAsteroidsInLoS(xx, yy, map, angles):
    #angleList = []
    list = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '#':
                vx = x - xx
                vy = y - yy 
                angle = math.atan2(vx, vy)       
                
                elem = (x, y, angle)    
                #angleList.append( elem )                             
                
                list.append(elem)

    angles[(xx,yy)] = list
    
    return len(set(list))

def getVisibleAsteroidsFromStation(map, station):
    
    angles = {} 
    countAsteroidsInLoS(station[0], station[1], map, angles)
    #list(set(angles.get(station)))

    visibleAsteroids = list(set(angles.get(station)))
    visibleAsteroids.sort(key=lambda tup: tup[2]) 
    #visibleAsteroids.sort()
    #print(visibleAsteroids)
    #visibleAsteroids.reverse()
    return visibleAsteroids

station = (30, 34)
filepath = 'input.txt' 
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



    vaporisedAsteroids = []
    startingAngle = math.atan2(30-30, 25-34)

    
    currentAngle = startingAngle
    fullRotation = True
    while True:
        # full rotation, get new visible asteroids
        if currentAngle == startingAngle and fullRotation:
            visibleAsteroids = getVisibleAsteroidsFromStation(map, station)
            fullRotation = False
        # list is ordered in reverse so we can pop
        currentAngle = visibleAsteroids.pop()
        #zap asteroid!
        map[currentAngle[1]][currentAngle[0]] = '.'
        
        while True:
            aux = visibleAsteroids.pop()
            if aux[2] != currentAngle[2]:
                visibleAsteroids.append(aux)
                break
               
        vaporisedAsteroids.append(currentAngle)        
        if len(vaporisedAsteroids) == 200:
            break

    #print(vaporisedAsteroids)
    print(vaporisedAsteroids[199])

    
            