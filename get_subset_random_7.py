import operator
from functools import reduce
import functools
import re
import matplotlib.pyplot as plt
import collections
import random
from pprint import pprint

"""needed for the selected subset"""
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

# i need the dictionary of all the corresponding recipes and corresponding diphones
def from_recipe_to_diphones(filename):
    my_recipes_list = open(filename).readlines()

    divided_recipes_list = []
    for recipe in my_recipes_list:
        recipe_diphones_list = recipe.split(' ')
        divided_recipes_list.append(recipe_diphones_list)

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
    recipe_dictionary = {recipe[0]:recipe[1:] for recipe in clean_recipes_list}

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
arctic_dict = from_recipe_to_diphones("one_arctic_per_line.txt")

'''1. RANDOM SELECTION - start '''
# getting a random list
def random_selection(recipe_dictionary, n_sents):

    # pseudo-random
    random.seed(40)

    only_keys = list(recipe_dictionary.keys())
    random_selected = []

    while len(random_selected) != n_sents:
        choice = random.choice(only_keys)
        if choice not in random_selected:
            random_selected.append(choice)
    return random_selected
# this is a list with a 200 randomly selected lines:

random_list = random_selection(arctic_dict, n_sents=200) # if you want less or more sentence CHANGE HERE!
'''1. RANDOM SELECTION - end '''

def getting_labels(random_list):
    random_list_2 = []
    for label in random_list: # for every element of the random list
        text_to_process = re.sub(r"\"\*\/", r"", label)
        text_to_process = re.sub(r"\.lab\"", r"", text_to_process)
        random_list_2.append(text_to_process)

    return random_list_2

random_list_matches = getting_labels(random_list)
random_list_matches.sort()

# FROM LABELS TO THE ACTUAL SENTENCES -- OUTPUT FILE READY TO GO THROUGH MLF
def ordered_sentences_utt_format(filename, match_list, new_file):
    with open(filename, 'r') as f:
        sentences = f.read()
        sentences = sentences.split('\n')
        actual_sentences = [] # I need to store the selected sentences
        for match in match_list: # for each label
            for sentence in sentences: # for each sentence
                if re.search(match, sentence):
                    actual_sentences.append(sentence)

    file = open(new_file, "w") # write mode
    for item in actual_sentences:
        file.write(item + "\n")
    file.close()

ordered_sentences_utt_format(filename="artic_utts.txt",
                             match_list=random_list_matches,
                             new_file="artic_random_utts.txt")

'''SELECTED -- start '''

chosen_recipes = open("chosen_recipes.txt").readlines()
chosen_recipes = [re.sub(r"\n", r"", line) for line in chosen_recipes] #they had a /n at the end, removed

all_recipes_list = open("one_recipe_per_line.txt").readlines()
label_dictionary = {}
for recipe in all_recipes_list:
    each_recipe = recipe.split(" ") # i want only the first part, recipe label
    if each_recipe[0] in chosen_recipes:
        label_dictionary[each_recipe[0]] = each_recipe[1:]

def from_recipes_to_diphone_counts(dictionary):
    # setting up a dictionary to look at zipf-like distribution
    all_diphones_in_sentences = []
    for key in dictionary:
        all_diphones_in_sentences.append(dictionary[key])

    all_diphones_in_sentences = reduce(operator.add, all_diphones_in_sentences)
    counts_of_diphones = collections.Counter(all_diphones_in_sentences)
    ordered_counts_of_diphones = collections.OrderedDict(counts_of_diphones.most_common())

    print('Total different diphones in sentences in Arctic: ', len(ordered_counts_of_diphones))

    # how many diphones we have in total
    total_diphones = 0
    for key in ordered_counts_of_diphones:
        total_diphones += ordered_counts_of_diphones[key]

    print("Total diphones (including repetitions) in Arctic: ", total_diphones)
    return ordered_counts_of_diphones

ordered_counts_of_diphones_artic = from_recipes_to_diphone_counts(arctic_dict)

# EXTRA DIPHONES FROM ARCTIC A THAT ARE NOT IN RECIPES
def from_dict_to_diphones(dictionary):

    useless_phones = ['t_cl', 'd_cl', 'g_cl', 'k_cl', 'p_cl', 'b_cl', 'sp', 'jh_cl', 'ch_cl', 'Q_cl', 'Q', '\n', '', '.']
    clean_recipes_list = []
    # abandoning labels and removing useless phones
    for key in dictionary:
        recipe = [phone for phone in dictionary[key] if phone not in useless_phones]
        clean_recipes_list.append(recipe)

    # making diphones out of phones
    diphone_bag_list = []
    for lst in clean_recipes_list: # for each recipe
        if lst != []:
            lst = [[phone, phone] for phone in lst] # duplicating phone
            lst = reduce(operator.add, lst)

            del lst[0] # eliminating the duplicated sil phone at the start
            diphone_lst = [lst[i] + '-' + lst[i + 1] for i in range(0, len(lst) - 1, 2)]
            diphone_bag_list.append(diphone_lst)

    diphone_bag_list = functools.reduce(operator.iconcat, diphone_bag_list, [])

    return diphone_bag_list

diph_bag_recipes = from_dict_to_diphones(label_dictionary) #this is a list of all the diphones in Recipes
counts_diph_recipes = collections.Counter(diph_bag_recipes)

extra_diphones = {}
once_only = []
for key in ordered_counts_of_diphones_artic.keys():
    if key not in counts_diph_recipes.keys():
        extra_diphones[key] = ordered_counts_of_diphones_artic[key]

        # i want to see how many are only appearing once
        if ordered_counts_of_diphones_artic[key] == 1:
            once_only.append(key)

print("Amount of extra_diphones in Arctic A that we want to add in our Recipes: ", len(extra_diphones))
print("Appearing only once: ", len(once_only), "\n")

# WEIGHTED DICTIONARY FOR SCORING
def weight_dict(ordered_counts, extra_diphones): # takes a dict
    #weight dictionary that assigns different weights to diphones depending on their frequency
    weight_dictionary = {}
    for key in ordered_counts.keys():
        if key in extra_diphones:
            weight_dictionary[key] = 10000
        elif ordered_counts[key] <= 10:
            weight_dictionary[key] = 1000
        elif ordered_counts[key] > 10 and ordered_counts[key] <= 100:
            weight_dictionary[key] = 250
        elif ordered_counts[key] > 100:
            weight_dictionary[key] = 1
    return weight_dictionary

weight_dictionary = weight_dict(ordered_counts_of_diphones_artic, extra_diphones)

def greedy_algorithm(recipe_dict, wish_list, how_many):

    list_of_chosen_recipes = []
    diphones_contained_in_chosen_recipes = {}
    new_diphones = []  # to see the increment in diphones, and then decrease
    total_diph_algorithm = 0  # total diphones
    t = 0

    # considering all our dataset available!
    while t != how_many:
        #print(t)
        scoring_dictionary = {}  # scoring all the sentences
        for key in recipe_dict:
            if recipe_dict[key] != []:
                set_diphones = set(recipe_dict[key]) # only one per type -- not counting duplicates
                sentence_score = 0
                for diphone in set_diphones:
                    sentence_score += weight_dictionary[diphone]

                norm_sentence_score = sentence_score/len(set_diphones) # normalising by dividing by number of diphones in the string
                scoring_dictionary[key] = norm_sentence_score

        # getting the recipe label
        best_scored_recipe = max(scoring_dictionary, key=scoring_dictionary.get)

        wish_list_update = [x for x in wish_list if x not in recipe_dict[best_scored_recipe]]

        if len(wish_list_update) == len(wish_list):
            #print(f"Deleting this {best_scored_recipe} from the dataset")
            del recipe_dict[best_scored_recipe]
        else:
            # storing each time, the increment of the dictionary
            new_diphones.append(len(wish_list) - len(wish_list_update))
            t += 1

            #print("Diphones added in our script: ", len(wish_list) - len(wish_list_update))

            list_of_chosen_recipes.append(best_scored_recipe) # to track the recipe

            # accumulating the diphones selected
            for diphone in recipe_dict[best_scored_recipe]:
                total_diph_algorithm += 1 # we need to store also how many
                if diphone in diphones_contained_in_chosen_recipes:
                    diphones_contained_in_chosen_recipes[diphone] += 1
                else:
                    diphones_contained_in_chosen_recipes[diphone] = 1

            # removing the best sentence
            recipe_dict.pop(best_scored_recipe)
            wish_list = wish_list_update

    print('Total diphones in sentences after algorithm for SELECTED: ', len(diphones_contained_in_chosen_recipes))

    return diphones_contained_in_chosen_recipes, list_of_chosen_recipes

diphs_in_subset_arctic, chosen_arctic_sentences = greedy_algorithm(arctic_dict, wish_list, 200)
#print("diphs_in_subset_arctic: ", diphs_in_subset_arctic)

# how many diphones we have in total
total_diphones_after = 0
# checking that they are all inserted
sanity_check = 0
for key in diphs_in_subset_arctic.keys():
    total_diphones_after += diphs_in_subset_arctic[key]
    if key in extra_diphones:
        sanity_check += 1

print("Total diphones (including repetitions) for our SELECTED: ", total_diphones_after)
print("Amount of extra diphones in SELECTED: ", sanity_check, "\n")

# to get the file ready for MLF for the selected arctic sentences
selected_list_matches = getting_labels(chosen_arctic_sentences)
selected_list_matches.sort()
ordered_sentences_utt_format(filename="artic_utts.txt",
                             match_list=selected_list_matches,
                             new_file="artic_selected_utts.txt")
'''SELECTED -- end'''

'''RANDOMLY SELECTED -- stats start'''
# NEXT: LOOK AT THE DISTRIBUTION OF THE DIPHONES IN THIS RANDOMLY SELECTED GROUP!
def looking_zipf_distribution_from_list(list_to_check, dict, type):

    all_diphones_in_sentences = []

    keys_with_tags = []
    for key in list_to_check:
        keys_with_tags.append("\"*/" + key + ".lab\"")
    for key in keys_with_tags:
        all_diphones_in_sentences.append(dict[key])

    all_diphones_in_sentences = reduce(operator.add, all_diphones_in_sentences)
    counts_of_diphones = collections.Counter(all_diphones_in_sentences)
    ordered_counts_of_diphones = collections.OrderedDict(counts_of_diphones.most_common())

    print(f'Different diphones in {type}: ', len(ordered_counts_of_diphones))

    # how many diphones we have in total
    extra_diphones_included = 0
    total_diphones = 0
    for key in ordered_counts_of_diphones:
        total_diphones += ordered_counts_of_diphones[key]
        if key in extra_diphones:
            extra_diphones_included += 1

    print(f"Diphones (including repetitions) of {type}: ", total_diphones)
    print(f"Extra diphones of {type}: ", extra_diphones_included)

    return ordered_counts_of_diphones # the dictionary

arctic_dict2 = from_recipe_to_diphones("one_arctic_per_line.txt") # add to create another one because of problem of subtraction in greedy algorithm


# info about diphones selected
diphones_info_random = looking_zipf_distribution_from_list(random_list_matches,
                                                           arctic_dict2,
                                                           type="random sentences")
'''RANDOMLY SELECTED -- stats end'''


'''VISUAL'''

# randomly selected diphones
def getting_plot(diphones_info,
                 color=None,
                 title=None,
                 name_sav=None):
    keys = diphones_info.keys()
    values = diphones_info.values()
    plt.bar(keys, values, color=color)
    plt.xlabel(f"Diphones (N={len(diphones_info)}), ordered by frequency")
    plt.ylabel("Frequency")
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
    plt.title(title)
    plt.savefig(name_sav)
    plt.clf()

"""RANDOM"""
getting_plot(diphones_info=diphones_info_random,
             color='#984ea3', # purple
             title="Zipf-like distribution of diphones \n randomly selected from Arctic A.",
             name_sav="zipf-like distribution_artic_random.pdf")

"""SELECTED"""
ord_diphs_in_subset_arctic = dict(sorted(diphs_in_subset_arctic.items(), key=operator.itemgetter(1), reverse=True))
getting_plot(diphones_info=ord_diphs_in_subset_arctic,
             color='#dede00', # yellow
             title="Zipf-like distribution of diphones \n selected via greedy algorithm from Arctic A.",
             name_sav="zipf-like distribution_artic_greedy.pdf")
'''
def getting_plot_for_diphones():
    x = list(range(len(new_diphones)))
    plt.plot(x, new_diphones, color='#4daf4a') # green
    plt.xlabel(f"Amount of sentences selected (N={len(x)})")
    plt.ylabel("Amount of diphones inserted in the script")
    plt.xticks(np.arange(0, len(x), 50))
    plt.axhline(y=1, color='black', linestyle='--')

    plt.title("Diphones' selection during the greedy algorithm.")
    plt.savefig("diphones' selection in algorithm - recipes.pdf")

getting_plot_for_diphones()
'''