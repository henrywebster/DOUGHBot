"""underlying pizza-generation module of DOUGH system"""

import random
from functools import reduce

_MAX_PREMIUM = 3
_MAX_FREE = 4


def _file_to_list(filename):
    """turn a file with one item to a line into a python list"""

    return list(filter(None, (line.rstrip() for line in open(filename))))


# TODO: clean this up
PREMIUM_LIST = _file_to_list('premium.txt')
PREMIUM_MOD_LIST = _file_to_list('premiummod.txt')
FREE_LIST = _file_to_list('free.txt')
FREE_MOD_LIST = _file_to_list('freemod.txt')


def _generate_pair_list(option_pair, size):
    """
    Return a list of tuples length of the size param. The tuples represent
    (MODIFIER, TOPPING) pairs. There can be no duplicate topping component
    in the tuple list, but there can be duplicate modifiers. The modifier
    component is optional.
    """

    # The set() cast here might be the cause of the non-deterministic ordering
    # for indgredients but this is low-priority.
    return list(map(
        lambda x: ('', x) if random.randint(0, 2) else(
            random.choice(option_pair[1]), x), set(
            map(lambda _: random.choice(option_pair[0]), [None] * size))))


def list_to_sentence(lst):
    """
    Return the (MODIFIER, INGREDIENT) tuple list folded into a
    comma-deliniated string.

    [('extra', 'tofu'), ('', 'ham')] => 'extra tofu, ham'

    lst: (MODIFER, INGREDIENT) tuple list

    returns: string in documented format
    """

    return str(reduce(lambda x, y: "{}, {}".format(x, y), map(
        lambda x: "{} {}".format(x[0], x[1]) if x[0] else x[1], lst)))


def generate_pizza(seed=None,
                   premium_pair=(PREMIUM_LIST, PREMIUM_MOD_LIST),
                   free_pair=(FREE_LIST, FREE_MOD_LIST)):
    """
    Create a pizza tuple based on input ingredients and RNG seed.

    premium_pair: tuple of premium ingredients and their possible modifiers
    free_pair: tuple of free ingredients and their possible modifiers
    seed: used for initializing random values

    returns: pizza tuple
    """

    random.seed(seed)

    pizza = (_generate_pair_list(
        premium_pair, random.randint(1, _MAX_PREMIUM)), _generate_pair_list(
            free_pair, random.randint(1, _MAX_FREE)))

    return pizza
