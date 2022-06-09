# Author: Elisa Gambicchia (2021)
# This script checks for average missing diphones

import re
import glob

recipes = ["a_1", "a_2", "a_3", "a_4", "a_5"]
harvard = ["b_1", "b_2", "b_3", "b_4", "b_5"]

def average_missing_diphones(directory, which_set):
    print("\nFor sentences from ", which_set, " of this voice: ", directory)

    missing_diphones = 0
    silence = 0
    for filename in which_set:
        for file in glob.glob(f"./voices/txt_files/{directory}/{filename}.txt"):
            with open(file, 'r') as f:
                utts_to_process = f.readlines()
                regex = "missing_diphone"
                regex2 = "#_#"
                for utt in utts_to_process:
                    if re.search(regex, utt):
                        missing_diphones += 1
                    if re.search(regex2, utt):
                        silence += 1


    print("Missing diphones: ", missing_diphones)
    print("Silence inserted: ", silence)

def main():

    # voice RL
    average_missing_diphones(directory = "RL_sentences", which_set=recipes)
    average_missing_diphones(directory = "RL_sentences", which_set=harvard)

    # voice A
    average_missing_diphones(directory = "A_sentences", which_set=recipes)
    average_missing_diphones(directory = "A_sentences", which_set=harvard)

    # voice R
    average_missing_diphones(directory = "R_sentences", which_set=recipes)
    average_missing_diphones(directory = "R_sentences", which_set=harvard)

    # voice R random
    average_missing_diphones(directory = "ARR_sentences", which_set=recipes)
    average_missing_diphones(directory = "ARR_sentences", which_set=harvard)

    # voice R greedy
    average_missing_diphones(directory = "ARG_sentences", which_set=recipes)
    average_missing_diphones(directory = "ARG_sentences", which_set=harvard)

    # voice AR
    average_missing_diphones(directory = "AR_sentences", which_set=recipes)
    average_missing_diphones(directory = "AR_sentences", which_set=harvard)

    # voice EDINBURGH
    average_missing_diphones(directory = "W_EDI_sentences", which_set=recipes)
    average_missing_diphones(directory = "W_EDI_sentences", which_set=harvard)

    # voice GAM
    average_missing_diphones(directory = "W_GAM_sentences", which_set=recipes)
    average_missing_diphones(directory = "W_GAM_sentences", which_set=harvard)

if __name__ == "__main__":
    main()