import math
from math import gcd

def LCM(arr, n): 
      
    # Find the maximum value in arr[] 
    max_num = 0; 
    for i in range(n): 
        if (max_num < arr[i]): 
            max_num = arr[i]; 
  
    # Initialize result 
    res = 1; 
  
    # Find all factors that are present  
    # in two or more array elements. 
    x = 2; # Current factor. 
    while (x <= max_num): 
          
        # To store indexes of all array 
        # elements that are divisible by x. 
        indexes = []; 
        for j in range(n): 
            if (arr[j] % x == 0): 
                indexes.append(j); 
  
        # If there are 2 or more array  
        # elements that are divisible by x. 
        if (len(indexes) >= 2): 
              
            # Reduce all array elements  
            # divisible by x. 
            for j in range(len(indexes)): 
                arr[indexes[j]] = int(arr[indexes[j]] / x); 
  
            res = res * x; 
        else: 
            x += 1; 
  
    # Then multiply all reduced  
    # array elements 
    for i in range(n): 
        res = res * arr[i]; 
  
    return res; 
def lcm(arr):
    lcm = arr[0]
    for i in arr[1:]:
        lcm = lcm*i/gcd(lcm, i)
    return lcm

def applyGravity(moons, velocity):
    
    for i in range(len(moons)):
        # (moon_a, moon_b)
        delta_x = 0
        delta_y = 0
        delta_z = 0
        #print(moons)
        for j in range(len(moons)):
            if moons[i][0] < moons[j][0]:
                delta_x += 1
            if moons[i][1] < moons[j][1]:
                delta_y += 1
            if moons[i][2] < moons[j][2]:
                delta_z += 1
            
            if moons[i][0] > moons[j][0]:
                delta_x -= 1
            if moons[i][1] > moons[j][1]:
                delta_y -= 1
            if moons[i][2] > moons[j][2]:
                delta_z -= 1

        #end for 
        
        velocity[i] =  (velocity[i][0] + delta_x, velocity[i][1] + delta_y, velocity[i][2] + delta_z)
    #print(velocity)  

    return velocity


def applyVelocity(moons, velocity):
    for i in range(len(moons)):
        moons[i] = (moons[i][0] + velocity[i][0], moons[i][1] + velocity[i][1],  moons[i][2] + velocity[i][2])
    return moons

def computeEnergy(moons, velocity):
    energy = []
    for i in range(len(moons)):
        #print(moons[i])
        #print(velocity[i])

        pot = abs(moons[i][0]) + abs(moons[i][1]) + abs(moons[i][2])
        kin = abs(velocity[i][0]) + abs(velocity[i][1]) + abs(velocity[i][2])
        #print(pot)
        #print(kin)

        energy.append(pot * kin)
    return energy


def moonMotions(moons, velocity, steps):
    for i in range(steps):
        applyGravity(moons, velocity)
        applyVelocity(moons, velocity)
    
    return computeEnergy(moons, velocity)

def getMoonKey(moons, i):
    moonsCoords = ''    
    for moon in moons:
        moonsCoords = str(moon[i]) + "-" + moonsCoords
    return moonsCoords

def getVelKey(velocity, i):
    moonsVel = ''
    for vel in velocity:
        moonsVel = str(vel[i]) + "-" + moonsVel
    return moonsVel

def moonMotionsWithState(moons, velocity, states):
   
    arr = []
    for c in range(3):
        steps = 0  
        states = {}
        while True:
        #print(states.get((getMoonKey(moons), getVelKey(velocity))) )
            key = getMoonKey(moons, c) + getVelKey(velocity, c)
            print(key)
            if states.get( key ) == None:
                states[key] = steps
            else:
                arr.append(steps)
                break

            applyGravity(moons, velocity)
            applyVelocity(moons, velocity)
        
        
            steps +=1
    return arr



states = {}
moons = []
velocity = [(0,0,0)]*4
filepath = 'input.txt' 
with open(filepath) as fp: 	
    line = fp.readline().strip().split(',')
   
    while line != ['']:

        x = int(line[0].split('=')[1])
        y = int(line[1].split('=')[1])
        z = line[2].split('=')[1]
        z = int(z[0:len(z)-1])

        moons.append((x,y,z))
        #print( (x,y,z) )

        line = fp.readline().strip().split(',')       
    #end while

    steps = moonMotionsWithState(moons, velocity, states)
    print(steps)
    print(LCM(steps, 3))
    #print(lcm(steps))
    #print(moons)
    #print(energy)
    #print(sum(energy))

    