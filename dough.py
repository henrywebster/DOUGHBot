import random
import sys
from fractions import Fraction
from functools import reduce

VERSION_MAJOR = 0
VERSION_MINOR = 2

MAX_PREMIUM = 3
MAX_FREE = 4

"""
	(c) 2017 Henry Webster

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
	
# Helper functions for generatePizza

def fileToList (filename):
    """
    turn a file with one item to a line into a python list
    """
    return list (filter (None, (line.rstrip() for line in open(filename))))

def generatePairList (optionPair, size):
    """
    Return a list of tuples length of the size param. The tuples represent
    (MODIFIER, TOPPING) pairs. There can be no duplicate topping component 
    in the tuple list, but there can be duplicate modifiers. The modifier
    component is optional.
    """

	# The set() cast here might be the cause of the non-deterministic ordering
	# for indgredients but this is low-priority.
    return list (map (
        lambda x: ('', x) if random.randint(0, 2) else (
            random.choice(optionPair[1]), x), set (
            map (lambda _: random.choice(optionPair[0]), [None] * size))))

def listToSentance (lst):
    """
    Return the (MODIFIER, INGREDIENT) tuple list folded into a 
    comma-deliniated string.

    [('extra', 'tofu'), ('', 'ham')] => 'extra tofu, ham'
    """

    return str(reduce (lambda x, y: "{}, {}".format(x, y), map(
        lambda x: "{} {}".format(x[0], x[1]) if x[0] else x[1], lst)))
    
def generatePizzaWithPairs (premiumPair, freePair, seed):
    """
    premiumPair: tuple that represents a list of premium
    ingredients and a list of their possible modifiers

    freePair: tuple that is a list of free ingredients
    and a list of their possible modifiers
    
    seed: used for initializing random values
    """

    random.seed(seed)

    pizza = (generatePairList(
        premiumPair, random.randint(1, MAX_PREMIUM)), generatePairList(
            freePair, random.randint(1, MAX_FREE)))
    
    return pizza

def generatePizza (seed):
	return generatePizzaWithPairs((PREMIUM_LIST, PREMIUM_MOD_LIST), (FREE_LIST, FREE_MOD_LIST), seed)

PREMIUM_LIST = fileToList ('premium.txt')
PREMIUM_MOD_LIST = fileToList ('premiummod.txt')
FREE_LIST = fileToList ('free.txt')
FREE_MOD_LIST = fileToList ('freemod.txt')