import time

def timer(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    f = func(*args, **kwargs)
    print(f'The function ran for {time.time() - start} s')
    return f
  return wrapper

def buildGraph(map, portals, ZZ = None):
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

            # if (x,y) is an outer portal, then close "doors"
            if (x,y) in portals.values() and not innerPortal((x,y), map):
                neighbours = []
            elif ZZ == (x,y):
                neighbours = []
            else:
                if map[y][x] == '.':
                    if map[east[1]][east[0]] == '.' and east != ZZ:
                        neighbours.append(east)
                    if map[west[1]][west[0]] == '.' and west != ZZ:
                        neighbours.append(west)
                    if map[north[1]][north[0]] == '.' and north != ZZ:
                        neighbours.append(north)
                    if map[south[1]][south[0]] == '.' and south != ZZ:
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

def joinPortals(graph, portals):
    for p in portals:
        points = portals.get(p)
        if len(points) == 2:
            entry = graph.get(points[0])
            entry.append(points[1])
            graph[points[0]] = entry
            
            exit = graph.get(points[1])
            exit.append(points[0])
            graph[points[1]] = exit
    return graph



def innerPortal(portal, map):
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


def doMagic(graph, zeroGraph, AA, ZZ, portals, position, level):


    paths = {}
    for i in range(400):

        # find reachable points from position
        if level == 0:
            explored = bfs(zeroGraph, position)
        else:
            explored = bfs(graph, position)
            
        # check all reachable portals from position
        for portal in explored:           
            isPortal = any(portal in val for val in portals.values())
            
            if isPortal:                
                # if we're at level 0, check if we have a path to ZZ
                if level == 0:
                    path = find_shortest_path(zeroGraph, position, ZZ)
                    if path != None:
                        l = paths.get(position)
                        paths[position] = []
                        paths[portal] = l + path
                        
                        return len(l+path)

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
        

@timer
def part2(map, debug = True):
    level = 0
    portals = findPortals(map)
    AA = portals.get("AA")[0]
    ZZ = portals.get("ZZ")[0]

    # zero level graph
    zeroGraph = buildGraph(map, portals)
    
    # inner levels graph 
    graph = buildGraph(map, portals, ZZ)
    graph = joinPortals(graph, portals)    
    
    paths = doMagic(graph, zeroGraph, AA, ZZ, portals, AA, level)
    #print(paths)
    
    if debug:
        printMap(map)

        for portal in portals:
            n = portals.get(portal)
            if len(n) == 2:
                print(str(portal) + " => " + str(portals.get(portal)))
                print(innerPortal(n[0], map))
                print(innerPortal(n[1], map))
        
        printGraph(zeroGraph)   
        #printGraph(graph)   
    
    #print(str(i) + " iterations.")
    #remove starting point
    
    #if path != None:
    #    path.pop(0)  
    #    print(len(path))
    #else:
    #    print("There is no path to ZZ!")

    


filepath = 't3.txt' 
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
