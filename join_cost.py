import re
import glob

recipes = ["a_1", "a_2", "a_3", "a_4", "a_5"]
harvard = ["b_1", "b_2", "b_3", "b_4", "b_5"]

def average_join_cost(directory, which_set):
    print("\nFor sentences from ", which_set, " of this voice: ", directory)
    list_join_cost = []
    average_cost_one_sentence = 0
    join_ratio_sent = 0
    for filename in which_set:
        for file in glob.glob(f"./{directory}/{filename}.txt"):
            with open(file, 'r') as f:
                utts_to_process = f.readlines()
                regex = re.compile(r'join_cost\s([0-9]+\.*[0-9]*)\s')
                for utt in utts_to_process:
                    for match in regex.finditer(utt):
                        join = float(match.group(1))
                        list_join_cost.append(join)

        actual_joins = [join for join in list_join_cost if join != 0]
        join_ratio_sent += len(actual_joins) / len(list_join_cost) # join ratio per sentence

        #print("Join ratio: ", len(actual_joins), "/", len(list_join_cost))

        # average join cost (join cost sum divided by number of joins per sentence)
        average_cost_one_sentence += sum(actual_joins)/len(list_join_cost)

    # averaging over the number of sentences
    average_cost = average_cost_one_sentence / len(which_set)
    print("Average join cost per sentence (normalised by number of joins): ", round(average_cost, 3))

    join_ratio = join_ratio_sent / len(which_set)
    print("Join ratio: ", round(join_ratio, 3), "\n")

# voice Little
average_join_cost(directory = "voices/txt_files/RL_sentences", which_set=recipes)
average_join_cost(directory = "voices/txt_files/RL_sentences", which_set=harvard)

# voice A
average_join_cost(directory = "voices/txt_files/A_sentences", which_set=recipes)
average_join_cost(directory = "voices/txt_files/A_sentences", which_set=harvard)

# voice R
average_join_cost(directory = "voices/txt_files/R_sentences", which_set=recipes)
average_join_cost(directory = "voices/txt_files/R_sentences", which_set=harvard)

# voice R random
average_join_cost(directory = "voices/txt_files/ARR_sentences", which_set=recipes)
average_join_cost(directory = "voices/txt_files/ARR_sentences", which_set=harvard)

# voice R greedy
average_join_cost(directory = "voices/txt_files/ARG_sentences", which_set=recipes)
average_join_cost(directory = "voices/txt_files/ARG_sentences", which_set=harvard)

# voice AR
average_join_cost(directory = "voices/txt_files/AR_sentences", which_set=recipes)
average_join_cost(directory = "voices/txt_files/AR_sentences", which_set=harvard)

# voice EDI
average_join_cost(directory = "voices/txt_files/W_EDI_sentences", which_set=recipes)
average_join_cost(directory = "voices/txt_files/W_EDI_sentences", which_set=harvard)

# voice GAM
average_join_cost(directory = "voices/txt_files/W_GAM_sentences", which_set=recipes)
average_join_cost(directory = "voices/txt_files/W_GAM_sentences", which_set=harvard)

