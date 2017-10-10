"""Turns a pizza tupple into an image"""

import json
from PIL import Image, ImageDraw


MARKET_DIR = "recipes/"
_IMAGE_DICT = {"premium": {}, "free": {}}

# TODO
# * Add pizza background image instead of drawing natively.
# * Load multiple recipes and vary size according to data. Define scale in JSON?


def stock_kitchen():
    """
    Fill up the internal dictionaries with all the images from the markets.
    """
    with open("recipes/basic/recipe.json") as _f:
        ingredientdict = json.load(_f)


    # TODO
    # * define one NULL image that is shared
    # * REFACTOR this
    for ingredient, imagefile in ingredientdict["category"]["premium"].items():
        if imagefile:
            _IMAGE_DICT["premium"][ingredient] = Image.open("recipes/basic/" + imagefile)
        else:
            _IMAGE_DICT["premium"][ingredient] = Image.new("RGBA", (64, 64))

    for ingredient, imagefile in ingredientdict["category"]["free"].items():
        if imagefile:
            _IMAGE_DICT["free"][ingredient] = Image.open("recipes/basic/" + imagefile)
        else:
            _IMAGE_DICT["free"][ingredient] = Image.new("RGBA", (64, 64))

def bake_pizza(pizza):
    """
        Create an image of the input pizza

        TODO: VARIABLE NAMES / ORGANIZATION OF THIS IS TERRIBLE

        REFACTOR REFACTOR REFACTOR
    """

    # blank image
    background = Image.new("RGBA", (64, 64))

    # image of pizza crust
    piz = Image.new("RGBA", (64, 64), 0xff52c1ea)

    tomato = Image.new("RGBA", (64, 64))
    sauce = ImageDraw.Draw(tomato)
    sauce.ellipse([4, 4, 60, 60], fill=0xff0440d8)

    piz = Image.alpha_composite(piz, tomato)

    # mask for circu-lating the pizza
    mask = _create_pizza_mask(64, 64)

    # add toppings
    pizzaimg = Image.new("RGBA", (64, 64))

    for ingredient in pizza[0]:
        pizzaimg = Image.alpha_composite(pizzaimg, _IMAGE_DICT["premium"][ingredient[1]])

    for ingredient in pizza[1]:
        pizzaimg = Image.alpha_composite(pizzaimg, _IMAGE_DICT["free"][ingredient[1]])

    pizzaimg = Image.alpha_composite(piz, pizzaimg)
    pizzaimg = Image.composite(pizzaimg, background, mask)

    return pizzaimg.resize((64 * 5, 64 * 5), Image.NEAREST)


def _create_pizza_mask(width, height):
    """
    Creates an ellipse of the needed size for an image mask to "carve out" pizza
    """

    mask = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, width, height], fill="white")

    return mask
