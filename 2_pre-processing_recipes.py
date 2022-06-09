# Author: Elisa Gambicchia (2021)
# This script does a deep cleaning of the web-scraped text

import re
from pprint import pprint
import collections

# split the file into single sentences
def pre_process(textfile):
    with open(textfile, 'r') as f:
        print(f'Opening file: "{textfile}"...')
        text_to_process = f.read()

        # replacing spaces at the end of a sentence with new line 
        text_to_process = re.sub(r"([.?!:])\s", r"\1\s", text_to_process)
        text_to_process = re.sub(r"\n", r"", text_to_process)
        text_to_process = re.sub(r"([\.!]\))\s", r"\1\n", text_to_process)

        # replacing some web tags
        text_to_process = re.sub(r"\[<ol class=\"recipeSteps\"><li>", r"", text_to_process)
        text_to_process = re.sub(r"</li></ol>, <ol class=\"recipeSteps\"><li>", r"", text_to_process)
        text_to_process = re.sub(r"</li><li>", r"", text_to_process)
        text_to_process = re.sub(r"</li></ol>]", r"", text_to_process)
        text_to_process = re.sub(r"\[]", r"", text_to_process)
        text_to_process = re.sub(r"<i>", r"", text_to_process)
        text_to_process = re.sub(r"</i>", r"", text_to_process)
        text_to_process = re.sub(r"<br/>", r"", text_to_process)
        text_to_process = re.sub(r"<b>", r"", text_to_process)
        text_to_process = re.sub(r"</b>", r"", text_to_process)
        text_to_process = re.sub(r"(<strong>).*(</strong>)", r"", text_to_process)

        # removing https
        text_to_process = re.sub(r"(<b><a).*(\">)", r"", text_to_process)
        text_to_process = re.sub(r"<\/a><\/b>", r"", text_to_process)

        text_to_process = re.sub(r"(<a).*(\">)", r"", text_to_process)
        text_to_process = re.sub(r"<\/a>", r"", text_to_process)

        # expanding some key words - need them for the phoneme-grapheme correspondence
        text_to_process = re.sub(r"[°º˚°ºº][Cc]/", r" celsius or ", text_to_process)
        text_to_process = re.sub(r"[°º˚°ºº]F/", r" fahrenheit or ", text_to_process)

        text_to_process = re.sub(r"¼", r"one quarter", text_to_process)
        text_to_process = re.sub(r" 1cm/½", r" one and half centimetres", text_to_process)
        text_to_process = re.sub(r" 1cm", r" one centimetre", text_to_process)
        text_to_process = re.sub(r" 1mm", r" one millimetre", text_to_process)
        text_to_process = re.sub(r"([0-9])mm", r"\1 millimetres", text_to_process)
        text_to_process = re.sub(r"([0-9])cm", r"\1 centimetres", text_to_process)
        text_to_process = re.sub(r" x ([0-9])", r" by \1", text_to_process)
        text_to_process = re.sub(r"([0-9])ml", r"\1 millimetres", text_to_process)
        text_to_process = re.sub(r"([0-9])g", r"\1 grams", text_to_process)
        text_to_process = re.sub(r" ([0-9])\.5", r" \1 point five ", text_to_process)
        text_to_process = re.sub(r" ½cm", r" half a centimetre", text_to_process)
        text_to_process = re.sub(r" ½", r" half", text_to_process)

        text_to_process = re.sub(r"\n", r"", text_to_process)
        text_to_process = re.sub(r"\(", r". ", text_to_process)
        text_to_process = re.sub(r"\)", r". ", text_to_process)

        # lowercase everything
        text_to_process = text_to_process.lower()

        # creating a list of utterances
        list_sentences = text_to_process.split('.')

        # removing white spaces or empty strings
        list_sentences = [sentence for sentence in list_sentences if sentence != ' ' and sentence != '']

    return list_sentences

def main():
    list_sentences = pre_process("all_recipes.txt")
    pprint(list_sentences)
    pprint(type(list_sentences))
    pprint(len(list_sentences))

    file = open("pre-processed_recipes.txt", "w")
    for item in list_sentences:
        file.write("\n" + item)
    file.close()

    # exploring vocabulary
    def make_vocabulary(our_list_of_sentences):
        # making lists out of sentences

        our_tokenised_sentences = []
        for sentence in our_list_of_sentences:
            tokenised_sentence = sentence.split(" ")
            our_tokenised_sentences.append(tokenised_sentence)


        flat_list = [word for tokenised_sentence in our_tokenised_sentences for word in tokenised_sentence]

        return collections.Counter(flat_list)

    '''
    vocabulary_bag = make_vocabulary(list_sentences)
    pprint(vocabulary_bag)
    print(len(vocabulary_bag))
    '''

if __name__ == "main":
    main()