import json
from PIL import Image, ImageDraw
import functools

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
		print(ingredient, imageFile)
		if imageFile:
			imageDict[ingredient] = Image.open("recipes/basic/" + imageFile)
		
	
	background = Image.new("RGBA", (64, 64), "white")
	piz = Image.new("RGBA", (64, 64), "orange")
	mask = Image.new("RGBA", (64, 64))
	draw = ImageDraw.Draw(mask)
	
	draw.ellipse([0, 0, 64, 64], fill="white")
	

	ph = Image.new("RGBA", (64, 64))
	
	# reduce
	for key, image in imageDict.items():
			ph = Image.alpha_composite(ph, image)
	
	
	ph = Image.alpha_composite(piz, ph)
	ph = Image.composite(ph, background, mask)
	ph.resize((64 * 5, 64 * 5), Image.NEAREST).show()
	


	
bakePizza(None, None)