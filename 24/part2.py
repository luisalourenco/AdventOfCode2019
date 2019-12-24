import time

def timer(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    f = func(*args, **kwargs)
    print(f'The function ran for {time.time() - start} s')
    return f
  return wrapper


def printMap(map, level = None, iteration = None, fileMode = True):
    if fileMode:
        file1 = open("MyFileAll.txt","a") 
        
        if iteration != None:
            file1.write("Time: "+str(iteration))
        file1.write("\n")

        if level != None:
            file1.write("Level "+str(level))
        file1.write("\n")
        
        for l in map:
            for j in range(len(l)):
                file1.write(l[j])
            file1.write("\n")
        file1.write("\n")
        file1.write("\n")
        file1.close() 


def bugsInAdjacentTilesLowerLevel(map, border):
    # -1, 0 - lower border
    # 0, -1 - upper border
    # -1, -1 - right border
    # -2, -2 - left border

    bugs = 0
    if border == 'DOWN':
        for i in range(5):
            if map[4][i] == '#':
                bugs += 1
    if border == 'UP':
        for i in range(5):
            if map[0][i] == '#':
                bugs += 1
    if border == 'RIGHT':
        for i in range(5):
            if map[i][4] == '#':
                bugs += 1
    if border == 'LEFT':
        for i in range(5):
            if map[i][0] == '#':
                bugs += 1
    return bugs

def bugsInAdjacentTilesUpperLevel(map, x, y):
    bugs = 0
    if map != None:
        left = map[2][1]
        right = map[2][3]
        up = map[1][2]
        down = map[3][2] 

        if x == 0:
            if left == '#':
                bugs += 1

        if y == 0:
            if up == '#':
                bugs += 1

        if x == 4:
            if right == '#':
                bugs += 1

        if y == 4:
            if down == '#':
                bugs += 1
    return bugs

def bugsInAdjacentTiles(map, x, y, levels, level):
    bugs = 0
    size = 5

    upperMap = levels.get(level + 1)   
    bugs += bugsInAdjacentTilesUpperLevel(upperMap, x, y)

    lowerLevel = levels.get(level-1)
    if lowerLevel != None:
        if (x,y) == (2,1): # upper
            bugs += bugsInAdjacentTilesLowerLevel(lowerLevel, 'UP')
        if (x,y) == (1,2): # left
            bugs += bugsInAdjacentTilesLowerLevel(lowerLevel, 'LEFT')
        if (x,y) == (3,2): # right
            bugs += bugsInAdjacentTilesLowerLevel(lowerLevel, 'RIGHT')
        if (x,y) == (2,3): # down
            bugs += bugsInAdjacentTilesLowerLevel(lowerLevel, 'DOWN')

    if y != 0:
        if map[y-1][x] == '#': 
            bugs += 1
    
    if y != size -1:
        if map[y + 1][x] == '#':
            bugs += 1
    
    if x != 0:
        if map[y][x - 1] == '#':
            bugs += 1
    
    if x != size -1:
        if map[y][x + 1] == '#':
            bugs += 1
        
    return bugs


def mutation(levels, levelSize, iteration):
    size = 5
    newLevels = {}

    for level in range(-levelSize, levelSize):
        # current map
        map = levels.get(level)
        # map after mutation
        newMap = [ [ '.' for i in range(5) ] for j in range(5) ]
        
        for y in range(size):
            for x in range(size):
                unchanged = True
                if (x,y) != (2,2):
                    # count bugs in adjacent tiles, including edge cases with lower and upper level
                    numBugs = bugsInAdjacentTiles(map, x, y, levels, level)

                    # bug dies unless there is exactly one bug adjacent to it
                    if map[y][x] == '#' and numBugs != 1:
                        newMap[y][x] = '.'
                        unchanged = False      
                    # empty space becomes infested with a bug if exactly one or two bugs are adjacent to it
                    if map[y][x] == '.' and (numBugs == 1 or numBugs == 2):
                        newMap[y][x] = '#'
                        unchanged = False

                    # otherwise, nothing changes
                if unchanged:
                    newMap[y][x] = map[y][x]
            #end for
        #end for
        # update current level's map
        newLevels[level] = newMap.copy()

        # printing map for debugging
        if level == -levelSize:
            printMap(newMap, level, iteration+1)
        else:
            printMap(newMap, level)

    return newLevels


def countBugsAllLevels(levels):
    bugs = 0
    for map in levels.values():
        for y in range(5):
            for x in range(5):
                if map[y][x] == '#':
                    bugs += 1
    return bugs

@timer
def part2(map, iterations, size):
    levels = {}

    # init levels maps for -size..size
    for i in range(-size, size):
        level = [ [ '.' for i in range(5) ] for j in range(5) ] 
        level[2][2] = '?'        
        levels[i] = level

    levels[0] = map
    newLevels = levels.copy()

    for i in range(iterations):
        # feed next iteration with resulting levels maps
        newLevels = mutation(newLevels, size, i)
    
    # count bugs for all levels
    print(countBugsAllLevels(newLevels)) 
    

filepath = 'input.txt' 
with open(filepath) as fp: 	
    line = fp.readline().strip()
    map = [ [ '.' for i in range(5) ] for j in range(5) ] 

    j = 0
    while line:
        map[j] = list(line)
        j += 1
        line = fp.readline().strip()
    #end while

    # part2(map, iterations, size)
    part2(map, 200, 110)

    
   