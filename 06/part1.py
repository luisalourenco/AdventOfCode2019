filepath = 'input.txt'

dict = {} 

def aux(l, dict):
    if len(l) == 1:
        return 1

    res = len(l)
    for e in l:
        res += aux(e, dict)
    return res

with open(filepath) as fp: 	
    input = fp.readline().strip().split(')')
   
    while input:
        if len(input) != 2:
            break
        a = input[0]
        b = input[1]

        elem = dict.get(a)

        if elem == None:
            dict[a] = []
        dict.get(a).append(b)

        input = fp.readline().strip().split(')')
    #end while
    
    #print(dict)
    checkSum = 1

    sum = 0
    for e in dict:
        sum += aux(e, dict)
        #print(e)
        #print(sum)
        checkSum += sum
    
    #print(checkSum)
    

    
