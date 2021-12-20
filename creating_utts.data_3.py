from pprint import pprint
from functools import reduce
import operator

with open("pre-processed_recipes3.0.txt", 'r') as f:
    text_to_process = f.read()
    list_sentences = text_to_process.split('\n')

    ext_list_sentences = []
    for sentence in list_sentences:
        if len(sentence) > 50:
            sentence = sentence.split(',')
            ext_list_sentences.append(sentence)
    ext_list_sentences = reduce(operator.add, ext_list_sentences)

    for sentence in list_sentences:
        if len(sentence) <= 50:
            if sentence == '':
                ext_list_sentences.append(sentence)

    ext_set_sentences = set(ext_list_sentences) # i do not want duplicates of my sentences
    ext_list_sentences2 = list(ext_set_sentences) #i want to index it later so converting it into a list again

print(len(ext_list_sentences2))
valid_input = []
for sentence in ext_list_sentences2:
    valid_sentence = "( recipe_" + "{:0>5d}".format(ext_list_sentences2.index(sentence)) + " \"" + sentence + "\" )"
    valid_input.append(valid_sentence)

#
# file = open("ready_to_go_recipes2.txt", "w") # write mode
# for item in valid_input:
#     file.write("\n" + item)
# file.close()
