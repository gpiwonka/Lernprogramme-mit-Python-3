import PySimpleGUI as sg
from Datenbank import VokabeltrainerDB
import random

class VokabeltrainerGUI:

    def __init__(self):
        self.trainer_db = VokabeltrainerDB()
        self.current_begriff = None

        # Layout definieren
        layout = [
            [sg.Text("Vokabeltrainer")],
            [sg.Text("Begriff:"), sg.Text("", size=(20, 1), key="-Begriff-")],
            [sg.Text("Bedeutung:"), sg.InputText(key="-Antwort-")],
            [sg.Button("�ben"), sg.Button("Fortschritt anzeigen"), sg.Menu([['Hinzuf�gen', ['Neue Vokabel']]])]
        ]

        # Fenster erstellen
        self.window = sg.Window("Vokabeltrainer", layout, resizable=True, finalize=True)



