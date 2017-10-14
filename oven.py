"""Turns a pizza tupple into an image"""

import json
import os
from collections import namedtuple
from PIL import Image, ImageDraw

MarketEntry = namedtuple("MarketEntry", "toppings, name, size")

MARKET_DIR = "recipes/"
_MARKET_DICT = {}

_BLANK_IMG = Image.new("RGBA", (64, 64))

# TODO
# * Add pizza background image instead of drawing natively.
# * Load multiple recipes and vary size according to data. Define scale in JSON?

def stock_kitchen():
    """
    Fill up the internal dictionary with all the images from the image 'recipes'.
    """

    recipebook = {}
    for subdir, currdir, _ in os.walk(MARKET_DIR):
        for recipedir in currdir:
            with open(os.path.join(subdir, recipedir, "recipe.json")) as _f:
                recipe = json.load(_f)

            marketentry = MarketEntry._make(recipe.values())

            # replace filenames with image objects
            for topping, imagefile in marketentry.toppings.items():
                marketentry.toppings[topping] = Image.open(
                    os.path.join(
                        subdir, recipedir, imagefile)) if imagefile else _BLANK_IMG

            recipebook[marketentry.name] = marketentry

    return recipebook


def bake_pizza(pizza, marketname="basic"):
    """
        Create an image of the input pizza

        TODO: VARIABLE NAMES / ORGANIZATION OF THIS IS TERRIBLE

        REFACTOR REFACTOR REFACTOR
    """

    market = _MARKET_DICT[marketname]
    size = (market.size, market.size)

    # blank image
    background = Image.new("RGBA", size)

    # image of pizza crust
    piz = Image.new("RGBA", size, 0xff52c1ea)

    tomato = Image.new("RGBA", size)
    sauce = ImageDraw.Draw(tomato)
    sauce.ellipse([4, 4, 60, 60], fill=0xff2440d8)

    piz = Image.alpha_composite(piz, tomato)

    # mask for circu-lating the pizza
    mask = _create_pizza_mask(size)

    # add toppings
    pizzaimg = Image.new("RGBA", size)

   # list comprehsenion
   
    for pair in pizza:
        for _, topping in pair:
            pizzaimg = Image.alpha_composite(pizzaimg, market.toppings[topping])

    pizzaimg = Image.alpha_composite(piz, pizzaimg)
    pizzaimg = Image.composite(pizzaimg, background, mask)

    return pizzaimg.resize((64 * 5, 64 * 5), Image.NEAREST)


def _create_pizza_mask(size):
    """
    Creates an ellipse of the needed size for an image mask to "carve out" pizza
    """

    mask = Image.new("RGBA", size)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, size], fill=0xffffffff)

    return mask

_MARKET_DICT = stock_kitchen()
