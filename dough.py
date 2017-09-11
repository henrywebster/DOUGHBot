import random
import math

MAX_PREMIUM = 3
MAX_FREE = 4

def fileToList (filename):
    """
    turn a file with one item to a line into a python list
    """
    return list (filter (None, (line.rstrip() for line in open(filename))))


def generatePizza (premiumPair, freePair, frequency, seed):
    """
    premiumPair: tuple that represents a list of premium
    ingredients and a list of their possible modifiers

    freePair: tuple that is a list of free ingredients
    and a list of their possible modifiers
    
    frequency: the chance an ingredient will get a modifier

    seed: used for initializing random values
    """

    random.seed()

    # TODO: study the statistics of throwing out repeated vs 1 / 3
    # add verify stats & script for alphabetizing txt files

    freeNum = random.randint (1, MAX_FREE)

    pizza = ([],[])

    for _ in range (0, random.randint (1, MAX_PREMIUM)):
        ingredient = random.choice (premiumPair[0])
        if (('', ingredient) not in pizza[0]):
            pizza[0].append (('',ingredient))       

    for i, ingredient in enumerate(pizza[0]):
        if (random.randint(0, math.floor(1 / frequency))):
            pizza[0][i] = (random.choice(premiumPair[1]), ingredient[1])
            
    return pizza


def main ():
    
    premiumList = fileToList ('premium.txt')
    premiumModList = fileToList ('premiummod.txt')
    freeList = fileToList ('free.txt')
    freeModList = fileToList ('freemod.txt')

    pizza = generatePizza ((premiumList,premiumModList), (freeList,freeModList), 0.5, 101212)
    print (pizza)
    
main()

    

    
