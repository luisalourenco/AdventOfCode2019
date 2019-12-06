filepath = 'input.txt'

graph = {} 

def aux(elem, graph):
    count = 0
    while True:
        if elem == None:
            break
        count += 1
        elem = graph.get(elem[0])
    return count

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
    checkSum = 0

    sum = 0
    for node in graph:
        sum = aux(graph.get(node), graph)

        #print(node +" - "+ str(aux(graph.get(node), graph)))
        #print(sum)
        checkSum += sum
    
    print(checkSum)
    

    
