from random import *

gesamt = 0
richtige = 0
while True:
    rechenart = randint(1,4)
    rechenArtZeichen = ""
    a = randint(1,100)
    b = randint(1,100)
    if rechenart == 1:
        richtigesErgebnis = a+b
        rechenArtZeichen = "+"
    if rechenart == 2:
        richtigesErgebnis = a*b
        rechenArtZeichen = "*"
    if rechenart ==3:
        if a < b:
            temp = b
            b = a
            a=temp
        richtigesErgebnis = a-b
        rechenArtZeichen = "-"
    if rechenart ==4:
        if a < b:
            temp = b
            b = a
            a=temp
        m = a%b 
        if m > 0:
            a = a-m
        richtigesErgebnis = a/b
        rechenArtZeichen = "/"        
    eingabe = input("(e für Ende) " + str(a)+" "+rechenArtZeichen+" "+ str(b) + " = ") #Hier warten wir auf die Eingabe des Benutzers
    if eingabe == 'e':
        break
    gesamt = gesamt +1
    ergebnis = int(eingabe)
    if richtigesErgebnis == ergebnis:
        print("richtig!!!")
        richtige = richtige +1
    else:
        print("falsch!!! richtig wäre: "+str(richtigesErgebnis)) 
print ("Du hast "+str(gesamt)+" Fragen beantwortet! Davon waren "+str(richtige)+"!")