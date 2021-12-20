from jiwer import wer

recipe = ["mix the beaten egg with the milk and a little bit of limoncello in a shallow dish",
                       "preheat the oven at 180 celsius while you finely slice your porcini lengthways",
                       "roughly tear up the radicchio and mix the peppers",
                       "spoon half the ragù over the tray of potatoes",
                       "add some cannellini beans to your salad"]

general = ["the girl at the booth sold 50 bonds",
                        "the source of the huge river is the clear spring",
                        "the salt breeze came across from the sea",
                        "help the woman get back to her feet a pot of tea helps to pass the evening",
                        "smoky fires lack flame and heat the soft cushion broke the man's fall"]

def calculate_wer(file, type):
    with open(file, 'r') as f:
        utts_to_process = f.read()
        utts = utts_to_process.split("\n")

        error = round(wer(type, utts),3)
        print(file, error)

calculate_wer(file='./voices/transcriptions/R200_recipes.txt', type=recipe)
calculate_wer(file='./voices/transcriptions/R200_general.txt', type=general)
print()
calculate_wer(file='./voices/transcriptions/R_recipes.txt', type=recipe)
calculate_wer(file='./voices/transcriptions/R_general.txt', type=general)
print()
calculate_wer(file='./voices/transcriptions/A_recipes.txt', type=recipe)
calculate_wer(file='./voices/transcriptions/A_general.txt', type=general)
print()
calculate_wer(file='./voices/transcriptions/ARR_recipes.txt', type=recipe)
calculate_wer(file='./voices/transcriptions/ARR_general.txt', type=general)
print()
calculate_wer(file='./voices/transcriptions/ARG_recipes.txt', type=recipe)
calculate_wer(file='./voices/transcriptions/ARG_general.txt', type=general)
print()
calculate_wer(file='./voices/transcriptions/AR_recipes.txt', type=recipe)
calculate_wer(file='./voices/transcriptions/AR_general.txt', type=general)
print()
calculate_wer(file='./voices/transcriptions/refe_recipes.txt', type=recipe)
calculate_wer(file='./voices/transcriptions/refe_general.txt', type=general)
