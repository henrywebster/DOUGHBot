import random
import math
from fractions import Fraction
from functools import reduce

MAX_PREMIUM = 3
MAX_FREE = 4

MOD_CHANCE = 2

# Helper functions for generatePizza

def fileToList (filename):
    """
    turn a file with one item to a line into a python list
    """
    return list (filter (None, (line.rstrip() for line in open(filename))))

def randomPairSet (optionPair, size):
    """
    Return a list of tuples length of the size param. The tuples represent
    (MODIFIER, TOPPING) pairs. There can be no duplicate topping component 
    in the tuple list, but there can be duplicate modifiers. The modifier
    component is optional.
    """

    return list (map (
        lambda x: ('', x) if random.randint(0, MOD_CHANCE) else (
            random.choice(optionPair[1]), x), set (
            map (lambda _: random.choice(optionPair[0]), [None] * size))))

def listToSentance (lst):
    """
    Return the (MODIFIER, INGREDIENT) tuples folded into a 
    comma-deliniated string.
    """

    return str(reduce (lambda x, y: "{}, {}".format(x, y), map(
        lambda x: "{} {}".format(x[0], x[1]) if x[0] else x[1], lst)))
    
def generatePizza (premiumPair, freePair, seed):
    """
    premiumPair: tuple that represents a list of premium
    ingredients and a list of their possible modifiers

    freePair: tuple that is a list of free ingredients
    and a list of their possible modifiers
    
    seed: used for initializing random values
    """

    random.seed()

    pizza = (randomPairSet(
        premiumPair, random.randint(1, MAX_PREMIUM)), randomPairSet(
            freePair, random.randint(1, MAX_FREE)))
    
    return pizza


def main ():
    
    premiumList = fileToList ('premium.txt')
    premiumModList = fileToList ('premiummod.txt')
    freeList = fileToList ('free.txt')
    freeModList = fileToList ('freemod.txt')

    pizza = generatePizza ((premiumList,premiumModList), (freeList,freeModList), 101212)

    pizzaString = "One {} pizza with {}".format(
        listToSentance(pizza[0]), listToSentance(pizza[1]))
    
    print (pizzaString)

    
main()

    

    
