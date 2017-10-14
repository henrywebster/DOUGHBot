"""Turns a pizza tupple into an image"""

import json
import os
from collections import namedtuple
from PIL import Image

# TODO
# * Handle user error on entering directory names
# * Have only one oven per recipe type?
# * Image seems blurry on twitter
# * Fix background color

RecipeBook = namedtuple("RecipeBook", "toppings, crust, name, size")


class Oven:
    """
    The Oven class takes a recipe dir, which has subdirs of the pictures it needs to load and a definition
    formatted in json called 'recipe.json'.

    The Oven returns an image of a pizza based on what that pizza is composed of.
    """

    def __init__(self, rootdir):
        self.rootdir = rootdir
        self.recipebook = self._stock_kitchen(self.rootdir)

        # 512px is Twitter recommended, but I thought it looked weird with these
        self.imgsize = (320, 320)

    def bake(self, pizza):
        """
        Composite images from the recipe according to what is in the pizza.
        """
        pizzaimg = self.recipebook.crust

        # the syntax with named tuples got out of hand
        for pair in pizza:
            for _, topping in pair.toppingpairs:
                pizzaimg = Image.alpha_composite(
                    pizzaimg, self.recipebook.toppings[topping])

        return pizzaimg.resize(self.imgsize, Image.NEAREST)

    def _stock_kitchen(self, rootdir):
        """
        Fill up the internal dictionary with all the images from the image 'recipes'.
        """

        with open(os.path.join(rootdir, "recipe.json")) as _f:
            recipe = json.load(_f)

            # this is a bit of a hack: mutate the dictionary before it goes into the immutable tuple
            recipe["crust"] = Image.open(
                os.path.join(rootdir, recipe["crust"]))
            recipebook = RecipeBook._make(recipe.values())

            # replace filenames with image objects
            for topping, imagefile in recipebook.toppings.items():
                recipebook.toppings[topping] = Image.open(
                    os.path.join(
                        rootdir, imagefile)) if imagefile else Image.new(
                            "RGBA", (recipebook.size, recipebook.size))

        return recipebook
