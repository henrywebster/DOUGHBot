"""Turns a pizza tupple into an image"""

import json
import os
from collections import namedtuple
from PIL import Image

MarketEntry = namedtuple("MarketEntry", "toppings, crust, name, size")

# TODO
# * Add pizza background image instead of drawing natively.
# * Load multiple recipes and vary size according to data. Define scale in JSON?
# * Handle user error on entering directory names

class Oven:

    def __init__(self, recipedir):
        self.recipedir = recipedir
        self.recipebook = self.stock_kitchen(self.recipedir)
        self.imgsize = (512, 512)

    def bake(self, pizza, recipe):

        pizzaimg = recipe.crust

        for pair in pizza:
            for _, topping in pair:
                pizzaimg = Image.alpha_composite(pizzaimg, recipe.toppings[topping])

        return pizzaimg.resize(self.imgsize, Image.NEAREST)

    def stock_kitchen(self, recipedir):
        """
        Fill up the internal dictionary with all the images from the image 'recipes'.
        """

        recipebook = {}
        for subdir, currdir, _ in os.walk(recipedir):
            for recipedir in currdir:
                with open(os.path.join(subdir, recipedir, "recipe.json")) as _f:
                    recipe = json.load(_f)

                # this is a bit of a hack: mutate the dictionary before it goes into the immutable tuple
                recipe["crust"] = Image.open(os.path.join(subdir, recipedir, recipe["crust"]))
                marketentry = MarketEntry._make(recipe.values())


                # replace filenames with image objects
                for topping, imagefile in marketentry.toppings.items():
                    marketentry.toppings[topping] = Image.open(
                        os.path.join(
                            subdir, recipedir, imagefile)) if imagefile else Image.new(
                                "RGBA", (marketentry.size, marketentry.size))

                recipebook[marketentry.name] = marketentry

        return recipebook
