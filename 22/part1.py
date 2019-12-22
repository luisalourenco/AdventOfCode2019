import time

def timer(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    f = func(*args, **kwargs)
    print(f'The function ran for {time.time() - start} s')
    return f
  return wrapper


def dealNewStack(deck):
    #print("new stack")
    return deck[::-1]

def cut(deck, n):
    #print("cutting of " + str(n))
    bottom = deck[:n]
    top = deck[n:]
    return top + bottom

def increment(deck, n):
    #print("increment of " + str(n))
    size = len(deck)
    shuffle = [ i for i in range(size) ]

    pos = 0
    for i in range(size):
        card = deck[i]
        index = pos % size
        shuffle[index] = card
        pos += n
    return shuffle

@timer
def part1(fp):
    deck = [ i for i in range(10007) ]
    line = fp.readline().strip().split(' ')
  
    while line != ['']:        
        #print("processing: "+str(line))
        deck = shuffeStrategy(deck, line, False)
        line = fp.readline().strip().split(' ')
    #end while

    for i in range(10007):
        #print("finding solution..." + str(i))
        if deck[i] == 2019:
            print(i)

def shuffeStrategy(deck, line, debug = True):
    # cut
    if len(line) == 2:
            n = int(line[1])
            deck = cut(deck, n)
    elif len(line) == 4:
        # increment
        if str.isnumeric(line[3]):
            n = int(line[3])
            deck = increment(deck, n)
        else: # new stack
            deck = dealNewStack(deck)
    return deck



filepath = 'input.txt' 
with open(filepath) as fp: 	
    part1(fp)
    
