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


def printMap(map, rating, fileMode = True):
    if fileMode:
        file1 = open("MyFileAll.txt","a") 
    
        for l in map:
            for j in range(len(l)):
                file1.write(l[j])
            file1.write("\n")
        file1.write("rating "+str(rating))
        file1.write("\n")
        file1.write("\n")
        file1.close() 



def bugsInAdjacentTiles(map, x, y):
    bugs = 0
    size = 5

    if y != 0:
        if map[y-1][x] == '#': 
            bugs += 1
    if y != size -1:
        if map[y + 1][x] == '#':
            bugs += 1
    if x != 0:
        if map[y][x -1] == '#':
            bugs += 1
    if x != size -1:
        if map[y][x + 1] == '#':
            bugs += 1
    return bugs


def mutation(map):
    newMap = [ [ '.' for i in range(5) ] for j in range(5) ]
    size = 5

    for y in range(size):
        for x in range(size):
            unchanged = True
            numBugs = bugsInAdjacentTiles(map, x, y)

            if map[y][x] == '#' and numBugs != 1:
                newMap[y][x] = '.'
                unchanged = False      
                
            if map[y][x] == '.' and (numBugs == 1 or numBugs == 2):
                newMap[y][x] = '#'
                unchanged = False

            if unchanged:
                newMap[y][x] = map[y][x]
            
    return newMap

def biodiversityRating(map):
    num = 0
    rating = 0
    for y in range(5):
        for x in range(5):
            if map[y][x] == '#':
                rating += pow(2, num)
            num +=1
    return rating

def part1(map):
    iterations = 200
    resultMap = map
    ratings = set()
    exit = False
    for i in range(iterations):
        
        if exit:
            break
        
        rating = biodiversityRating(resultMap)
        if rating in ratings:
            print(rating)
            exit = True
            break
        else:
            ratings.add(rating)
        
        resultMap = mutation(resultMap)
        printMap(resultMap, rating)

    return resultMap


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

    
    m = part1(map)

    
   