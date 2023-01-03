
import random
import os

def load_irregular_verbs(file_path):
    irregular_verbs = []
    with open(file_path, 'r') as file:
        for line in file:
            verb, present_s, past_s, past_participle = line.strip().split(', ')
            irregular_verbs.append({
                'verb': verb,
                'present_singular': present_s,
                'present_plural': 'are' if present_s == 'am' else present_s,
                'past_singular': past_s,
                'past_plural': 'were' if past_s == 'was' else past_s,
                'past_participle': past_participle
            })
    return irregular_verbs

def choose_random_verb(verbs_list):
    return random.choice(verbs_list)

def irregular_verbs_trainer(irregular_verbs):
    score = 0
    num_Frage = 5

    
    for _ in range(num_Frage):
        random_verb = choose_random_verb(irregular_verbs)

        verb = random_verb['verb']
        

        tense = random.choice(list(random_verb.keys()))
        correct_form = random_verb[tense]

        user_input = input(f"What is the {tense.replace('_',' ')} form of '{verb}'? ")

        if user_input == correct_form:
            print("Correct!")
            score +=1
        else:
            print(f"Wrong. The correct answer is '{correct_form}'.")

        
        print()

    print(f"Quiz abgeschlossen! Du hast {score}/{num_Frage} richtig! Gut gemacht!")

# Pfade zur Datei mit unregelm‰ﬂigen Verben
file_path = 'irregular_verbs.txt'  # Passe den Pfad entsprechend an

if os.path.exists(file_path):
    # Lade die unregelm‰ﬂigen Verben aus der Datei
    irregular_verbs = load_irregular_verbs(file_path)
    # Starte den Trainer
    irregular_verbs_trainer(irregular_verbs)
else:
    print(f"Irregular Verb File {file_path} nicht gefunden!")
    

