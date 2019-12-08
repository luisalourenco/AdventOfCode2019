import sys

filepath = 'input.txt' 

images = 100
wide = 150
tall = 6
layers = {} 
image = {} 
image2 = {} 
auxImg = {} 

with open(filepath) as fp: 	
    layer = fp.read(1)
    num = 0
    currW = 1
    t = 1
    while layer:     
        
        l = layers.get(num)
        if l == None:
            layers[num] = []
       
        layers.get(num).append(layer)

        
        if currW == wide:
            
            currW = 1
            num += 1
        else:
            currW += 1
        
        layer = fp.read(1)

    #end while
    
    for i in range(6):
        if image2.get(i) == None:
            image2[i] = ['2'] * 25
    
    for r in range(100):
        layer = layers.get(r)

        if len(layer) == 1:
            break
        print("layer: "+ str(r))
        p = 0
        for i in range(6):
            b =  p
            p = b + 25
            
            auxImg[i] = layer[b:p]            
            
            #print(auxImg)
            
            print("init: " + str(b) + ",end: "+ str(p) )
            pixelLine = image2.get(i)
            for j in range(25):
                if pixelLine[j] == '2':
                   pixelLine[j] = layer[b:p][j]
    
    

print (image2)
for r in range(6):
    layer = "".join(image2.get(r))
    
    print(layer.replace("0", ".").replace("1", "#"))




