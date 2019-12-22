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


def shuffeStrategy(deck, step, debug = True):
    # cut
    op = step[0]
    n = step[1]
    if op == 'CUT':
        n = int(n)
        deck = cut(deck, n)
    elif op == 'INC':
        n = int(n)
        deck = increment(deck, n)
    elif op == 'NEW':
        deck = dealNewStack(deck)
    return deck

def parseInput(line, steps):
    # cut
    if len(line) == 2:
            n = int(line[1])
            steps.append( ('CUT', n) )
    elif len(line) == 4:
        # increment
        if str.isnumeric(line[3]):
            n = int(line[3])
            steps.append( ('INC', n) )
        else: # new stack
            steps.append( ('NEW', None) )
    return steps


@timer
def part1(steps):
    deck = [ i for i in range(10007) ]
    repeat = 101741582076661

    for i in range(repeat):
        for step in steps:
            deck = shuffeStrategy(deck, step, False)

    for i in range(10007):
        #print("finding solution..." + str(i))
        if deck[i] == 2019:
            print(i)


@timer
def part2(fp):
    deck = [ i for i in range(119315717514047) ]
    repeat = 101741582076661

    for i in range(repeat):
        for step in steps:
            deck = shuffeStrategy(deck, step, False)

    print(deck[2020])




filepath = 'input.txt' 
with open(filepath) as fp: 	
    steps = []
    line = fp.readline().strip().split(' ')
    while line != ['']:        
        steps = parseInput(line, steps)
        line = fp.readline().strip().split(' ')
    #end while
    
    part1(steps)
    
    
