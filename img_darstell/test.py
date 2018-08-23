from icalendar import Calendar
from datetime import datetime
import time
import datetime

termin = []

class Termin:

    def __init__(self, strtdatum, enddatum, raum, name):
        self.name = name
        self.strtdatum = strtdatum
        self.enddatum = enddatum
        self.raum = raum

# sucht aus einem String den Namen des Profs raus. Dabei wird der Name der nach "Dozent:"" kommt. Also "Mustermann" bei "Dozent: Mustermann, Max ".
def namensSuche(satz):

    if not satz:
        raise ValueError("dein String ist leer")
    
    wortListe = satz.split(" ")
    name = ""

    for zl in range(len(wortListe)):
        try:
            if wortListe[zl].upper() == "DOZENT:":
                name = wortListe[zl+1].strip(",")
        except:
            print("Kein Dozent gefunden! der String scheint nach Dozent leer zu sein!")
    if (name == ("" or "Raum:")):
        print("Es wurde kein Name gefunden")

    return name

# sucht aus einem String den Raum raus in dem der Prof sich befinden soll. Dafür soll die Konvention mit Raum: genutzt werden wie bei namensSuche()
def raumSuche(satz):

    if not satz:
        raise ValueError("dein String ist leer")
    
    wortListe = satz.split(" ")
    raum = ""

    for zl in range(len(wortListe)):
        try:
            if(wortListe[zl].upper() == "RAUM:"):
                raum = wortListe[zl+1]
        except:
            print("Kein Raum gefunden checke den String, nach RAUM: kommt nichts !")
    if not raum:
        print("Kein Raum gefunden !!")
    
    return raum

def aktualisieren(pfad ="kalender/hskalender.ics"):
    datei = ""
    try:
        datei = open(pfad,"rb")
    except:
        print("Beim öffnen des Pfads ist etwas schiefgegangen, richtiger Pfad eingegeben ?")
    kalender = Calendar.from_ical(datei.read())
    for component in kalender.walk():
        if component.name == "VEVENT":
            beschreibung = component.get("description")
            name = namensSuche(beschreibung)
            raum = raumSuche(beschreibung)
            beginn = component.get("dtstart").dt
            ende = component.get("dtend").dt
            eintrag = Termin(beginn, ende, raum, name)
            termin.append(eintrag)

            
    if  datei:
        datei.close()
        print("fertig")

aktualisieren()
# for eintrag in termin:
#     print(eintrag.strtdatum)
termin = sorted(termin, key=lambda x: x.strtdatum)
for eintrag in termin:
    print(eintrag.strtdatum)



