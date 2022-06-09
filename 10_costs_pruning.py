# Author: Elisa Gambicchia (2021)
# This script computes the join and the target costs of joining diphones 

import re

def average_join_cost(filename):
    list_join_cost = []
    average_cost_one_sentence = 0
    with open(filename, 'r') as f:
        utts_to_process = f.readlines()
        regex = re.compile(r'join_cost\s([0-9]+\.*[0-9]*)\s')
        for utt in utts_to_process:
            for match in regex.finditer(utt):
                join = float(match.group(1))
                list_join_cost.append(join)

    actual_joins = [join for join in list_join_cost if join != 0]
    print("Join ratio: ", len(actual_joins), "/", len(list_join_cost))

    average_cost_one_sentence += sum(actual_joins) / len(list_join_cost)
    print("Average join cost (normalised by number of joins): ", round(average_cost_one_sentence, 3))

def average_target_cost(filename):
    list_target_cost = []
    average_cost_one_sentence = 0
    with open(filename, 'r') as f:
        utts_to_process = f.readlines()
        regex = re.compile(r'target_cost\s([0-9]+\.*[0-9]*)\s')
        for utt in utts_to_process:
            for match in regex.finditer(utt):
                join = float(match.group(1))
                list_target_cost.append(join)

    actual_joins = [join for join in list_target_cost if join != 0]
    print("Target cost ratio: ", len(actual_joins), "/", len(list_target_cost))

    average_cost_one_sentence += sum(actual_joins) / len(list_target_cost)
    print("Average target cost (normalised by number of joins): ", round(average_cost_one_sentence, 3))

def clear_format(filename):
    print("\nFor sentences from this setting: ", filename)
    average_join_cost(filename)
    average_target_cost(filename)

def main():
    # TARGET AND JOIN COSTS MANIPULATION
    # baseline
    clear_format(filename="./target_join_pruning/baseline.txt")

    # target
    clear_format(filename="./target_join_pruning/baseline_target0.txt")
    clear_format(filename="./target_join_pruning/baseline_target0_obprun0.txt")

    #Join cost: weighted sum of energy, F0 and MFCCs
    clear_format(filename="./target_join_pruning/baseline_f0_0.txt")
    clear_format(filename="./target_join_pruning/baseline_power_0.txt")
    clear_format(filename="./target_join_pruning/baseline_spectral_0.txt")

    # # OBSERVATION PRUNING
    # average_join_cost(filename="./target_join_pruning/baseline_pruning1.txt")
    # average_target_cost(filename="./target_join_pruning/baseline_pruning1.txt")

    # # VITERBI BEAM PRUNING
    # average_join_cost(filename="./target_join_pruning/baseline_beam_pruning1.txt")
    # average_target_cost(filename="./target_join_pruning/baseline_beam_pruning1.txt")

if __name__ == "__main__":
    main()