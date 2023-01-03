# encoding: latin-1

from asyncio.windows_events import NULL
import random
import csv
import PySimpleGUI as sg



def PeriodensystemEinlesen():

    # Dateiname der CSV-Datei
    csv_datei = 'PeriodicTableofElements.csv'  

    # Liste zum Speichern der Daten
    daten = []

    # Öffne die CSV-Datei und lies sie ein
    with open(csv_datei, 'r', newline='',encoding='latin-1') as datei:
        csv_reader = csv.DictReader(datei)
    
        for zeile in csv_reader:
            daten.append(zeile)

    return daten

def findeElementAnPos(elemente,zeile,spalte):
    for row in elemente:
        if int(row['Display Row']) == zeile and int(row['Display Column']) == spalte:
            return row
    return NULL

def findeElement(elemente,symbol):
    for row in elemente:
        if row['Symbol'] == symbol:
            return row
    return NULL
    
def infosAnzeigen(element):
    
    elementlayout = []
    for item in element:
        elementlayout.append([sg.Text(item, size=(30, 1)),sg.Text(element[item])])
       
    layout=[[sg.Column(elementlayout,scrollable=True,expand_x=True,expand_y=True)], [sg.Button('Ok')]]

    window = sg.Window('Element Info', layout,resizable=True, grab_anywhere=False, size=(800, 480), return_keyboard_events=True, finalize=True)
    window.BringToFront()
    while True:
        event, values = window.read()
        if event in (None, 'Ok'):
            break
        
SPIELBUTTON="--spiel--"
SPIELBUTTON_TEXT_STARTEN = "Spiel starten"
SPIELBUTTON_TEXT_STOPPEN = "Spiel beenden"

FRAGE = "--frage--"

AktuelleFrage = NULL


ps_elemente = PeriodensystemEinlesen();

layout =  [[NULL for _ in range(18)] for _ in range(9)]

for row in range(9):
    for col in range(18):
        element = findeElementAnPos(ps_elemente,row+1,col+1)
        if element != NULL:
      
           layout[row][col] = sg.Button(element['Symbol'], size=(4, 2))
        else:
            layout[row][col] = sg.Push(background_color='gray')


layout.insert(0, [sg.Radio('Info', "Modus", default=True,enable_events=True, size=(10,1), k='-Info-'), sg.Radio('Spiel', "Modus", default=False,enable_events=True, size=(10,1), k='-Spiel-')])
layout.insert(0,[sg.Button(SPIELBUTTON_TEXT_STARTEN,key=SPIELBUTTON,visible=False), sg.Text('', key=FRAGE,visible=False, font='_ 16')])
layout.insert(0,[sg.Text('Periodensystem', font='_ 20')])

sg.theme('DarkAmber') 
Spielen = False
Richtig = 0
Gesamt = 0
window = sg.Window("Periodensystem", layout,background_color='gray')
i=0
while True:
    event,value = window.read()
    if event == "close":
        break
    if event == sg.WINDOW_CLOSED:
        break
    if event == "-Spiel-":
        
        window[SPIELBUTTON].update(visible=True)
        window[SPIELBUTTON].update(SPIELBUTTON_TEXT_STARTEN)
        window[FRAGE].update(visible=True)
    if event == "-Info-":
        window[SPIELBUTTON].update(visible=False)
        window[FRAGE].update(visible=False)
    if event == SPIELBUTTON:
        Spielen = not Spielen
        if (Spielen == True):
            window[FRAGE].update(visible=True)
            AktuelleFrage = random.choice(ps_elemente)
            window[SPIELBUTTON].update(SPIELBUTTON_TEXT_STOPPEN)
            window[FRAGE].update(f"Welches Atom hat die Ordnungszahl {AktuelleFrage['Atomic Number']} ?")   
        else:
            prozent = Richtig / Gesamt * 100
            SpielerText = "Weiter so Du wirst immer besser!"
            if prozent > 30:
                SpielerText = "Sehr gut!"
            if prozent > 50:
                SpielerText = "Wunderbar! Du bist am bestem Weg zum Experten!"
            if prozent > 70:
                SpielerText = "Viel fehlt nicht mehr und Du bist Experte!"
            if prozent > 80:
                SpielerText = "Du bist Experte!"    

            sg.popup("Ergebnis",f"{SpielerText}\nDu hast {Gesamt} Fragen beantwortet davon {Richtig} Richtig!")
            window[SPIELBUTTON].update(SPIELBUTTON_TEXT_STARTEN)
            window[FRAGE].update(visible=False)
            Gesamt =0
            Richtig = 0
            
    element = findeElement(ps_elemente,event)
    if element != NULL:
        if Spielen == True:
            Gesamt = Gesamt +1;
            if (element['Symbol'] == AktuelleFrage['Symbol']):
                sg.popup("Richtig!!")
                Richtig = Richtig+1
            else:
                sg.popup("Falsch",f"Leider falsch!!\nDie richtige Antwort ist {AktuelleFrage['Symbol']} - {AktuelleFrage['Element']}\nDu hast {element['Symbol']} mit der Ordnungszahl {element['Atomic Number']} ausgewähl! ")
            AktuelleFrage = random.choice(ps_elemente)
            window[FRAGE].update(f"Welches Atom hat die Ordnungszahl {AktuelleFrage['Atomic Number']} ?")        
        else:
            infosAnzeigen(element)
       
    
window.close()