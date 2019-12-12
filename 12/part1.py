import math

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

    energy = moonMotions(moons, velocity, 1000)
    #print(moons)
    #print(energy)
    print(sum(energy))

    