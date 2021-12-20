import re
import pandas as pd
from functools import reduce
import operator
from pprint import pprint
import collections
import matplotlib.pyplot as plt
import exploring_artic_A_4
import numpy as np

def create_wish_list():
    '''
    need to create all the possible diphones that we would need in the database
    :return: the list of diphones
    '''
    phone_list1 = ['sil', 's', 't', 'aa', 'f', 'sp', 'd', 'y', 'uu', 'p', 'l', 'i', 'k', 'ei', 'sh', 'n!', '@', 'n', 'b', 'ii', 'm', 'z', 'ai', 'ng', 'a', 'lw', 'g', 'ou', 'r', 'iy', 'w', 'dh', 'eir', 'uw', 'ch', '@@r', 'e', 'v', 'oi', 'h', 'th', 'oo', 'l!', 'ow', 'o', 'uh', 'u', 'i@', 'jh', 'ur', 'zh', 'm!']
    phone_list2 = ['sil', 's', 't', 'aa', 'f', 'sp', 'd', 'y', 'uu', 'p', 'l', 'i', 'k', 'ei', 'sh', 'n!', '@', 'n', 'b', 'ii', 'm', 'z', 'ai', 'ng', 'a', 'lw', 'g', 'ou', 'r', 'iy', 'w', 'dh', 'eir', 'uw', 'ch', '@@r', 'e', 'v', 'oi', 'h', 'th', 'oo', 'l!', 'ow', 'o', 'uh', 'u', 'i@', 'jh', 'ur', 'zh', 'm!']

    diphone_wish_list = []
    for phone1 in phone_list1:
        for phone2 in phone_list2:
            diphone = phone1 + '-' + phone2
            diphone_wish_list.append(diphone)

    return diphone_wish_list

wish_list = create_wish_list()
print('Total potential diphones in wish list: ', len(wish_list))
# print(wish_list)


def one_recipe_per_line_file():
    with open("utts-mlf-recipes.txt", 'r') as f:
        text_to_process = f.read()

        utts_to_process = re.sub(r"\s", r" ", text_to_process)
        utts_to_process = re.sub(r"#!MLF!#", r"", utts_to_process)
        utts_to_process = re.sub(r"(\"\*/recipe_[0-9]+.lab\")", r"\n\1", utts_to_process)

    file = open("one_recipe_per_line.txt", "w") # write mode
    output = utts_to_process
    file.write(output)
    file.close()

one_recipe_per_line_file()

def from_recipe_to_diphones(filename):
    my_recipes_list = open(filename).readlines()

    divided_recipes_list = []
    for recipe in my_recipes_list:
        recipe_diphones_list = recipe.split(' ')
        divided_recipes_list.append(recipe_diphones_list)
    print("sentences: ", len(divided_recipes_list))
    # eliminating short pause from the list of diphones-to-be
    useless_phones = ['t_cl', 'd_cl', 'g_cl', 'k_cl', 'p_cl', 'b_cl', 'sp', 'jh_cl', 'ch_cl', 'Q_cl', 'Q', '\n', '', '.']
    clean_recipes_list = []
    for recipe in divided_recipes_list:
        if len(recipe) == 2: # in case there is an empty recipe
            pass
        else:
            recipe = [phone for phone in recipe if phone not in useless_phones]
            clean_recipes_list.append(recipe)

    # turning the list into a dictionary with recipe label as key
    recipe_dictionary = {recipe[0]: recipe[1:] for recipe in clean_recipes_list}

    # making diphones out of phones
    for key in recipe_dictionary:
        if recipe_dictionary[key] != []: # if the recipe is not empty
            recipe_dictionary[key] = [[phone, phone] for phone in recipe_dictionary[key]]
            recipe_dictionary[key] = reduce(operator.add, recipe_dictionary[key])
            del recipe_dictionary[key][0] # eliminating the duplicated sil phone at the start

            recipe_dictionary[key] = [recipe_dictionary[key][i] + '-' + recipe_dictionary[key][i + 1]
                                      for i in range(0, len(recipe_dictionary[key])-1, 2)]

    return recipe_dictionary

# dictionary with all recipes and their diphone sequence as value
recipe_dict = from_recipe_to_diphones("one_recipe_per_line.txt")

def from_recipes_to_diphone_counts(dictionary):
    # setting up a dictionary to look at zipf-like distribution
    all_diphones_in_sentences = []
    for key in dictionary:
        all_diphones_in_sentences.append(dictionary[key])

    all_diphones_in_sentences = reduce(operator.add, all_diphones_in_sentences)
    counts_of_diphones = collections.Counter(all_diphones_in_sentences)
    ordered_counts_of_diphones = collections.OrderedDict(counts_of_diphones.most_common())

    print('Total different diphones in sentences: ', len(ordered_counts_of_diphones))

    # how many diphones we have in total
    total_diphones = 0
    for key in ordered_counts_of_diphones:
        total_diphones += ordered_counts_of_diphones[key]

    print("Total diphones (including repetitions): ", total_diphones)
    return ordered_counts_of_diphones

ordered_counts_of_diphones = from_recipes_to_diphone_counts(recipe_dict)

# '''from the other script'''
# # dictionary with all recipes and their diphone sequence as value
# art_dict = exploring_artic_A_4.from_arctic_to_diphones()
#
# # looking at zipf-like distribution
# all_diphones_in_sentences_art = []
# for key in art_dict:
#     all_diphones_in_sentences_art.append(art_dict[key])
#
# all_diphones_in_sentences_art = reduce(operator.add, all_diphones_in_sentences_art)
# counts_of_diphones_art = collections.Counter(all_diphones_in_sentences_art)
# ordered_counts_of_diphones_art = collections.OrderedDict(counts_of_diphones_art.most_common())
#
# print('Total diphones in arctic A: ', len(ordered_counts_of_diphones_art))
#
# # i want to see how frequent are the diphones that are extra in our Recipes domain -- are we getting rare diphones??
#
# extra_diphones = {}
# for key in ordered_counts_of_diphones.keys():
#     if key not in ordered_counts_of_diphones_art.keys():
#         extra_diphones[key] = ordered_counts_of_diphones[key]
#
# print("Amount of extra_diphones: ", len(extra_diphones))

#
# def getting_plot_recipes_before():
#     # figure
#     keys = ordered_counts_of_diphones.keys()
#     values = ordered_counts_of_diphones.values()
#     plt.bar(keys, values, color='#377eb8')
#     plt.xlabel(f"Diphones (N={len(ordered_counts_of_diphones)}), ordered by frequency")
#     plt.ylabel("Frequency")
#     plt.tick_params(
#         axis='x',          # changes apply to the x-axis
#         which='both',      # both major and minor ticks are affected
#         bottom=False,      # ticks along the bottom edge are off
#         top=False,         # ticks along the top edge are off
#         labelbottom=False) # labels along the bottom edge are off
#     plt.title("Zipf-like distribution of diphones in Recipes \n before the selection algorithm.")
#     plt.savefig("zipf-like distribution_before.pdf")
#     plt.clf()
#
# getting_plot_recipes_before()
#
# def weight_dict(ordered_counts): # takes a dict
#     #weight dictionary that assigns different weights to diphones depending on their frequency
#     weight_dictionary = {}
#     for key in ordered_counts.keys():
#         if key in extra_diphones:
#             weight_dictionary[key] = 1000
#         elif ordered_counts[key] <= 10:
#             weight_dictionary[key] = 1000
#         elif ordered_counts[key] > 10 and ordered_counts[key] <= 100:
#             weight_dictionary[key] = 250
#         elif ordered_counts[key] > 100:
#             weight_dictionary[key] = 1
#     return weight_dictionary
#
# weight_dictionary = weight_dict(ordered_counts_of_diphones)
#
# list_of_chosen_recipes = []
# diphones_contained_in_chosen_recipes = {}
# new_diphones = [] #to see the increment in diphones, and then decrease
# total_diph_algorithm = 0 # total diphones
# t = 0
#
# # considering all our dataset available!
# # two conditions to stop: same diphones as in Arctic or we have all the different diphones
# #while total_diph_algorithm < 19611 or len(diphones_contained_in_chosen_recipes) != len(ordered_counts_of_diphones):
# while t != 534: # it seems that it stops after 551
#
#     print(t)
#     scoring_dictionary = {}  # scoring all the sentences
#     for key in recipe_dict:
#         if recipe_dict[key] != []:
#             set_diphones = set(recipe_dict[key]) # only one per type -- not counting duplicates
#             sentence_score = 0
#             for diphone in set_diphones:
#                 sentence_score += weight_dictionary[diphone]
#
#             norm_sentence_score = sentence_score/len(set_diphones) # normalising by dividing by number of diphones in the string
#             scoring_dictionary[key] = norm_sentence_score
#
#     # getting the recipe label
#     try:
#         best_scored_recipe = max(scoring_dictionary, key=scoring_dictionary.get)
#     except ValueError: # it means that we don't have any recipe anymore
#         continue
#         # PROBLEM --- IT WILL KEEP GOING FOREVER!
#     wish_list_update = [x for x in wish_list if x not in recipe_dict[best_scored_recipe]]
#
#     if len(wish_list_update) == len(wish_list):
#         print(f"Deleting this {best_scored_recipe} from the dataset")
#         del recipe_dict[best_scored_recipe]
#     else:
#         # storing each time, the increment of the dictionary
#         new_diphones.append(len(wish_list) - len(wish_list_update))
#         t += 1
#
#         print("Diphones added in our script: ", len(wish_list) - len(wish_list_update))
#
#         list_of_chosen_recipes.append(best_scored_recipe) # to track the recipe
#
#         # accumulating the diphones selected
#         for diphone in recipe_dict[best_scored_recipe]:
#             total_diph_algorithm += 1 # we need to store also how many
#             if diphone in diphones_contained_in_chosen_recipes:
#                 diphones_contained_in_chosen_recipes[diphone] += 1
#             else:
#                 diphones_contained_in_chosen_recipes[diphone] = 1
#
#
#         # removing the best sentence
#         recipe_dict.pop(best_scored_recipe)
#         wish_list = wish_list_update
#
#
# print('Total diphones in sentences after algorithm: ', len(diphones_contained_in_chosen_recipes))
# print("These are the diphones chosen: ", diphones_contained_in_chosen_recipes)
#
# # how many diphones we have in total
#
# total_diphones_after = 0
# # checking that they are all inserted
# sanity_check = 0
# for key in diphones_contained_in_chosen_recipes.keys():
#     total_diphones_after += diphones_contained_in_chosen_recipes[key]
#     if key in extra_diphones:
#         sanity_check +=1
# print("amount of extra diphones:", sanity_check)
# print("Total diphones (including repetitions): ", total_diphones_after)
#
# # seeing the potential improvement
# def getting_plot_after_selection():
#     ord_diphones_contained_in_chosen_recipes = dict(sorted(diphones_contained_in_chosen_recipes.items(), key=operator.itemgetter(1), reverse=True))
#     keys = ord_diphones_contained_in_chosen_recipes.keys()
#     values = ord_diphones_contained_in_chosen_recipes.values()
#     plt.bar(keys, values, color='#377eb8') #blue
#     plt.xlabel(f"Diphones (N={len(ord_diphones_contained_in_chosen_recipes)}), ordered by frequency")
#     plt.ylabel("Frequency")
#
#     plt.tick_params(
#         axis='x',          # changes apply to the x-axis
#         which='both',      # both major and minor ticks are affected
#         bottom=False,      # ticks along the bottom edge are off
#         top=False,         # ticks along the top edge are off
#         labelbottom=False) # labels along the bottom edge are off
#     plt.title("Zipf-like distribution of diphones in Recipes \n after running the selection algorithm.")
#     plt.savefig("zipf-like distribution after algorithm-recipes.pdf")
#     plt.clf()
#
# getting_plot_after_selection()
#
# def getting_plot_for_diphones():
#     x = list(range(len(new_diphones)))
#     plt.plot(x, new_diphones, color='#4daf4a') # green
#     plt.xlabel(f"Amount of sentences selected (N={len(x)})")
#     plt.ylabel("Amount of diphones inserted in the script")
#     plt.xticks(np.arange(0, len(x), 50))
#     plt.axhline(y=1, color='black', linestyle='--')
#
#     plt.title("Diphones' selection during the greedy algorithm.")
#     plt.savefig("diphones' selection in algorithm - recipes.pdf")
#     plt.clf()
#
# getting_plot_for_diphones()
#
# file = open("chosen_recipes.txt", "w") # write mode
# for item in list_of_chosen_recipes:
#     file.write("\n" + item)
# file.close()
#
# # # write a file with chosen recipes ready for mlf
# # for item in list_of_chosen_recipes:
