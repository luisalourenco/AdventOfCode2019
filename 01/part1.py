filepath = 'input.txt' 

def computeFuel(mass):
    return int(mass)/3 - 2

sum = 0
count = 0
with open(filepath) as fp: 	
    mass = fp.readline().strip()
    while mass:
        sum += computeFuel(mass)
        count += 1
        mass = fp.readline().strip()
    #end while
print (sum)
print (count)