import time
from collections import deque

def timer(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    f = func(*args, **kwargs)
    print(f'The function ran for {time.time() - start} s')
    return f
  return wrapper

def buildGraph(map):
    graph = {}

    for y in range(1,99):
        for x in range(1,99):

            east = (x+1, y)
            west = (x-1, y)
            north = (x, y-1)
            south = (x, y+1)
            
            neighbours = []
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
    keys = {}
    doors = {}
    entrance = None
    for j in range(100):
        for i in range(100):
            obj = map[j][i]
            if obj != '@':
                if str.islower(obj):
                    keys[obj] = (i,j)                    
                elif str.isupper(obj):
                    doors[obj] = (i,j)
            else:
                entrance = (i,j)
    return keys, doors, entrance


map = [ [ ('') for i in range(100) ] for j in range(100) ] 
filepath = 't.txt' 
with open(filepath) as fp: 	
    line = fp.readline().strip()
    
    j = 0
    while line:
        for i in range(len(line)):
            map[j][i] = line[i]
        j += 1
        line = fp.readline().strip()
    #end while

    printMap(map)
    keys, doors, entrance = gatherLocations(map)
    graph = buildGraph(map)

    