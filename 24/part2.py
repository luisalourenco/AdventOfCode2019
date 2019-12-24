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


def printMap(map, rating = None, fileMode = True):
    if fileMode:
        file1 = open("MyFileAll.txt","a") 
    
        for l in map:
            for j in range(len(l)):
                file1.write(l[j])
            file1.write("\n")
        if rating != None:
            file1.write("rating "+str(rating))
        file1.write("\n")
        file1.write("\n")
        file1.close() 



def bugsInAdjacentTiles(map, x, y, levels, level):
    bugs = 0
    size = 5
    # -1, 0 - lower border
    # 0, -1 - upper border
    # -1, -1 - right border
    # -2, -2 - left border

    # implement borders logic    


    # implement upper level logic
    # if x = 0 or x = 5, go up and down
    # if y = 0 or y = 5, 
    if y != 0:
        if map[y-1][x] == '#': 
            bugs += 1
        elif map[y-1][x] == '?':
            lowerLevel = levels.get(level-1)
            # search lower level in lower border
            bugs += bugsInAdjacentTiles(lowerLevel, -1, 0, levels, level -1)
    if y != size -1:
        if map[y + 1][x] == '#':
            bugs += 1
        elif map[y + 1][x] == '?':
            lowerLevel = levels.get(level-1)
            # search lower level in upper border
            bugs += bugsInAdjacentTiles(lowerLevel, 0, -1, levels, level -1)
    if x != 0:
        if map[y][x - 1] == '#':
            bugs += 1
        elif map[y][x - 1] == '?':
            lowerLevel = levels.get(level-1)
            # search lower level in right border
            bugs += bugsInAdjacentTiles(lowerLevel, -1, -1, levels, level -1)
    if x != size -1:
        if map[y][x + 1] == '#':
            bugs += 1
        elif map[y][x + 1] == '?':
            lowerLevel = levels.get(level-1)
            # search lower level in left border
            bugs += bugsInAdjacentTiles(lowerLevel, -2, -2, levels, level -1)
    return bugs


def mutation(levels):
    newMap = [ [ '.' for i in range(5) ] for j in range(5) ]
    size = 5
    level = 0
    newLevels = {}

    for map in range(len(levels.keys())):

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
        newLevels[level] = newMap.copy()
        level += 1
                
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

def part2(map):
    iterations = 10
    levels = {}
    resultMap = map
    levels[0] = map

    for i in range(iterations):
        resultMap = mutation(resultMap, levels)
    printMap(resultMap)

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

    
    m = part2(map)

    
   