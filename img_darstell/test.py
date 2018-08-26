from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from icalendar import Calendar
from datetime import datetime
import time
import datetime



def main():
    termin = aktualisieren()
    heute = datetime.datetime.now
    print (heute)

    bildZeichner('O',raum="202")
    # Stellt das Bild dar
    # epd.display_frame(epd.get_frame_buffer(Image.open('nachricht.bmp')))

def bildZeichner(name = 'Müller', anwesenheit = 'ist nicht da', raum ="", vorlage = "vorlagen/nachricht_vorlage.bmp",fontpfad = 'font/VertigoPlusFLF-Bold.ttf'):
    # epd = epd2in7.EPD()
    # epd.init()
    if raum:
        raum = "ist im Raum: {}".format(raum)
    # Lädt die vorlage (Hinweis : sie muss horizontal 264px breit und 176px hoch sein)
    mask = Image.open(vorlage)  
    #Erstellt ein Draw Objekt mit dem man dann aus mask rumschreiben kann. 
    schreib = ImageDraw.Draw(mask)
    größen = großBestimm('Prof. {}:'.format(name), fontpfad, schreib) 
    #Schrift wird ausgesucht inkl. schriftgröße
    font = ImageFont.truetype(fontpfad, größen[0])
    schreib.text((2,10), 'Prof. {}:'.format(name),font = font, fill = 0)
    font = ImageFont.truetype(fontpfad, 45)
    schreib.multiline_text((2,größen[1]), '{}!\n{}'.format(anwesenheit, raum ),font = font, fill = 0)
    #Save the picture on disk ( now create a new Image with vertikal orientation)
    neu = Image.new('1',(176, 264),255)
    #rotate the image in mask created 90 degree
    neu = mask.transpose(Image.ROTATE_90)
    neu.save('nachricht.bmp',"bmp")
    neu.show()

# gibt die Schriftgröße(x)/den Zeilenabstand(y) zurück der gewählt werden soll damit der Text lesbar ist.
def großBestimm(name, fontpfad ="font/VertigoPlusFLF-Bold.ttf", schreib = ImageDraw.Draw(Image.open("vorlagen/nachricht_vorlage.bmp"))):
    if not name:
        raise ValueError("leerer Name")

    schriftgröße =1
    font = ImageFont.truetype(fontpfad,schriftgröße)
    xy = schreib.textsize(name ,font = font)

    while ((xy[0]<= 195) and (xy[1]<=50)):
        schriftgröße = 1 + schriftgröße
        font = ImageFont.truetype(fontpfad,schriftgröße)
        xy = schreib.textsize(name ,font = font)

    ergebnis = [ schriftgröße, xy[1]+10 ]

    return ergebnis
   

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
    termin = []
    for component in kalender.walk():
        if component.name == "VEVENT":
            if (component.get("categories").upper()==("NORMAL" or "AKTUELL" or "")):
                beschreibung = component.get("description")
                name = namensSuche(beschreibung)
                print(name)
                raum = raumSuche(beschreibung)
                beginn = component.get("dtstart").dt
                ende = component.get("dtend").dt
                eintrag = Termin(beginn, ende, raum, name)
                termin.append(eintrag)
    termin = sorted(termin, key=lambda x: x.strtdatum)
           
    if  datei:
        datei.close()

    return termin

if __name__ == '__main__':
    main()