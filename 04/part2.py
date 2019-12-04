input = '136760-595730' 

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


count = 0
for p in range(lowerBound, upperBound):
    password = str(p)
    if checkPasswordCriteria(password):
        count += 1

print count
