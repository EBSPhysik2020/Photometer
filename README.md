# Photometer

## Verwendung des Photometers
* [Kurzanleitung zur Inbetriebnahme und Verwendung des Photometers](Dokumentation/Kurzanleitung.pdf)
* [Ausführliches Handbuch](Dokumentation/Handbuch.pdf)
* [Projekt-Portfolio](Dokumentation/Portfolio.pdf)

## Referenzen
### Photometer
* Poster: https://www.haw-hamburg.de/fileadmin/user_upload/FakLS/08LABORE/BPA/Poster_Photometer_BPDs_2019.pdf
* Anleitung der HAW: https://www.haw-hamburg.de/fileadmin/user_upload/FakLS/08LABORE/BPA/WIFI_Photometer_20171116.pdf
### RaspberryPI / Hardware
* SD-Karte clonen (MacOS): https://computers.tutsplus.com/articles/how-to-clone-raspberry-pi-sd-cards-using-the-command-line-in-os-x--mac-59911
* Wifi-Access-Point: https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md
* Datenblatt mehrfarbige LED: http://funduino.de/DL/RGB.pdf
* Datenblatt Lichtsensor: https://cdn-learn.adafruit.com/downloads/pdf/tsl2561.pdf
* Datenblatt Lichtsensor: https://cdn-shop.adafruit.com/datasheets/TSL2561.pdf
* Wechsel zwischen LCD und HDMI: https://github.com/goodtft/LCD-show
## Hinweise zum Nachbauen
**Es sollte so oft wie möglich ein Backup des System gemacht werden.**
### Verwendung der Hardware
* Lichtsensor: Um den Lichtsensor betreiben zu könnnen, muss die Adafruit TSL2561 Bibliothek auf dem RaspberryPI installiert werden (`sudo pip3 install adafruit-circuitpython-tsl2561`). Damit die Bibliothek den Sensor ansteuern kann, muss zusätzlich I2C aktiviert werden.
* LCD-Display: Damit das Bild auf dem LCD-Display statt dem HDMI-Output ausgegeben wird, muss ein entsprechendes Programm ausgeführt werden (s. Referenzen). Dieser Schritt war eine häufige Ursache für Systemabstürze.
* LED: Ein möglicher Schaltplan für die LED befindet sich in diesem Ordner: [Schaltplan LED](LED)
### Verwendung der Software
* Um die Bedienung des Photometers möglichst einfach zu gestalten, sollten die Software nach dem Booten automatisch gestartet werden. Dazu wird sie in die Datei *~/.profile* eingetragen. Außerdem wird in dieser Datei die Umgebungsvariable *DISPLAY* gesetzt.
* Um Software auf den RaspberryPI zu überspielen und einzurichten, sollte SSH verwendet werden. Dadurch spart man sich das Umschalten zwischen dem LCD-Display, auf dem nicht immer optimal gearbeitet werden kann, und dem HDMI-Output.
### Verwendung eines 3D-gedruckten Gehäuses
In dem Ordner [Gehäuse](Gehäuse) befindet sich ein Modell für ein Gehäuse, welches mit einem 3D-Drucker gedruckt werden kann.
## Entwickler
* Sören Seidel
* Tom Schimansky
* Frederik Mrozek
* Niklas Riepen
