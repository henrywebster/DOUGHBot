import json
from PIL import Image, ImageDraw
import functools

import dough

MARKET_DIR = "recipes/"


def stockKitchen():
    """
    Fill up the internal dictionaries with all the images from the markets.
    """


def bakePizza(pizza, market):
    ingredientDict = {}

    imageDict = {}


    with open("recipes/basic/recipe.json") as f:
        ingredientDict = json.load(f)

    for ingredient, imageFile in ingredientDict["category"]["free"].items():
        if imageFile:
            imageDict[ingredient] = Image.open("recipes/basic/" + imageFile)

        # blank image
    background = Image.new("RGBA", (64, 64))

    # image of pizza crust
    piz = Image.new("RGBA", (64, 64), "orange")

    # mask for circu-lating the pizza
    mask = _createPizzaMask(64, 64)

    # add toppings
    pizzaImg = Image.new("RGBA", (64, 64))

    for ingredient in pizza[1]:
        pizzaImg = Image.alpha_composite(pizzaImg, imageDict[ingredient[1]])

        # put the toppings on the pizza
    pizzaImg = Image.alpha_composite(piz, pizzaImg)

    # put the pizza on the background
    pizzaImg = Image.composite(pizzaImg, background, mask)

    # scale up and display
    pizzaImg.resize((64 * 5, 64 * 5), Image.NEAREST).show()


def _createPizzaMask(width, height):
    """
    Creates an ellipse of the needed size for an image mask to "carve out" pizza
    """

    mask = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, width, height], fill="white")

    return mask

pizza = dough.generatePizza(100)
bakePizza(pizza, None)
