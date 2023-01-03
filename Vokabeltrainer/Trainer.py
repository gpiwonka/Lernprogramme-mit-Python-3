
#encoding: latin-1
import random

class Trainer:
    def __init__(self):
        self.vokabeln = {}
        self.fortschritt = {}

    def vokabel_hinzufuegen(self, begriff, bedeutung):
        self.vokabeln[begriff] = bedeutung
        self.fortschritt[begriff] = 0
    
    def vokabel_aendern(self,begriff_org,begriff,bedeutung):
        self.vokabeln[begriff] = bedeutung
        self.fortschritt[begriff] = 0
    
    def vokabel_loeschen(self,begriff):
        self.vokabeln.

    def vokabel_ueben(self):
        if not self.vokabeln:
            print("Der Vokabeltrainer enthält keine Vokabeln. Fügen Sie welche hinzu.")
            return

        begriff = random.choice(list(self.vokabeln.keys()))
        richtig = False

        print("Begriff:", begriff)
        antwort = input("Bedeutung: ")

        if antwort.lower() == self.vokabeln[begriff].lower():
            print("Richtig!\n")
            richtig = True
        else:
            print(f"Falsch! Die richtige Bedeutung ist: {self.vokabeln[begriff]}\n")

        # Fortschritt aktualisieren
        if richtig:
            self.fortschritt[begriff] += 1
        else:
            self.fortschritt[begriff] = 0

    def fortschritt_anzeigen(self):
        print("Fortschritt:")
        for begriff, fortschritt in self.fortschritt.items():
            print(f"{begriff}: {fortschritt} Mal richtig")
