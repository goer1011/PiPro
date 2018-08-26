##
 #  @filename   :   main.cpp
 #  @brief      :   2.7inch e-paper display demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     August 16 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##
import epd2in7
import epdif
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from icalendar import Calendar
from datetime import datetime,timezone, time, timedelta
import datetime





def main():
    prof = profLaden()
    termin = aktualisieren()
    print(len(termin), " Termine geladen")
    if(len(termin)==0):
        raise ValueError("Keine termine zum Laden")
    heute = heuteBestimmen(termin[0].strtdatum)
    testtermin = termin[0]
    if (testtermin.enddatum > heute):
        bildZeichner(name = prof.name,raum= prof.raum)

def profLaden(pfad = "config.txt",arg1="nachname",arg2="raumnummer"):
    datei = ""
    name = ""
    raum = ""
    try:
        datei = open(pfad,"r")
    except:
        print("datei konnte nicht gelesen werden")
    if datei:
        zeile = datei.readline()
        while(zeile):
            if zeile[0] != "#":
                print(zeile)
                zeile.split("=")
                if(zeile[0]==arg1):
                    try:
                        name = zeile[1]
                    except:
                        name = "unbenannt"
                elif(zeile[0]==arg2):
                    try:
                        raum = zeile[1]
                    except:
                        raum = "unbkt"
            zeile = datei.readline()
    prof = Prof(name,raum)
    return prof


def heuteBestimmen(datum):
    try:
        heute = datetime.datetime.now()
        print (heute - datum)
       
    except:
        heute = datetime.datetime.now(timezone.utc)
    return heute

def bildZeichner(name = 'Müller', anwesenheit = 'ist nicht da', raum ="", vorlage = "vorlagen/nachricht_vorlage.bmp",fontpfad = 'font/VertigoPlusFLF-Bold.ttf'):
     epd = epd2in7.EPD()
    epd.init()
    if raum:
        raum = "ist im Raum: {}".format(raum)
    # Lädt die vorlage (Hinweis : sie muss horizontal 264px breit und 176px hoch sein)
    mask = Image.open(vorlage)  
    #Erstellt ein Draw Objekt mit dem man dann aus mask rumschreiben kann. 
    schreib = ImageDraw.Draw(mask)
    größen = großBestimm('Prof. {}:'.format(name), fontpfad, schreib) 
    #Schrift wird ausgesucht inkl. schriftgröße
    font = ImageFont.truetype(fontpfad, größen[0])
    schreib.text((10,10), 'Prof. {}:'.format(name),font = font, fill = 0)
    font = ImageFont.truetype(fontpfad, 45)
    schreib.multiline_text((10,größen[1]), '{}!\n{}'.format(anwesenheit, raum ),font = font, fill = 0)
    # Erstellt ein neues Bild aber mit umgekehrten Größen
    neu = Image.new('1',(176, 264),255)
    # Die horizontale Maske wird nun um 90 Grad gedreht und auf das neue Bild geschrieben 
    neu = mask.transpose(Image.ROTATE_90)
    neu.save('nachricht.bmp',"bmp")
    # Stellt das Bild dar
     epd.display_frame(epd.get_frame_buffer(Image.open('nachricht.bmp')))
    

# gibt die Schriftgröße(x)/den Zeilenabstand(y) zurück der gewählt werden soll damit der Text lesbar ist.
def großBestimm(name, fontpfad ="font/VertigoPlusFLF-Bold.ttf", schreib = ImageDraw.Draw(Image.open("vorlagen/nachricht_vorlage.bmp"))):
    if not name:
        raise ValueError("leerer Name")

    schriftgröße =1
    font = ImageFont.truetype(fontpfad,schriftgröße)
    xy = schreib.textsize(name ,font = font)

    while ((xy[0]<= 185) and (xy[1]<=50)):
        schriftgröße = 1 + schriftgröße
        font = ImageFont.truetype(fontpfad,schriftgröße)
        xy = schreib.textsize(name ,font = font)

    ergebnis = [ schriftgröße, xy[1]+10 ]

    return ergebnis

class Prof:

    def __init__(self,name,raum):
        self.name = name
        self.raum = raum

class Termin:

    def __init__(self, strtdatum, enddatum, raum):
        # self.name = name
        self.strtdatum = strtdatum
        self.enddatum = enddatum
        self.raum = raum

# sucht aus einem String den Namen des Profs raus. Dabei wird der Name der nach "Dozent:"" kommt. Also "Mustermann" bei "Dozent: Mustermann, Max ".
# def namensSuche(satz):

#     if not satz:
#         raise ValueError("dein String ist leer")
    
#     wortListe = satz.split(" ")
#     name = ""

#     for zl in range(len(wortListe)):
#         try:
#             if wortListe[zl].upper() == "DOZENT:":
#                 name = wortListe[zl+1].strip(",")
#         except:
#             print("Kein Dozent gefunden! der String scheint nach Dozent leer zu sein!")
#     if (name == ("" or "Raum:")):
#         print("Es wurde kein Name gefunden")

#     return name

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
            try:
                kategorie = component.get("categories").upper()
            except:
                kategorie = "NORMAL"
            finally:
                if (kategorie==("NORMAL" or "AKTUELL")):
                    beschreibung = component.get("description")
                    # name = namensSuche(beschreibung)
                    raum = raumSuche(beschreibung)
                    beginn = component.get("dtstart").dt
                    ende = component.get("dtend").dt
                    eintrag = Termin(beginn, ende, raum)
                    heute = heuteBestimmen(eintrag.strtdatum) 
                    if(eintrag.enddatum > heute):
                        termin.append(eintrag)
    termin = sorted(termin, key=lambda x: x.strtdatum)
           
    if  datei:
        datei.close()

    return termin

if __name__ == '__main__':
    main()
