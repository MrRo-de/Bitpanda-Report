# Bitpanda-Report
A Python Script to analyze your Bitpanda *.csv History

Mit diesem Python-Skript lässt sich der Bitpanda *.csv-Verlauf analysieren und lesefreundlich darstellen.



## Was wird Angezeigt?

Durch das Python-Script wird eine PDF-Datei mit dem Namen "BP-Report.pdf" mit folgendem Inhalt erstellt.

#### Deckblatt

- Name und Anschrift
- gehandelte Assets
- Verteilung der jeweiligen Asset-Klassen


## Anleitung

### Wie erhalte ich die *csv Datei von Bitpanda

logged euch in euren Bitpanda- Account ein und klickt auf das "Bitpanda Symbol" in der rechten oberen Ecke.

Anschließend klickt ihr auf den "Verlauf" und nun nur noch auf "Exportieren".

Im erscheinenden Pop-Up Fenster klickt ihr nun auf CSV generieren, wartet kurz und klickt dann auf den Knopf mit
"bitpanda-trades-DATUM-UHRZEIT.csv"

Jetzt könnt Ihr das Pop-Up Fenster schließen und euch von eurem Bitpanda-Konto ausloggen.



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


<img src="https://user-images.githubusercontent.com/66023319/114274881-b1599080-9a20-11eb-9d5d-3d652f71b881.png" height="200">

Hier als Beispiel mit dem Tankerkönig Adapter und dem Datenpunkt tanken. 

```
on("tankerkoenig.0.stations.cheapest.e5.feed", function(dp) {
    var tankePreis = getState("tankerkoenig.0.stations.cheapest.e5.feed").val;

    setState("0_userdata.0.Siri.tanken", "Du zahlst " +tankePreis+ " je Liter.");
});
```

Um nun mittels Siri darauf zugreifen zu können erstellen wir auf einem iOS-Gerät ein Kurzbefehl:

