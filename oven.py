"""Turns a pizza tupple into an image"""

import json
import os
from collections import namedtuple
from PIL import Image

# TODO
# * Add pizza background image instead of drawing natively.
# * Load multiple recipes and vary size according to data. Define scale in JSON?
# * Handle user error on entering directory names
# * Have only one oven per recipe type?

RecipeBook = namedtuple("RecipeBook", "toppings, crust, name, size")


class Oven:
    """
    The Oven class takes a recipe dir, which has subdirs of the pictures it needs to load and a definition
    formatted in json called 'recipe.json'.

    The Oven returns an image of a pizza based on what that pizza is composed of.
    """

    def __init__(self, rootdir):
        self.rootdir = rootdir
        self.recipebook = self.stock_kitchen(self.rootdir)
        self.imgsize = (512, 512)

    def bake(self, pizza):
        """
        Composite images from the recipe according to what is in the pizza.
        """
        pizzaimg = self.recipebook.crust

        for pair in pizza:
            for _, topping in pair:
                pizzaimg = Image.alpha_composite(
                    pizzaimg, self.recipebook.toppings[topping])

        return pizzaimg.resize(self.imgsize, Image.NEAREST)

    def stock_kitchen(self, rootdir):
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
