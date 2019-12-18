import time
from collections import deque
from itertools import permutations 
from itertools import combinations

def timer(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    f = func(*args, **kwargs)
    print(f'The function ran for {time.time() - start} s')
    return f
  return wrapper

def buildGraph(map):
    graph = {}
    sizeX = len(map[0])
    sizeY = len(map)


    for y in range(1,sizeY-1):
        for x in range(1,sizeX-1):

            east = (x+1, y)
            west = (x-1, y)
            north = (x, y-1)
            south = (x, y+1)
            
            neighbours = []
            if map[y][x] != ' ' and map[y][x] != '#':
                if map[east[1]][east[0]] != ' ' and map[east[1]][east[0]] != '#':
                    neighbours.append(east)
                if map[west[1]][west[0]] != ' ' and map[west[1]][west[0]] != '#':
                    neighbours.append(west)
                if map[north[1]][north[0]] != ' ' and map[north[1]][north[0]] != '#':
                    neighbours.append(north)
                if map[south[1]][south[0]] != ' ' and map[south[1]][south[0]] != '#':
                    neighbours.append(south)
            
            graph[(x,y)] = neighbours
    return graph

def find_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        for node in graph[start]:
            if node not in path:
                newpath = find_path(graph, node, end, path)
                if newpath: return newpath
        return None

def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if graph[start] == None:
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

def find_shortest_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        
        if graph.get(start) == None:
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest 

def bfs(graph, start):
    explored = []
    queue = [start]
    steps = 0
    
    while queue:
        node = queue.pop(0)

        if node not in explored:
            explored.append(node)
            neighbours = graph.get(node)

            # add neighbours of node to queue
            for neighbour in neighbours:
                queue.append(neighbour)

    return steps

def printMap(map, fileMode = True):
    if fileMode:
        file1 = open("MyFileAll.txt","w") 
    
        for l in map:
            for j in range(len(l)):
                file1.write(l[j])
            file1.write("\n")
        file1.close() 

def gatherLocations(map):
    keys = []
    doors = []
    entrance = None
    sizeX = len(map[0])
    sizeY = len(map)

    for j in range(sizeY):
        for i in range(sizeX):
            obj = map[j][i]
            if obj != '@':
                if str.islower(obj):
                    #keys[obj] = (i,j)                    
                    keys.append((i,j))
                elif str.isupper(obj):
                    #doors[obj] = (i,j)
                    doors.append((i,j))
            else:
                entrance = (i,j)
    return keys, doors, entrance

def find_shortest_path2(graph, start, end):
        dist = {start: [start]}
        q = [start]
        while len(q):

            at = q.pop(0)            
            for next in graph.get(at):
                if next not in dist:
                    dist[next] = [dist[at], next]
                    q.append(next)
        return dist.get(end)

def printGraph(graph):
    for k in graph:
        nodes = graph.get(k)
        if nodes != None:
            print(str(k) + " => " + str(nodes))

@timer
def part1(map, debug=False):
    keys, doors, entrance = gatherLocations(map)
    graph = buildGraph(map)

    all = keys
    all.sort()
    #print(all)

    l = permutations(all)
    
    if not debug:
        start = entrance
        result = []
        for p in l:
            sum = 0
            start = entrance
            #print("permutation: "+ str(p))
            for end in p:
                path = find_shortest_path(graph, start, end)    
                #print("distance between "+ str(start) + " and " + str(end) + ": " + str(len(path))  )

                sum += len(path) - 1
                start = end
            #print("permutation had "+ str(sum) + " steps")
            #print("=====================")
            result.append(sum)
        return result




filepath = 't.txt' 
with open(filepath) as fp: 	
    line = fp.readline().strip()
    size = len(line)
    aux = [ [ ('') for i in range(size) ] for j in range(size) ]     
    j = 0
    while line:
        for i in range(size):
            aux[j][i] = line[i]
        j += 1
        line = fp.readline().strip()
    #end while
    map = [ [ ('') for i in range(size) ] for j in range(j) ]     
    
    #copy to correct size structure
    for y in range(j):
        for x in range(size):
            map[y][x] = aux[y][x]

    printMap(map)

    result = part1(map)
    print(min(result))