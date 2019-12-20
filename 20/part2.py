import time
from collections import deque


def timer(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    f = func(*args, **kwargs)
    print(f'The function ran for {time.time() - start} s')
    return f
  return wrapper

def buildGraph(map, portals, level, ZZ):
    graph = {}
    sizeX = len(map[0])
    sizeY = len(map)

    for y in range(1,sizeY-1):
        for x in range(1,sizeX-1):

            east =  (x+1, y, level)
            west =  (x-1, y, level)
            north =  (x, y-1, level)
            south =  (x, y+1, level)
            
            neighbours = []
       
            if map[y][x] == '.':
                if map[east[1]][east[0]] == '.' :
                    neighbours.append(east)
                if map[west[1]][west[0]] == '.' :
                    neighbours.append(west)
                if map[north[1]][north[0]] == '.':
                    neighbours.append(north)
                if map[south[1]][south[0]] == '.': 
                    neighbours.append(south)
            
            graph[(x,y, level)] = neighbours
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
        steps+=1

        if node not in explored:            
            explored.append(node)
            neighbours = graph.get(node)

            # add neighbours of node to queue
            for neighbour in neighbours:
                queue.append(neighbour)
    
    return explored


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



def printGraph(graph, filter = True):
    for k in graph:
        nodes = graph.get(k)
        if nodes != None:
            if nodes != [] and filter:
                print(str(k) + " => " + str(nodes))

def printMap(map, fileMode = False):
    if fileMode:
        file1 = open("MyFileAll.txt","w") 
    
        for l in map:
            for j in range(len(l)):
                file1.write(l[j])
            file1.write("\n")
        file1.close() 
    else:
        for l in map:
            print("".join(l))

def findPortalPosition(map, i, j, isFwd):
    if isFwd:
        if map[j][i+2] == '.':
            return (i+2, j)
        if map[j][i-1] == '.':
            return (i-1, j)
    else:
        if map[j+2][i] == '.':
            return (i, j+2)
        if map[j-1][i] == '.':
            return (i, j-1)

def findPortals(map):
    portals = {}
    size = 120
    
    for j in range(size-1):
        for i in range(size-1):
            
            fwd = str(map[j][i]).strip()
            fwd = fwd + str(map[j][i+1]).strip()

            dwn = str(map[j][i]).strip()
            dwn = dwn + str(map[j+1][i]).strip()

            skip = True

            # scenario letters are in horizontal
            if str.isalpha(fwd) and len(fwd) == 2:
                pos = findPortalPosition(map, i, j, True)
                key = fwd
                skip = False
            elif str.isalpha(dwn) and len(dwn) == 2:
                pos = findPortalPosition(map, i, j, False)
                key = dwn
                skip = False
            
            if not skip:
                #print("fwd: "+ str(fwd) + ", dwn: " +str(dwn))
                coords = portals.get(key)
                if coords == None:                    
                    portals[key] = [pos]
                else:
                    coords.append(pos)
                    portals[key] = coords

    return portals

def outerPortal(portal, map):
    leftX = 2
    rightX = None
    topY = 2
    bottomY = None    
    
    line = map[2]
    for i in range(2, len(line)):
        if map[2][i] != "#" and map[2][i] != ".":
            rightX = i - 1
            break
    
    y = 2
    while map[y][2] != " ":
        y += 1
    bottomY = y-1
    
    return portal[0] == leftX or portal[0] == rightX or portal[1] == topY or portal[1] == bottomY


def joinPortals(graphs, portals):
    
    maze = {}
    for level in range(len(graphs)-1):
        graph = graphs[level]
        graphN = graphs[level+1]

        for p in portals:
            points = portals.get(p)
            if len(points) == 2:   
                x1,y1 = points[0] 
                x2,y2 = points[1] 
                
                # x1, y1 inner portal
                if not outerPortal(points[0], map):
  
                    # inner level -> outer level + 1
                    entry = graph.get( (x1, y1, level) )
                    entry.append( (x2 ,y2, level + 1 ))

                    exit = graphN.get( (x2 , y2, level + 1 ) )
                    exit.append( (x1, y1, level)  )

                    graph[(x1 ,y1, level )] = entry
                    graphN[(x2, y2, level + 1) ] = exit

                else: # x2, y2 inner portal
                      
                    entry = graph.get( (x2 ,y2, level) )                    
                    entry.append( (x1, y1, level+1 ))

                    exit = graphN.get( (x1, y1, level+1 ) )
                    exit.append( (x2 ,y2, level ) )                         
        
                    graph[(x2 ,y2, level )] = entry
                    graphN[(x1, y1, level+1 )] = exit
            #end if

        maze[(x1, y1, level)] = graph[(x1, y1, level)]
        maze[(x2, y2, level + 1)] = graphN[(x2, y2, level + 1)]
    #end for
    for g in graphs:
        for key in g:
            maze[key] = g.get(key)

    return maze


# failed idea :( over-engineering again
def doMagic(graph, zeroGraph, AA, ZZ, portals, position, level):

    result = []
    paths = {}
    for i in range(1000):

        # find reachable points from position
        if level == 0:
            explored = bfs(zeroGraph, position)
        else:
            explored = bfs(graph, position)
            
        # check all reachable portals from position
        for portal in explored:           
            isPortal = any(portal in val for val in portals.values())
            
            if isPortal and position != portal:                
                # if we're at level 0, check if we have a path to ZZ
                if level == 0:
                    path = find_shortest_path(zeroGraph, position, ZZ)
                    if path != None:
                        l = paths.get(position)
                        paths[position] = []
                        #paths[portal] = l + path
                        print("RES: "+ str(len(l+path)))
                        result.append(l + path)
                        break
                        #return len(l+path)

                print("start: " + str(position) + ", end: " + str(portal))
                print("LEVEL: " + str(level))
                path = find_shortest_path(graph, position, portal)
                
                #update path
                if path != None:
                    l = paths.get(position)
                    paths[position] = []
                    if l == None:
                        paths[portal] = path
                    else:
                        paths[portal] = l + path
                
                    
                if innerPortal(portal, map):                
                    level += 1

                else:                    
                    level -= 1

                position = portal              
            #end isPortal
        #end for    
    return paths
 

import sys
sys.setrecursionlimit(10000)

@timer
def part2(map, debug = False):
    level = 0
    portals = findPortals(map)
    AA = portals.get("AA")[0]
    ZZ = portals.get("ZZ")[0]
    
    graphs=[]
    for i in range(50):
        # inner levels graph 
        graph = buildGraph(map, portals, i, ZZ)  
        graphs.append(graph) 

    mazeGraph = joinPortals(graphs, portals)  
    start = (AA[0], AA[1], 0)
    end = (ZZ[0], ZZ[1], 0)
    
    path = find_shortest_path2(mazeGraph, start, end)
    if path != None:
        path = [j for i in path for j in i]
        print(path)
        print(len(path)-1)
    else:
        print("No path found!")
    
   
    
    if debug:
        printMap(map)

        for portal in portals:
            n = portals.get(portal)
            if len(n) == 2:
                print(str(portal) + " => " + str(portals.get(portal)))
                print("outer: "+ str(outerPortal(n[0], map)))
                print("outer: " +str(outerPortal(n[1], map)))
        
        printGraph(zeroGraph)   
        #printGraph(graph)   
    
    
    

filepath = 'input.txt' 
with open(filepath) as fp: 	
    line = fp.readline()
    map = [ [ ' ' for i in range(120) ] for j in range(120) ] 

    j = 0
    while line:
        size = len(line) - 1
        for i in range(size):
            map[j][i] = line[i]
        j += 1
        line = fp.readline()
    #end while
    part2(map)
