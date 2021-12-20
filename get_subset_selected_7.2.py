import re
# CHECKING HOW MANY SENTENCES ARE THE SAME IN BOTH SCRIPTS

def find_numbers(file):
    with open(file, 'r') as f:
        utts_to_process = f.read()
        utts = utts_to_process.splitlines()
        pattern = r'a[0-9]+'
        numbers = [re.findall(pattern, utt) for utt in utts]
    return numbers

list_random = find_numbers("artic_random_utts_200.txt")
print(list_random)

list_greedy = find_numbers("artic_selected_utts.txt")
print(list_greedy)

common = [utt for utt in list_greedy if utt in list_random]
print(common)
print(len(common))
