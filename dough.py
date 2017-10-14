"""underlying pizza-generation module of DOUGH system"""

import random
from collections import namedtuple
from functools import reduce

_MAX_PREMIUM = 3
_MAX_FREE = 4

# Might have gone overboard with these
Category = namedtuple("Category", "modifiers, toppings")
ToppingPair = namedtuple("ToppingPair", "modifier, topping")
Pizza = namedtuple("Pizza", "premium, free")

# TODO
# * use list comprehensions instead of functional to be COOL and PYTHONIC
# * implement Generator


def _file_to_list(filename):
    """turn a file with one item to a line into a python list"""

    return [line.rstrip() for line in open(filename) if not None]


class Dough():
    """
    D.O.U.G.H. stands for Digitally Optimized Utility for inGredient Hacking.
    It will generate random pizzas based on an initial set of ingredients.
    """

    def __init__(self, 
                 premium, 
                 premiummod, 
                 free, 
                 freemod, 
                 responses):

        self.premiumpair = Category(premium, premiummod)
        self.freepair = Category(free, freemod)
        self.responses = responses

    def generate_pizza(self, 
                       seed=None):
        """
        Create a pizza tuple based on input ingredients and RNG seed.
        """
        random.seed(seed)

        pizza = Pizza((_generate_pair_list(
            self.premiumpair, random.randint(
                1, _MAX_PREMIUM)), _generate_pair_list(
                    self.freepair, random.randint(1, _MAX_FREE))))

        yield pizza

    def generate_response(self,
                          pizza,
                          name,
                          seed=None):
        """Create a random string response"""

        # TODO
        # * fill out docstring
        # * figure out coupling & dangerous default warning
        random.seed(seed)

        return random.choice(self.responses).format(name,
                                                    _list_to_sentence(pizza.premium),
                                                    _list_to_sentence(pizza.free))


# TODO
# * clean this up
PREMIUM_LIST = _file_to_list("premium.txt")
PREMIUM_MOD_LIST = _file_to_list("premiummod.txt")
FREE_LIST = _file_to_list("free.txt")
FREE_MOD_LIST = _file_to_list("freemod.txt")
RESPONSE_LIST = _file_to_list("responses.txt")


def _generate_pair_list(category, 
                        size):
    """
    Return a list of tuples length of the size param. The tuples represent
    (MODIFIER, TOPPING) pairs. There can be no duplicate topping component
    in the tuple list, but there can be duplicate modifiers. The modifier
    component is optional.
    """

    # The set() cast here might be the cause of the non-deterministic ordering
    # for indgredients but this is low-priority.
    # Is this easier to understand than functional? I'm not so sure.
    return [ToppingPair("", x) if random.randint(
        0, 2) else ToppingPair(random.choice(
            category.toppings), x) for x in set(random.choice(
                category.modifiers) for _ in range(size))]


def _list_to_sentence(tuplelist):
    """
    Return the (MODIFIER, INGREDIENT) tuple list folded into a
    comma-deliniated string.

    [("extra", "tofu"), ("", "ham")] => "extra tofu, ham"

    lst: (MODIFER, INGREDIENT) tuple list

    returns: string in documented format
    """

    # This functional / list comprehension hybrid is beautiful however
    return reduce("{}, {}".format, ["{} {}".format(
        modifier, ingredient) if modifier else ingredient for modifier, ingredient in tuplelist])
