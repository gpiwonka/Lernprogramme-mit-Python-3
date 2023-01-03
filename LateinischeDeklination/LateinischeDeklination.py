import random

# Funktion zum Laden der Deklinationen aus der externen Datei
def lade_deklinationen_aus_datei(dateipfad):
    deklinationen = {}
    with open(dateipfad, "r", encoding="utf-8") as datei:
        for zeile in datei:
            teile = zeile.strip().split()
            if len(teile) == 5:
                nominativ, genitiv, dativ, akkusativ, ablativ = teile
                deklinationen[nominativ] = {
                    "genitiv": genitiv,
                    "dativ": dativ,
                    "akkusativ": akkusativ,
                    "ablativ": ablativ
                }
    return deklinationen

# Lateinische Substantive und ihre Deklinationen
deklinationen = lade_deklinationen_aus_datei("deklinationen.txt")

def lateinische_deklination_ueben():
    # Wähle ein zufälliges Substantiv
    substantiv = random.choice(list(deklinationen.keys()))

    # Hole die korrekten Deklinationen für das Substantiv
    korrekte_deklinationen = deklinationen[substantiv]

    # Zeige das ausgewählte Substantiv an und fordere die Eingabe der Deklinationen
    print(f"Deklination von: {substantiv}")
    antworten = {}
    for fall in ["genitiv", "dativ", "akkusativ", "ablativ"]:
        antworten[fall] = input(f"Gib die {fall} Form ein: ")

    # Überprüfe die eingegebenen Deklinationen
    richtig = True
    for fall, antwort in antworten.items():
        if antwort != korrekte_deklinationen[fall]:
            richtig = False
            print(f"Falsch! Die richtige {fall} Form ist: {korrekte_deklinationen[fall]}")

    if richtig:
        print("Richtig! Gut gemacht!")

if __name__ == "__main__":
    while True:
        lateinische_deklination_ueben()
        weitermachen = input("Willst du noch eine? (Ja/Nein): ").lower()
        if weitermachen != "ja":
            break
