import json
import os
import dough

RECIPE_DIR = "recipes"

def printWarning(message, category):
	print("[warning] ({}) {}".format(category, message))

def validateCategory(category, localList, globalList):
	localListError = []
	globalListError = []
	
	rwFlag = False
	
	#in future, append mismatches to recipe file
	
	for ingredient in localList:
		if ingredient not in globalList:
			localListError.append(ingredient)
	
	for ingredient in globalList:
		if ingredient not in localList:
			globalListError.append(ingredient)
			rwFlag = True
			localList[ingredient] = None
	
	if localListError:
		printWarning("entries in local list not in global list:", category)
		for ingredient in localListError:
			print("\t* {}".format(ingredient))	
		print("\tThese ingredients won't be added until entered into the global list")
			
	if globalListError:
		printWarning("entries in master list not in the recipe:", category)
		for ingredient in globalListError:
			print("\t* {}".format(ingredient))
		print("\tThe oven won't know how to make the ingredient, nulls will be added to json file")
		
	return rwFlag
	
def validateRecipeDir(dir):
	
	rwFlag = False
	for subdir, dir, files in os.walk(RECIPE_DIR):
		for recipeDir in dir:
			
			print("Recipe: ", recipeDir)
			f = open("{}/{}/recipe.json".format(RECIPE_DIR, recipeDir), 'r+')
			recipes = json.load(f)
			
			rwFlag = True if validateCategory("premium", recipes["category"]["premium"], dough.PREMIUM_LIST) else rwFlag
			rwFlag = True if validateCategory("free", recipes["category"]["free"], dough.FREE_LIST) else rwFlag
			
			if rwFlag:
				f.seek(0)
				json.dump(recipes, f, sort_keys=True, indent=4, separators=(',',': '))
				f.truncate(f.tell())
			
			f.close()
		
	
if __name__ == "__main__":
	validateRecipeDir(RECIPE_DIR)


	

