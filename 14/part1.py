#!/usr/bin/python
# -*- coding: utf-8 -*-
import math



def computeNeededOre(comp, qty, reactions, res):
    
    l = reactions.get(comp)
    if l == None:
        return res
    
    qtyReaction = l[0]

    mul = int(math.ceil(qty/qtyReaction))
    result = [ (a, b * mul) for (a,b) in l[1] ]    

    for c in result:
        res = computeNeededOre(c[0], c[1], reactions, res + result)
   
    return result
   
 
def processRecipe(ores, recipe):
    for o in ores:
        comp = o[0]
        qty = o[1]
        if recipe.get(comp) == None:
            recipe[comp] = 0
        recipe[comp] += qty
    return recipe


filepath = 't.txt' 
with open(filepath) as fp: 	
    line = fp.readline().strip().split('=>')

    reactions = {}
    while line != ['']:
        chemicals = line[0].strip().split(',')
        
        inputChemicals = []
        inputQunatities = []
        inputComponents = []
        for c in chemicals: 
            c = c.strip().split(' ')          
            inputQuantity = int(c[0])
            inputComponent = c[1]
            inputChemicals.append( (inputComponent, inputQuantity) )
            inputComponents.append(inputComponent)
        
        result = line[1].strip().split(' ')
        quantity = int(result[0])
        component = result[1]

        reactions[component] = (quantity, inputChemicals)             

        line = fp.readline().strip().split('=>')      
    #end while
    neededComponents = reactions.get('FUEL')[1]
    #print(neededComponents)

   
    root = 'FUEL'
    recipe = {}
    ores = []
    for c in neededComponents:
        ores = computeNeededOre(c[0], c[1], reactions, ores)
        recipe = processRecipe(ores, recipe)
  
    print("recipe: " +str(neededComponents))
    print(reactions)

    sum = 0
    for r in neededComponents:
        t = reactions.get(r[0])
        print(r)

        #if t == None:
        #    break

        #if (t == 'ORE'):
            #sum += t[0]
        #    print(sum)
        
        qtyReaction = t[0]
        qty = t[1].pop()[1]
        val = int(math.ceil(qty/qtyReaction)) # apply recipe val times
        
        sum +=  int(math.ceil( (r[1]/ qtyReaction)))* qty
        
        print("reaction needs "+ str(qty) + " ORE")
        print("to produce " + str(qtyReaction) + " "+ str(r))
        print(val)
        #sum += r
    print(sum)
    #print(sum([ b for (a,b) in result ]))

        