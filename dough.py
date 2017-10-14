"""underlying pizza-generation module of DOUGH system"""

import random
from collections import namedtuple
from functools import reduce

_MAX_PREMIUM = 3
_MAX_FREE = 4

Category = namedtuple("Category", "modifiers, toppings")
ToppingPair = namedtuple("ToppingPair", "modifier, topping")

# TODO
# * use list comprehensions instead of functional to be COOL and PYTHONIC


def _file_to_list(filename):
    """turn a file with one item to a line into a python list"""

    return [line.rstrip() for line in open(filename) if not None]


# TODO
# * clean this up
PREMIUM_LIST = _file_to_list("premium.txt")
PREMIUM_MOD_LIST = _file_to_list("premiummod.txt")
FREE_LIST = _file_to_list("free.txt")
FREE_MOD_LIST = _file_to_list("freemod.txt")
RESPONSE_LIST = _file_to_list("responses.txt")


def _generate_pair_list(category, size):
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


def generate_response(pizza, name, seed=None, responses=RESPONSE_LIST):
    """Create a random string response"""

    # TODO
    # * fill out docstring
    # * figure out coupling & dangerous default warning
    random.seed(seed)

    return random.choice(responses).format(name,
                                           _list_to_sentence(pizza[0]),
                                           _list_to_sentence(pizza[1]))


def generate_pizza(seed=None,
                   premium=PREMIUM_LIST,
                   premiummod=PREMIUM_MOD_LIST,
                   free=FREE_LIST,
                   freemod=FREE_MOD_LIST):
    """
    Create a pizza tuple based on input ingredients and RNG seed.

    premium_pair: tuple of premium ingredients and their possible modifiers
    free_pair: tuple of free ingredients and their possible modifiers
    seed: used for initializing random values

    returns: pizza tuple
    """

    random.seed(seed)

    pizza = (_generate_pair_list(
        Category(premium, premiummod), random.randint(
            1, _MAX_PREMIUM)), _generate_pair_list(
                Category(free, freemod), random.randint(1, _MAX_FREE)))

    return pizza
