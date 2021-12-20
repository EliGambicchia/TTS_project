import re
import matplotlib.pyplot as plt
import collections
import numpy as np
from statistics import stdev

def words_recipes():
    with open("recipes_ready_to_record.txt", 'r') as f:

        utts_to_process = f.read()
        utts_to_process = re.sub(r"\(\srecipe_[0-9]+\s\"", r"", utts_to_process)
        utts_together = re.sub(r"\"\s\)\n", r" ", utts_to_process)

        words_list = utts_together.split(' ')

        return len(words_list), utts_to_process

def words_arctic():
    with open("artic_utts.txt", 'r') as f:
        utts_to_process = f.read()

        utts_to_process = re.sub(r"\(\sarctic_a[0-9]+\s\"", r"", utts_to_process)
        utts_together = re.sub(r"\"\s\)\n", r" ", utts_to_process)

        words_list = utts_together.split(' ')

        return len(words_list), utts_to_process

def words_counts(big_string):
    utt_list = big_string.split('\n')
    total_length_utt = 0
    utt_len_list = []
    for utt in utt_list:
        if len(utt) != 0:
            total_length_utt += len(utt) # i will make the average at the end of all the sentences
            utt_len_list.append(len(utt)) # i want to store how long each sentence is for the graph
    print("SD: ", stdev(utt_len_list))
    average_len = total_length_utt/len(utt_list)

    return average_len, utt_len_list

def plot_for_len_sentences(utt_len_list,
                           color=None,
                           title=None,
                           name_sav=None,
                           x_step=None,
                           avg_length=None
                           ):

    count_utt_len = collections.Counter(utt_len_list)

    keys = count_utt_len.keys()
    values = count_utt_len.values()
    plt.bar(keys, values, color=color)
    plt.xlabel("Sentence length (in characters) ")
    plt.ylabel("Frequency")
    plt.xticks(np.arange(0, max(utt_len_list), x_step))
    plt.axvline(x=avg_length, color='black', linestyle='--')
    plt.title(title)

    plt.savefig(name_sav)
    plt.clf()


print("Total words in chosen Recipes: ", words_recipes()[0])
big_string_recipe = words_recipes()[1]
print("Average utterance length for Recipes: ", words_counts(big_string_recipe)[0])
plot_for_len_sentences(words_counts(big_string_recipe)[1],
                       color='#377eb8',
                       title="Sentence length in Recipes (in characters).",
                       name_sav="Sentence length in Recipes.pdf",
                       x_step=20,
                       avg_length=words_counts(big_string_recipe)[0]
                       )

print("Total words in arctic A: ", words_arctic()[0])
string_arctic = words_arctic()[1]
print("Average utterance length for Arctic: ", words_counts(string_arctic)[0])
plot_for_len_sentences(words_counts(string_arctic)[1],
                       color='#ff7f00',
                       title="Sentence length in Arctic A (in characters).",
                       name_sav="Sentence length in Arctic A.pdf",
                       x_step=20,
                       avg_length=words_counts(string_arctic)[0]
                       )
