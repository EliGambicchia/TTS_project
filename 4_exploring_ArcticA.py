# Author: Elisa Gambicchia (2021)
# This script aims to explore the dataset "Arctic A", the diphones containing and their Zipf-like distribution

import re
import pandas as pd
from functools import reduce
import operator
from pprint import pprint
import collections
import matplotlib.pyplot as plt


def one_sentence_per_line_file(old_file, new_file, tag):
    with open(old_file, 'r') as f:

        text_to_process = f.read()
        utts_to_process = re.sub(r"\s", r" ", text_to_process)
        utts_to_process = re.sub(r"#!MLF!#", r"", utts_to_process)
        utts_to_process = re.sub(tag, r"\n\1", utts_to_process)

    file = open(new_file, "w") 
    output = utts_to_process
    file.write(output)
    file.close()

# DO NOT UNCOMMENT
one_sentence_per_line_file(old_file="utts_B.txt",
                           new_file="B_one_arctic_per_line.txt",
                           tag=r"(\"\*/arctic_a[0-9]+.lab\")")

def from_arctic_to_diphones():
    my_recipes_list = open("B_one_arctic_per_line.txt").readlines()

    divided_recipes_list = []
    for recipe in my_recipes_list:
        recipe_diphones_list = recipe.split(' ')
        divided_recipes_list.append(recipe_diphones_list)

    # eliminating short pause from the list of diphones-to-be
    useless_phones = ['t_cl', 'd_cl', 'g_cl', 'k_cl', 'p_cl', 'b_cl', 'sp', 'jh_cl', 'ch_cl', 'Q_cl', 'Q', '\n', '', '.']
    clean_recipes_list = []
    for recipe in divided_recipes_list:
        if len(recipe) == 2:  # in case there is an empty recipe
            pass
        else:
            recipe = [phone for phone in recipe if phone not in useless_phones]
            clean_recipes_list.append(recipe)

    # turning the list into a dictionary with recipe label as key
    recipe_dictionary = {recipe[0]:recipe[1:] for recipe in clean_recipes_list}

    # making diphones out of phones
    for key in recipe_dictionary:
        recipe_dictionary[key] = [[phone, phone] for phone in recipe_dictionary[key]]
        recipe_dictionary[key] = reduce(operator.add, recipe_dictionary[key])
        del recipe_dictionary[key][0] # eliminating the duplicated sil phone at the start

        recipe_dictionary[key] = [recipe_dictionary[key][i] + '-' + recipe_dictionary[key][i + 1]
                                  for i in range(0, len(recipe_dictionary[key])-1, 2)]

    return recipe_dictionary

def main():

    # dictionary with all recipes and their diphone sequence as value
    recipe_dict = from_arctic_to_diphones()

    # looking at zipf-like distribution
    all_diphones_in_sentences = []
    for key in recipe_dict:
        all_diphones_in_sentences.append(recipe_dict[key])

    all_diphones_in_sentences = reduce(operator.add, all_diphones_in_sentences)
    counts_of_diphones = collections.Counter(all_diphones_in_sentences)
    ordered_counts_of_diphones = collections.OrderedDict(counts_of_diphones.most_common())

    print(ordered_counts_of_diphones)
    print('Total unit types in arctic A: ', len(ordered_counts_of_diphones))

    # seeing how many diphones we have in total
    total_diphones = 0
    for key in ordered_counts_of_diphones:
        total_diphones += ordered_counts_of_diphones[key]

    print("Total diphones (including repetitions): ", total_diphones)

if __name__ == "__main__":
    main()