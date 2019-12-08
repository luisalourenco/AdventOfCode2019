import multiprocessing as mp
import functools

lowerBound = 136760
upperBound = 595730


# It is a six-digit number.
# The value is within the range given in your puzzle input.
# Two adjacent digits are the same (like 22 in 122345).
# Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
  
def checkPasswordCriteria(password):
    if len(password) != 6:
        return False

    lastDigit = int(password[0])
    dict = {} 
    crescent = True
    adjacent = False
    listAdjacent = []
    for i in range(0, 6):
        c = password[i]

        if dict.get(c) == None:
            dict[c] = []
        
        if (i-1) in dict.get(c):
            adjacent = True
            listAdjacent.append(c)     
            
        dict.get(c).append(i)

        if int(c) < lastDigit:
            crescent = False
        lastDigit = int(c)

    for c in listAdjacent:
        if password.count(c) == 2:
            return crescent and adjacent
    return False


def getBounds(lowerBound, upperBound, chunkSize, residual):
    bound1 = (lowerBound, lowerBound + chunkSize)
    bound2 = (bound1[1], bound1[1] + chunkSize)
    bound3 = (bound2[1], bound2[1] + chunkSize)
    bound4 = (bound3[1], bound3[1] + chunkSize)
    bound5 = (bound4[1], bound4[1] + chunkSize)
    bound6 = (bound5[1], bound5[1] + chunkSize)
    bound7 = (bound6[1], bound6[1] + chunkSize)
    bound8 = (bound7[1], upperBound)    
    return (bound1, bound2, bound3, bound4, bound5, bound6, bound7, bound8)

def secureContainer(bounds):
    count = 0
    for p in range(bounds[0], bounds[1]):
        password = str(p)
        if checkPasswordCriteria(password):
            count += 1
    return count


processors = mp.cpu_count()

# Step 1: Init multiprocessing.Pool()
pool = mp.Pool(processors)
chunkSize = (upperBound - lowerBound) / processors
residual = (upperBound - lowerBound) % processors


# Step 2: `pool.map` the `secureContainer`
count = pool.map(secureContainer, getBounds(lowerBound, upperBound, chunkSize, residual))

# Step 3: Don't forget to close
pool.close()    


print (sum(count))
