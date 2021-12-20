#from this guy:
# https://github.com/miguelfzafra/Latest-News-Classifier/blob/master/0.%20Latest%20News%20Classifier/05.%20News%20Scraping/17.%20WS%20-%20El%20Pais.ipynb

import numpy as np
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd

# get the HTML content
general_link = "https://www.jamieoliver.com/recipes/category/special-diets/vegetarian/"
r1 = requests.get(general_link)
coverpage = r1.content

# beautiful soup
soup1 = BeautifulSoup(coverpage, 'html.parser')
coverpage_recipes = soup1.find_all(class_= "recipe-block")

print("total recipe titles:", len(coverpage_recipes))

# getting only link
list_links_cut = []
for recipe in coverpage_recipes:
    list_links_cut.append(recipe.find('a')['href'])
print(len(list_links_cut))

#appending https://www.jamieoliver.com
list_links_completed = []
for link in list_links_cut:
    link = ''.join(('https://www.jamieoliver.com', link))
    list_links_completed.append(link)

print(list_links_completed)

recipe_contents = []

# saving them into a text file
sys.stdout = open("all_recipes.txt", "w")

for link in list_links_completed:
    recipe = requests.get(link)
    recipe_content = recipe.content
    soup_article = BeautifulSoup(recipe_content, 'html.parser')
    body = soup_article.find_all('ol', class_='recipeSteps')
    # x = body[0].find_all('li')
    recipe_contents.append(body)
    print(body)

print(f"done. total recipes: {len(recipe_contents)}")

sys.stdout.close()

# df_features
# df_features = pd.DataFrame(
#      {'Article Link': list_links_completed, 'Article Content': recipe_contents
#     })
#
# df_features