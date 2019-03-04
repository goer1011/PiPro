# PiPro

## Was ist das?

Es ist ein Projekt, mit der man mithilfe eines Raspberry Pi einen E-Paper Display ansteuern kann. Das E-Paper Display zeigt an ob ein Professor gerade da ist oder nicht. Man kann das dann an der Wand montieren und somit können die Studierenden sehen ob der Professor da ist oder nicht. Dieser soll für jeden Professor an der Hochschule funktionieren. Das wird dadurch geschafft, dass der Professor seinen Stundenplan in den Ordner reinlädt und das Programm selbst liest den Stundenplan aus. Das funktioniert mit den Stundenplänen der Professoren an der Hochschule, da ich diesen auf den angepasst habe.

## Was brauche ich dafür?
1. Raspberry Pi (ich hatte einen Zero)

2.	MicroSD Karte und etwas zum auslesen und beschreiben ( manche Laptops können MicroSD Karten lesen, dann braucht man nur einen MicroSD Karten Adapter)

3.	Raspbian von www.Raspberrypi.org runterladen.

4.	Win32 Disk Imager runterladen.

## Wie gehe ich vor ?

1.	SD Karte formatieren

2.	Win32DiskImager öffnen

3.	Image Datei ist die Datei aus punkt 4 und Datenträger ist die SD Karte
9.	Auf „schreiben“ Klicken und warten
10.	Danach kommt eine Benachrichtigung, dass hoffentlich alles geklappt hat, dann kann man nämlich die SD- Karte ins Rasppi einlegen.
11.	Entfernen Sie die SDKarte kurz aus dem Reader und stecken Sie sie wieder rein.
12.	 Windows erkennt die Fat32-Partition „boot“. Im Hauptverzeichnis legen Sie zunächst eine leere Datei namens „ssh“ an.( Achten Sie darauf, dass die Datei keine Dateinamenerweiterung wie .txt verpasst bekommt).
13.	Öffnen Sie die Datei cmd line.txt und ergänzen nach „rootwait“ und vor „quiet“ den folgenden Befehl:
modules-load=dwc2,g_ether 
Beachten Sie, dass vor und nach dem Befehl ein Leerzeichen stehen muss. Danach öffnen Sie die Datei config.txt und ergänzen ganz unten die folgende Zeile:
dtoverlay=dwc2 
14.	    "Nachdem Sie beide Dateien geändert haben, stecken Sie die Speicherkarte in den Raspi. Jetzt kommt das Micro-USB-Kabel ins Spiel: Verbinden Sie es einerseits mit dem PC und andererseits mit dem durch „USB“ gekennzeichneten Micro-USB-Anschluss des Raspi.

        Windows 10 
        Unter Windows 10 wird der Raspi nicht als
        Ethernet-Gadget, sondern als COMSchnittstelle erkannt. Eine manuelle Auswahl des korrekten NDIS-Treibers ist nicht  möglich, da Windows im entsprechenden Dialog lediglich Treiber für COM-Schnittstellen präsentiert. Unter ct.de/y7j9 finden Sie jedoch einen modifizierten Treiber, den Sie problemlos nutzen können. Entpacken Sie das Zip-Archiv in einem beliebigen Ordner. Öffnen Sie nun den Geräte-Manager und klicken Sie mit der rechten Maustaste auf „Serielles USB-Gerät“, das sich unter „Anschlüsse (COM & LPT)“ verbirgt. Wählen Sie „Treibersoftware aktualisieren / Auf dem Computer nach Treibersoftware suchen / Aus einer Liste von Gerätetreibern auf dem Computer auswählen“ und „Datenträger“. Im folgenden Dialog wählen Sie die Datei „RNDIS.inf“ aus dem entpackten Treiberarchiv. Nach einem Klick auf „Weiter“ wird der Raspi schließlich als „USB Ethernet/RNDIS Gadget“ identifiziert."

### Freiwillig 
---
10.	Visual Studio den Plug in für Python installiert

16.	Python selbst installiert
### nicht mehr Freiwillig 
---
12.	Passwort geändert auf _Piebacken3mal_ durch: passwd 
18.	sudo raspi-config damit auf den „Bios- Zugegriffen“ 
a.	System mit meinem Rooter verbunden
b.	Update durchgeführt. ( sudo apt-get update)
c.	Upgrade durchgefürt. (sudo apt-get upgrade)
Einrichten vom Zertifikat
1.	erstellen Sie eine Kopie der Konfigurationsdatei /etc/ssh/sshd_config und setzen einen Schreibschutz. Geben Sie die Befehle nacheinander in die Befehlszeile ein.
a.	sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.original
b.	sudo chmod a-w /etc/ssh/sshd_config.original

2.	damit man datei bearbeiten kann :
sudo nano /etc/ssh/sshd_config
3.	aus #PubkeyAuthentication yes  entfernen wir das #
4.	RSAAuthentication yes
5.	Banner none -> Banner /etc/issue.net
6.	Restart durch sudo systemctl restart sshd.service oder sudo systemctl restart ssh.service
7.	Public key generiert durch PuTTyGen:

a.  SSH-2 RSA

b.	Passphrase ist _Himbeerkuchen_

c.	Private Key speichern

d.	Verzeichnis erstellen
    
    sudo nano /home/pi/.ssh/authorized_keys

e.	Public key drin einspeichern indem man im Putty Key generator im fenster den Public key kopiert ( Beachte, dass es ein einzeiler sein muss)

	
## Python installieren

### Python 3.6 
```bash
wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz

tar xzvf Python-3.6.0.tgz

cd Python-3.6.0/

./configure

Make

Sudo make install
```
### Python libs updaten zu 3.6

```bash
sudo apt-get python3-dev python3-pip

sudo apt-get -y install python3-rpi.gpio

sudo apt-get python3-dev

wget https://github.com/doceme/py-spidev/archive/master.zip

unzip master.zip

cd py-spidev-master/

sudo python3 setup.py install

```
## Probleme die auftreten können
### 1.
da pip install … wiringpi nicht klappte bin ich dieser anleitung gefolgt : http://wiringpi.com/download-and-install/

### 2.
wegen Probleme mit SSL habe ich diese Anleitung befolgt um OpenSSL zu installieren
https://techglimpse.com/install-python-openssl-support-tutorial/ (Aktuelle Version von python am besten nehmen. Dauert dennoch sehr lange.)

---
```bash
sudo apt-get install libjpeg-dev

sudo apt-get install libfreetype6-dev
```
Neu installieren von Pillow (PIL)5.2.0
```bash
sudo pip install spidev
```

Enable the I2C function
```bash
sudo raspi-config
sudo nano /etc/modules
```

Add the following two lines to the configuration file

```bash
       i2c-bcm2708
        i2c-dev 
```

Enable the serial function

```bash
sudo raspi-config
```

Start up the spi function

```bash
sudo raspi-config

Wget https://www.waveshare.com/w/upload/f/f5/2.7inch-e-paper-hat-code.7z
```

7zip runterlade und datei entzippen

```bash
sudo apt-get install p7zip-full
7z x 2.7inch-e-paper-hat-code.7z.7z
Fonts runterladen und installieren
Sudo python main.py
```
    https://diyprojects.io/test-waveshare-epaper-eink-2-7-spi-screen-raspberry-pi-python/ (Anleitung für  Waveshare display)

    https://www.jeffgeerling.com/blogs/jeff-geerling/raspberry-pi-zero-conserve-energy
(Anleitung um Hdmi und Led ausschalten
33.	Git installieren und zum laufen bringen

### RTC Installieren
1.	DS3231 einstecken

    a.	Raspi ausschalten
    
    b.	Dazu nachgucken welche pins benutzt werden, benutzt werden die pins mit 3,3V Input 3x GPIO und 1 GND also die Pins 1,3,5,7,9

    c.	Raspi anschalten

    	Sudo i2cdetect -y 1
    ->	Es müsste nun viele -- und 68 dargestellt werden
2.	    Sudo nano /boot/config.txt
    a.	Am Ende des Textes einfügen
                
        dtparam=i2c_arm=on

        dtoverlay=i2c-rtc,ds3231
3.	    Sudo nano /etc/modules
        
    ```           
    i2c-dev 
    rtc-ds3231
    ```
    Am ende wieder einfügen

4.	Entfernen von fake-hwclock
```bash
Sudo apt-get -y remove fake-hwclock
Sudo update-rc.d -f fake-hwclock remove
Sudo nano /lib/udev/hwclock-set
```
    If [-e /run/systemd .. 
	Exit 0 
    Fi 

auskommentieren

5.    Reboot den pi

6.      Test mit 
    
        sudo hwclock -r. 

Jetzt müsste was angezeigt werden

7.	    Sudo hwclock -w

8.	https://github.com/bablokb/pi-wake-on-rtc 

Einrichten einer Bluetooth- Verbindung:
1.	    Sudo bluetoothctl
2.	    Agent on
3.	    Default-agent
4.	    Discoverable on
5.	    Scan on
6.	    Pair xx:xx:xx:…
7.	    Trust xx:xx:xx…
