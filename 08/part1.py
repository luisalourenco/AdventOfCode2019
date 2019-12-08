import sys

filepath = 'input.txt' 

images = 100
wide = 150
tall = 6
layers = {} 

with open(filepath) as fp: 	
    layer = fp.read(1)
    num = 1
    currW = 1
    t = 1
    while layer:
        #print(layer)        
        
        l = layers.get(num)
        if l == None:
            layers[num] = []
        #print(num)
        layers.get(num).append(layer)

        
        if currW == wide:
            
            currW = 1
            num += 1
        else:
            currW += 1
        
        layer = fp.read(1)

    #end while
    minZeros = sys.maxsize
    count = 0
    for k in layers:
        c = layers.get(k)
        count += 1
        zeros = c.count('0')
        if zeros <= minZeros:
            minZeros = zeros           
            ones = c.count('1')
            twos = c.count('2')
            res = ones * twos
            print(str(zeros) + ": " + str(res))
