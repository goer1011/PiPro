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
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from icalendar import Calendar
from datetime import datetime
import time
import datetime


def main():
    epd = epd2in7.EPD()
    epd.init()
    # Hier wird das Bild erzeugt
    bildZeichner('Zimmermann')
    # Stellt das Bild dar
    epd.display_frame(epd.get_frame_buffer(Image.open('IstDa.bmp')))

def bildZeichner(name = 'Müller', raum = 'ist nicht da'):
    #Image Size ( it is horizontal )
    EPD_WIDTH       = 176
    EPD_HEIGHT      = 264
    # Create a white mask 
    mask = Image.open("IstDa.bmp")  
    #Create a Draw object than allows to add elements (line, text, circle...) 
    draw = ImageDraw.Draw(mask) 
    #Create font and test it
    font = ImageFont.truetype('/home/pi/PiPro/img_darstell/font/VertigoPlusFLF-Bold.ttf', 25)
    draw.text((0,0), 'Prof. {} {} '.format(name, raum),font = font, fill = 0)
    #Save the picture on disk ( now create a new Image with vertikal orientation)
    neu = Image.new('1',(EPD_WIDTH, EPD_HEIGHT),255)
    #rotate the image in mask created 90 degree
    neu = mask.transpose(Image.ROTATE_90)
    neu.save('IstDa.bmp',"bmp")

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
    termin = sorted(termin, key=lambda x: x.strtdatum)
           
    if  datei:
        datei.close()
        print("fertig")

if __name__ == '__main__':
    main()
