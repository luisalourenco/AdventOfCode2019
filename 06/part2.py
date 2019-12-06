filepath = 'input.txt'

graph = {} 


def buildList(elem, graph):
    list = []
    while True:
        if elem == None:
            break
        list.append(elem)
        elem = graph.get(elem[0])
    return list

def countHops(youList, santaList):
    hops = 0
    for node in youList:
        #print(node)
        if node in santaList:
            return (hops, node)
        else:
            hops += 1
    return (hops, node)


with open(filepath) as fp: 	
    input = fp.readline().strip().split(')')
   
    while input:
        if len(input) != 2:
            break
        a = input[0]
        b = input[1]

        elem = graph.get(b)

        if elem == None:
            graph[b] = []

        graph.get(b).append(a)

        input = fp.readline().strip().split(')')
    #end while
    
    #print(graph)
    
    youList = buildList(graph.get("YOU"), graph)
    santaList = buildList(graph.get("SAN"), graph)

    #print(santaList)
    (count, elem) = countHops(youList, santaList)
    
    for n in santaList:
        if n[0] == elem[0]:
            print (count)
            break
        else:
            count += 1


    
    

    
