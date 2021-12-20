from pprint import pprint
from statistics import stdev

with open("test_sentences.txt", 'r') as f:
    utts_to_process = f.read()

    utts_to_process = utts_to_process.splitlines()
    pprint(utts_to_process)

mean_length_recipes = 0
mean_length_harvard = 0

print("hey: ", utts_to_process[5:11])
for utt in utts_to_process:
    print(utt, len(utt))
    if utt in utts_to_process[0:5]:
        mean_length_recipes += len(utt)
    else:
        mean_length_harvard += len(utt)

mean_length_recipes = mean_length_recipes / (len(utts_to_process)/2)
print("Recipes mean: ", mean_length_recipes)

mean_length_harvard = mean_length_harvard / (len(utts_to_process)/2)
print("Harvard mean: ", mean_length_harvard)

recipes_sd = round(stdev([len(utt) for utt in utts_to_process[0:5]]), 2)
print("Recipes sd: ", recipes_sd)

harvard_sd = round(stdev([len(utt) for utt in utts_to_process[5:11]]), 2)
print("Harvard sd: ", harvard_sd)

pprint(utts_to_process)

long_sentences_recipes_mean = ((len(utts_to_process[0]) + len(utts_to_process[1])) / 2)
print("Rec mean: ", long_sentences_recipes_mean)
long_recipe_sd = round(stdev([len(utt) for utt in utts_to_process[0:2]]), 2)
print("Rec sd: ", long_recipe_sd)

long_sentences_harv_mean = ((len(utts_to_process[8]) + len(utts_to_process[9])) / 2)
print("Harvard mean: ", long_sentences_harv_mean)
long_harvard_sd = round(stdev([len(utt) for utt in utts_to_process[8:10]]), 2)
print("Harvard sd: ", long_harvard_sd)

# Short sentences
short_sentences_recipes_mean = ((len(utts_to_process[2]) + len(utts_to_process[3]) + len(utts_to_process[4])) / 3)
print("Rec short mean: ", round(short_sentences_recipes_mean, 2))
short_recipe_sd = round(stdev([len(utt) for utt in utts_to_process[2:5]]), 2)
print("Rec short sd: ", short_recipe_sd)

short_sentences_harv_mean = ((len(utts_to_process[5]) + len(utts_to_process[6]) + len(utts_to_process[7])) / 3)
print("Harvard short mean: ", short_sentences_harv_mean)
short_harvard_sd = round(stdev([len(utt) for utt in utts_to_process[5:8]]), 2)
print("Harvard short sd: ", short_harvard_sd)

valid_input = []
for sentence in utts_to_process:
    valid_sentence = "( test_" + "{:0>4d}".format(utts_to_process.index(sentence)) + " \"" + sentence + "\" )"
    valid_input.append(valid_sentence)

file = open("test_sentences.data", "w") # write mode
for item in valid_input:
    file.write("\n" + item)
file.close()