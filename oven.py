import json
from PIL import Image, ImageDraw


import dough

MARKET_DIR = "recipes/"
_IMAGE_DICT = {}


def stock_kitchen():
    """
    Fill up the internal dictionaries with all the images from the markets.
    """
    with open("recipes/basic/recipe.json") as f:
        ingredientdict = json.load(f)

    for ingredient, imagefile in ingredientdict["category"]["free"].items():
        if imagefile:
            _IMAGE_DICT[ingredient] = Image.open("recipes/basic/" + imagefile)
        else:
            _IMAGE_DICT[ingredient] = Image.new("RGBA", (64, 64))


def bake_pizza(pizza):
    """
	Create an image of the input pizza
    """

    # blank image
    background = Image.new("RGBA", (64, 64))

    # image of pizza crust
    piz = Image.new("RGBA", (64, 64), 0xff52c1ea)

    # mask for circu-lating the pizza
    mask = _createPizzaMask(64, 64)

    # add toppings
    pizzaimg = Image.new("RGBA", (64, 64))

    for ingredient in pizza[1]:
        pizzaimg = Image.alpha_composite(pizzaimg, _IMAGE_DICT[ingredient[1]])

    pizzaimg = Image.alpha_composite(piz, pizzaimg)
    pizzaimg = Image.composite(pizzaimg, background, mask)

    return pizzaimg.resize((64 * 5, 64 * 5), Image.NEAREST)

def _createPizzaMask(width, height):
    """
    Creates an ellipse of the needed size for an image mask to "carve out" pizza
    """

    mask = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, width, height], fill="white")

    return mask