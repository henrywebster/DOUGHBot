"""underlying pizza-generation module of DOUGH system"""

import random
from collections import namedtuple
from functools import reduce

_MAX_PREMIUM = 3
_MAX_FREE = 4

# TODO
# * add args list to ctor

# Might have gone overboard with these
Category = namedtuple("Category", "modifiers, toppings")
PairList = namedtuple("PairList", "toppingpairs")
Pizza = namedtuple("Pizza", "premium, free")

# This functional / list comprehension hybrid is beautiful however
#   [("extra", "tofu"), ("", "ham")] => "extra tofu, ham"
setattr(PairList, "__str__", lambda pair: reduce("{}, {}".format, ["{} {}".format(
    modifier, topping) if modifier else topping for modifier, topping in pair.toppingpairs]))


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
                 responses,
                 maxpremium=_MAX_PREMIUM,
                 maxfree=_MAX_FREE):

        self.premiumpair = Category(premium, premiummod)
        self.freepair = Category(free, freemod)
        self.responses = responses

        self.maxpremium = maxpremium
        self.maxfree = maxfree

    def generate_pizza(self,
                       seed=None):
        """
        Create a pizza tuple based on input ingredients and RNG seed.
        """
        random.seed(seed)

        pizza = Pizza(self._generate_pair_list(
            self.premiumpair, random.randint(
                1, _MAX_PREMIUM)), self._generate_pair_list(
                    self.freepair, random.randint(1, _MAX_FREE)))

        return pizza

    def generate_response(self,
                          pizza,
                          name,
                          seed=None):
        """Create a random string response"""

        # TODO
        # * fill out docstring
        # * figure out coupling & dangerous default warning

        random.seed(seed)

        return random.choice(self.responses).format(name, pizza.premium, pizza.free)

    def _generate_pair_list(self,
                            category,
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
        return PairList([("", x) if random.randint(
            0, 2) else (random.choice(
                category.toppings), x) for x in set(random.choice(
                    category.modifiers) for _ in range(size))])
