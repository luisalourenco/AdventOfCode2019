filepath = 'input.txt' 

def computeFuel(mass):
    return int(mass)/3 - 2

sum = 0
count = 0
with open(filepath) as fp: 	
    mass = fp.readline().strip()
    while mass:
        fuel = computeFuel(mass)
        while (fuel > 0):
            sum += fuel
            mass = fuel
            fuel = computeFuel(mass)
        #end while
        mass = fp.readline().strip()
    #end while

print sum
#print (computeFuel(12))
#print (computeFuel(14))
#print (computeFuel(1969))
#print (computeFuel(100756))