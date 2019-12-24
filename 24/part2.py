import time
from collections import deque
from itertools import permutations 
from itertools import combinations
import sys

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


def bugsInAdjacentTilesLowerLevel(map, x, y):
    # -1, 0 - lower border
    # 0, -1 - upper border
    # -1, -1 - right border
    # -2, -2 - left border

    bugs = 0
    # implement borders logic above
    if x == -1 and y == 0:
        for i in range(5):
            if map[4][i] == '#':
                bugs += 1
    if x == 0 and y == -1:
        for i in range(5):
            if map[0][i] == '#':
                    bugs += 1
    if x == -1 and y == -1:
        for i in range(5):
            if map[i][4] == '#':
                bugs += 1
    if x == -2 and y == -2:
        for i in range(5):
            if map[i][0] == '#':
                bugs += 1
    return bugs

def bugsInAdjacentTiles(map, x, y, levels, level):
    bugs = 0
    size = 5

    topMap = levels.get(level + 1)
    if topMap != None:
        lefTop = topMap[2][1]
        rightTop = topMap[2][3]
        top = topMap[1][2]
        bot = topMap[3][2]
        # implement upper level logic
        # if x = 0, compare with x,y? LeftTop
        # or x = 5,  ?x,y rightTop
        # if y = 0, ? top x,y Top
        # or y = 5 x,y ? bot Bot
        if x == 0:
            if lefTop == '#':
                bugs += 1
        if y == 0:
            if top == '#':
                bugs += 1
        if x == 4:
            if rightTop == '#':
                bugs += 1
        if y == 4:
            if bot == '#':
                bugs += 1

    if y != 0:
        if map[y-1][x] == '#': 
            bugs += 1
        if map[y-1][x] == '?':
            lowerLevel = levels.get(level-1)
            if lowerLevel != None:
                # search lower level in lower border
                bugs += bugsInAdjacentTilesLowerLevel(lowerLevel, -1, 0)
    
    if y != size -1:
        if map[y + 1][x] == '#':
            bugs += 1
        if map[y + 1][x] == '?':
            lowerLevel = levels.get(level-1)
            if lowerLevel != None:
                # search lower level in upper border
                bugs += bugsInAdjacentTilesLowerLevel(lowerLevel, 0, -1)
    
    if x != 0:
        if map[y][x - 1] == '#':
            bugs += 1
        if map[y][x - 1] == '?':
            lowerLevel = levels.get(level-1)
            if lowerLevel != None:
                # search lower level in right border
                bugs += bugsInAdjacentTilesLowerLevel(lowerLevel, -1, -1)
    
    if x != size -1:
        if map[y][x + 1] == '#':
            bugs += 1
        if map[y][x + 1] == '?':
            lowerLevel = levels.get(level-1)
            if lowerLevel != None:
                # search lower level in left border
                bugs += bugsInAdjacentTilesLowerLevel(lowerLevel, -2, -2)
    return bugs


def mutation(levels, levelSize, iteration):
    size = 5
    #level = 0
    newLevels = {}

    for level in range(-levelSize,levelSize):
        map = levels.get(level)

        newMap = [ [ '.' for i in range(5) ] for j in range(5) ]
        
        for y in range(size):
            for x in range(size):
                unchanged = True
                numBugs = bugsInAdjacentTiles(map, x, y, levels, level)

                if map[y][x] == '#' and numBugs != 1:
                    newMap[y][x] = '.'
                    unchanged = False      
                    
                if map[y][x] == '.' and (numBugs == 1 or numBugs == 2):
                    newMap[y][x] = '#'
                    unchanged = False

                if unchanged:
                    newMap[y][x] = map[y][x]
            #end for
        #end for
        newLevels[level] = newMap.copy()
        if level == -levelSize:
            printMap(newMap, level, iteration+1)
        else:
            printMap(newMap, level)
        #level += 1

    return (newMap, newLevels)

def biodiversityRating(map):
    num = 0
    rating = 0
    for y in range(5):
        for x in range(5):
            if map[y][x] == '#':
                rating += pow(2, num)
            num +=1
    return rating

def part2(map, iterations, size):
    levels = {}
    resultMap = map    

    # init levels maps for 1..100
    for i in range(-size, size):
        level = [ [ '.' for i in range(5) ] for j in range(5) ] 
        level[2][2] = '?'        
        levels[i] = level

    levels[0] = map
    newLevels = levels.copy()
    for i in range(iterations):
        #printMap(levels.get(0))
        (resultMap, newLevels) = mutation(newLevels, size, i)
    
    #for 
    
    #printMap(newLevels.get(0))

    return resultMap


filepath = 't.txt' 
with open(filepath) as fp: 	
    line = fp.readline().strip()
    map = [ [ '.' for i in range(5) ] for j in range(5) ] 

    j = 0
    while line:
        map[j] = list(line)
        j += 1
        line = fp.readline().strip()
    #end while

    
    m = part2(map, 10, 5)

    
   