import time

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
        steps+=1

        if node not in explored:            
            explored.append(node)
            neighbours = graph.get(node)

            # add neighbours of node to queue
            for neighbour in neighbours:
                queue.append(neighbour)
    
    return steps, explored


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

def printMap(map, fileMode = True):
    if fileMode:
        file1 = open("MyFileAll.txt","w") 
    
        for l in map:
            for j in range(len(l)):
                file1.write(l[j])
            file1.write("\n")
        file1.close() 

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
    size = 20
    for j in range(size-1):
        for i in range(size-1):

            fwd = str(map[j][i:i+1]).strip()
            dwn = str(map[j:j+1][i]).strip()
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
                coords = portals.get(key)
                if coords == None:                    
                    portals[key] = [pos]
                else:
                    coords.append(pos)
                    portals[key] = coords

    return portals

@timer
def part1(map):
    portals = findPortals(map)
    print(portals)

    return 0


filepath = 't.txt' 
with open(filepath) as fp: 	
    line = fp.readline()
    size = len(line)
    map = [ [ ' ' for i in range(20) ] for j in range(20) ] 

    j = 0
    while line:
        map[j]= line[:len(line)-1]
        j += 1
        line = fp.readline()
    #end while
    #print(map)
    printMap(map)
    part1(map)
