import random
import math
from fractions import Fraction

MAX_PREMIUM = 3
MAX_FREE = 4

MOD_CHANCE = 2

def fileToList (filename):
    """
    turn a file with one item to a line into a python list
    """
    return list (filter (None, (line.rstrip() for line in open(filename))))

def randomPairSet (optionPair, size):
    return list (map (
        lambda x: ('', x) if random.randint(0, 2) else (random.choice(optionPair[1]), x), set (
            map (lambda _: random.choice(optionPair[0]), [None] * size))))

def generatePizza (premiumPair, freePair, seed):
    """
    premiumPair: tuple that represents a list of premium
    ingredients and a list of their possible modifiers

    freePair: tuple that is a list of free ingredients
    and a list of their possible modifiers
    
    seed: used for initializing random values
    """

    random.seed()

    # TODO: study the statistics of throwing out repeated vs 1 / 3
    # add verify stats & script for alphabetizing txt files

#    [None] * random.randint(1, MAX_PREMIUM)
    
    # premium
    """
    for _ in range (0, random.randint (1, MAX_PREMIUM)):
        ingredient = random.choice (premiumPair[0])
        if (('', ingredient) not in pizza[0]):
            pizza[0].append (('',ingredient))       
    """

    
    pizza = (randomPairSet(
        premiumPair, random.randint(1, MAX_PREMIUM)), randomPairSet(
            freePair, random.randint(1, MAX_FREE)))

    
    """
    # free
    for _ in range (0, random.randint (1, MAX_FREE)):
        ingredient = random.choice (freePair[0])
        if (('', ingredient) not in pizza[1]):
            pizza[1].append (('', ingredient))

    for i, ingredient in enumerate(pizza[1]):
        if (not random.randint(0, 2)):
            pizza[1][i] = (random.choice(freePair[1]), ingredient[1])
       """     
    return pizza


def main ():
    
    premiumList = fileToList ('premium.txt')
    premiumModList = fileToList ('premiummod.txt')
    freeList = fileToList ('free.txt')
    freeModList = fileToList ('freemod.txt')

    pizza = generatePizza ((premiumList,premiumModList), (freeList,freeModList), 101212)

    # use a FOLD
    print (pizza)
    """
    pizzaString = ""
    if 2 == len(pizza[0][0]):
        pizzaString = " and ".join(pizza[0][0])

    elif len(pizza[0][0]) > 2:
        pizzaString = ", ".join(pizza[0][0])
        lIndex = pizzaString.rfind(',') + 1
        pizzaString = pizzaString[:lIndex] + " and" + pizzaString[lIndex:]

    else:
        pizzaString = pizza[0]
    """
main()

    

    
