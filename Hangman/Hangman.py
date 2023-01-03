#encoding: latin-1
import random
import requests

def waehleWort():
    api_url = "https://random-word-api.herokuapp.com/word?lang=de"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Wirft eine Exception, wenn die Anfrage nicht erfolgreich war (z.B., wenn Statuscode nicht 200 ist)

        # Die Antwort des API ist ein JSON, wir extrahieren das Wort aus dem JSON
        word = response.json()[0]

        return word
    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der API-Anfrage: {e}")
        return None
    
def hangman():
    wort = waehleWort()
    geratene_buchstaben = set()
    max_fehler = 6
    fehler = 0
    wort_geloest = False

    print("Willkommen beim Hangman-Spiel!")
    print("_ " * len(wort))

    while not wort_geloest and fehler < max_fehler:
        geraten = input("Rate einen Buchstaben: ").lower()

        if len(geraten) == 1 and geraten.isalpha():
            if geraten in geratene_buchstaben:
                print("Du hast diesen Buchstaben bereits geraten. Versuche es erneut.")
            elif geraten in wort:
                geratene_buchstaben.add(geraten)
            else:
                fehler += 1
                print(f"Falsch! Du hast {fehler} von {max_fehler} Fehlern gemacht.")
        else:
            print("Ungültige Eingabe. Gib einen einzelnen Buchstaben ein.")

        aktueller_stand = ""
        for buchstabe in wort:
            if buchstabe in geratene_buchstaben:
                aktueller_stand += buchstabe + " "
            else:
                aktueller_stand += "_ "

        print(aktueller_stand)

        if "_" not in aktueller_stand:
            wort_geloest = True
            print("Glückwunsch! Du hast das Wort richtig geraten.")
        elif fehler == max_fehler:
            print(f"Leider verloren! Das richtige Wort war '{wort}'.")

if __name__ == "__main__":
    hangman()
