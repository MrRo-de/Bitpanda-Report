# Bitpanda-Report
A Python Script to analyze your Bitpanda *.csv History

Mit diesem Python-Skript lässt sich der Bitpanda *.csv-Verlauf analysieren und lesefreundlich in einer PDF-Datei darstellen.


# Hinweis

Es gibt nun auch eine Beispiel PDF und CSV Datei von Max Mustermann.
 

## Was wird Angezeigt?

Durch das Python-Script wird eine PDF-Datei mit dem Namen "BP-Report.pdf" mit folgendem Inhalt erstellt.

### Deckblatt

- Name und Anschrift
- gehandelte Assets
- Verteilung der jeweiligen Asset-Klassen

### Detailierte Transaktionen

- Sortiert nach Asset-Klasse
--  Fiat Transaktionen
--  Edelmetall Transaktionen
--  Cryptowährungen
--  Aktien
- Gewinn / Verlust des jeweiligen Assets (bei Verkauf)

### Steuer Details Haltefrist < 1 Jahr (Deutschland)

- Sortiert nach Asset-Klasse
- Anzeige des zu versteuernden Gewinn / Verlust

### Steuer Zusammenfassung

- Sortiert nach Jahren
- Berechnung des gesamt zu versteuernden Gewinn / Verlust

### Auflistung des aktuellen Portfolios

- Sortiert nach Asset-Klassen
-- Kaufdatum
-- Betrag
-- Asset Menge
-- Kaufpreis
-- Haltedauer
- Anzeige Asset Menge bei Haltefrist > 1 Jahr
- Anzeige der Gesamtmenge
- Anzeige des Durchschnittpreises

### Letzte Seite

- Infos



## Anleitung

### Wie erhalte ich die *csv Datei von Bitpanda

logged euch in euren Bitpanda- Account ein und klickt auf das "Bitpanda Symbol" in der rechten oberen Ecke.

Anschließend klickt ihr auf den "Verlauf" und nun nur noch auf "Exportieren".

Im erscheinenden Pop-Up Fenster klickt ihr nun auf CSV generieren, wartet kurz und klickt dann auf den Knopf mit
"bitpanda-trades-DATUM-UHRZEIT.csv"

Jetzt könnt Ihr das Pop-Up Fenster schließen und euch von eurem Bitpanda-Konto ausloggen.

### Installation und Benutzung

Sollte noch nicht geschehen müsst Ihr als erstes Python3 installieren.
Ihr findet es unter www.python.org -> Downloads -> Downlad Python 3.9.6 (aktuelle Version)

Das Script könnt Ihr unter https://github.com/MrRo-de/Bitpanda-Report downloaden, indem Ihr auf den grünen Knopf drückt und Download Zip auswählt.
Nach erfolgreichem Download müsst Ihr die ZIP Datei noch entpacken.

Nach erfolgreicher Installation und entpacken des Scripts öffnet Ihr die Eingabeaufforderung unter Windows, oder das Terminal unter MacOS.
Hier navigiert Ihr in den Bitpanda-Report-main Ordner und gebt ein:
```
pip3 install -r requirements.txt
```
*evtl ist ein Neustart eures Systems notwendig.

Nachdem der pip3 Befehl durchgelaufen ist, könnt Ihr das Script starten:
```
python Bitpanda-Report.py
```

Nach einer kurzen Ladezeit werdet Ihr aufgefordert den Pfad zur *.csv Datei einzufügen. 
Bei Drag&Drop ist es wichtig das alle Sonder- und Leerzeichen entfernt werden.

Anschließend wird nach eurem Namen und eurer Anschrift gefragt. Dies dient nur zur Personalisierung des Deckblattes.
Dies kann auch mit Enter/Return übersprungen werden.

Nach dem durchlaufen des Scripts erscheint nun die "Bitpanda-Report.pdf" Datei.


### Beim Ausführen des Scripts

Zuerst wird man aufgefordert den Pfad der *.csv Datei einzugeben.
Dies kann auch via Drag&Drop geschehen, hierbei ist darauf zu achten das vor und nach dem Pfad keine Zusätze wie "" oder '' vorhanden sind.
Diese entfernen, sonst gibt es eine Fehlermeldung.

Anschließend wird man gebeten Seinen Namen, Anschrift und die PLZ Ort anzugeben. Wenn dies nicht auf dem PDF erscheinen soll, die Felder einfach leer lassen und mit Return/Enter bestätigen.

Abwarten bis das Script durchgelaufen ist.

*Hinweis: Es werden beim Durchlaufen zusätzliche Daten, wie die Kreisdiagramme, erstellt. Diese werden nach dem Beenden des Scripts automatisch wieder gelöscht.



### Personalisieren des Codes

Damit nicht bei jedem Ausführen des Codes der Name und die Anschrift eingegeben werden muss, kann der Code angepasst werden.

Code-Zeile 75 bis 82 = Beispiel für die Abfrage und Manuelle Eingabe der Daten
```
full_name = input('Dein Namen:\n')
street = input('Straße, Hausnummer:\n')
postcode_city = input('PLZ und Ort:\n')
"""
full_name = ''
street = ''
postcode_city = ''
"""
```

Unteres Beispiel für die Nutzung der Hinterlegten Daten
```
"""
full_name = input('Dein Namen:\n')
street = input('Straße, Hausnummer:\n')
postcode_city = input('PLZ und Ort:\n')
"""
full_name = 'Max Mustermann'
street = 'Musterstraße 1'
postcode_city = '12345 Musterstadt'
```


Sollte eine *.csv Datei öfter verwendet werden. Zu Testzwecken oder was auch immer, sind die Code-Zeilen 53, 54 zu bearbeiten:
```
csv_path_to_file = ''
csv_filename = ''
```

Als Beispiel:
```
csv_path_to_file = 'Mein/Muster/Pfad'
csv_filename = 'bitpanda-trade-DATUM-UHRZEIT.csv'
```


