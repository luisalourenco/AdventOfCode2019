import time

def timer(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    f = func(*args, **kwargs)
    print(f'The function ran for {time.time() - start} s')
    return f
  return wrapper


@timer
def FFT(inputList, phase):
    size = len(inputList)
    
    

    for i in range(phase):
        results = []
        inputList = inputList[::-1]
        # position of output   
        val = 0  
        for o in range(size):
            val += int(inputList[o])
            lenght = len( str(val) ) - 1 
            results.append( str(val)[lenght] ) 
        #end for 

        results = results[::-1]
        inputList = "".join(results)
    #end for

    return "".join(results)

def repeatInput(s, n):
    result = ""
    for i in range(n):
        result += s
    return result


test = str(12345678)
t2 = str(80871224585914546619083218645595)
t3 = str(19617804207202209144916044189917)

tt = '03081770884921959731165446850517'

filepath = 'input.txt' 
with open(filepath) as fp: 	
    line = fp.readline().strip()
    
    #result = FFT(t2, 100)
    offset = int(line[0:7])
    line *= 10000
    #line = repeatInput(line, 10000)
    result = FFT( line[offset:], 100)
    
    res = str(result[:8])

    print("".join(res))