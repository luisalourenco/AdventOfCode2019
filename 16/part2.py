
def convert(s): 
  
    # initialization of string to "" 
    new = "" 
  
    # traverse in the string  
    for x in s: 
        new += x  
  
    # return string  
    return new 

def FFT(inputList, phase):
    base = [0, 1, 0, -1]
    size = len(inputList)

    
    for i in range(phase):
        result = []
        # position of output       
        for o in range(size):
            #position of input to compute
            basePos = 0
            #print("output "+ str(o)+":")
            val = 0
            repeat = o
            for s in range(size):
                if repeat != 0:
                    repeat -= 1
                else:
                    basePos += 1
                    repeat = o

                val += int(inputList[s]) * base[basePos%4]
                #print(inputList[s] + " *  " + str(base[basePos%4]))
                
            #end for
            #print("value: "+ str(val))
            lenght = len(str(val)) -1 
            result.append(str(val)[lenght])
        #print(convert(result))
        inputList = convert(result)
    #end for

    return result


base = [0, 1, 0, -1]
test = str(12345678)
t2 = str(80871224585914546619083218645595)
t3 = str(19617804207202209144916044189917)

filepath = 'input.txt' 
with open(filepath) as fp: 	
    line = fp.readline().strip()
    #result = FFT(t2, 100)
    result = FFT(line, 100)
    
    #print(str(result))

    print(str(result[0:8]))