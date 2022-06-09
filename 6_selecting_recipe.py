# Author: Elisa Gambicchia (2021)

import re
from pprint import pprint

with open("ready_to_go_recipes.txt", 'r') as f:
    text_to_process = f.read()
    text_to_process = re.sub(r"\(\s(recipe_[0-9]+)\s\"", r"\1\n", text_to_process)
    text_to_process = re.sub(r"\"\s\)", r"", text_to_process)
    list_recipe = text_to_process.split('\n')

#creating a dictionary with recipe label as key and recipe text as value
recipe_dictionary = {}
for i in range(0, len(list_recipe)-1, 2):
    recipe_dictionary[list_recipe[i]] = list_recipe[i+1]

pprint(recipe_dictionary)


# getting all the recipes' names chosen by the algorithm
def getting_recipe_names():
    with open("chosen_recipes.txt", 'r') as f:
        text_to_process = f.read()
        text_to_process = re.sub(r"\"\*\/", r"", text_to_process)
        text_to_process = re.sub(r"\.lab\"", r"", text_to_process)

        list_recipe_names = text_to_process.split('\n')
        return list_recipe_names

list_recipe_names = getting_recipe_names()

# see which recipe to record
recipes_to_record = []
for key in recipe_dictionary.keys():
    if key in list_recipe_names:
        recipes_to_record.append(recipe_dictionary[key])

valid_input = []
for sentence in recipes_to_record:
    valid_sentence = "( recipe_" + "{:0>4d}".format(recipes_to_record.index(sentence)) + " \"" + sentence + "\" )"
    valid_input.append(valid_sentence)

file = open("recipes_ready_to_record.data", "w") 
for item in valid_input:
    file.write("\n" + item)
file.close()