# Beschreibung

Dies ist mein erstes Python und TKinter Projekt und dient als Versuchsobjekt was man noch so Sinnvolles hinzufügen kann. Die Idee war es ein Programm zu entwickeln das Daten von Punkt A nach B und C kopiert ohne Fehler beim Kopiervorgang. Zusätzlich zum Kopieren besteht die Möglichkeit, nach erfolgreichem kopieren, die Infos über die Dateien in eine Datenbank zu speichern. Es wird hierbei vorerst eine SQLite Datenbank verwendet. 
![Main Bereich](https://cdn.discordapp.com/attachments/724282844419194982/724289139536822312/main_view.jpg)

# Wofür kann ich das Programm verwenden?

Wenn Sie Wert legen das Ihre Dateien beim Kopieren immer sicher an die neuen Orte gelangen, sind Sie hier genau richtig. Dieses Programm prüft nach jedem Kopiervorgang ob der MD5 Hash von dem Original und der neuen Datei übereinstimmt. Sollte der Hash nicht übereinstimmen, werden Sie darüber informiert.


# Wozu ein solches Programm?

Man kennt es, man will schnell etwas kopieren und aus welchem Grund auch immer ist die Datei auf einmal fehlerhaft und die originale Datei bereits gelöscht. Damit man sich nun sicher sein kann, ob die Dateien alle korrekt und fehlerfrei am Zielort angekommen sind, habe ich dieses Programm geschrieben.

# Wie kann ich es benutzen?

Clonen Sie zunächst die Repo mit git clone https://github.com/ReneRup/MediaBackup.git.
Wechseln sie danach in das Verzeichnis MediaBackup.
Starten Sie die main.py mit python main.py -y oder python main.py -n.
Die Argumente y und n geben an ob Sie wünschen das eine lokale SQLite erstellt werden soll.
In der Datenbank stehen Infos zu den vollständig kopierten Dateien.
> git clone https://github.com/ReneRup/MediaBackup.git  
> cd MediaBackup  
> python main.py n


# Das Programm
## Wie starte ich das Programm
Wechseln Sie per CMD in das Verzeichnis des Programms.
Führen Sie nun (Python main.py y) oder (Python main.py n) aus ohne die ()

## Gestartet mit y Argument
![Mit y Argument](https://cdn.discordapp.com/attachments/724282844419194982/724289139536822312/main_view.jpg)

## Gestartet mit n Argument
![Mit n Argument](https://cdn.discordapp.com/attachments/724282844419194982/724289152509542520/main_view_n.jpg)


## Was ist der Unterschied zwischen y und n als Argument
An mit dem Argument y wird der Oberfläche ein kleiner Button am oberen rechten Rand hinzugefügt womit man die Datenbank auslesen kann. Dieser wird bei dem Argument n nicht mit angezeigt.

- Das Argument y, erstellt eine lokale SQLiDatenbank in der Dateiinformationen gespeichert werden wie zb. die Größe der kopierten Datei und die Pfade woher diese kommt und wohin diese kopiert worden ist.
- Das Argument n, erstellt keine lokale Datenbank und speichert somit keine Daten.

## Wie starte ich einen Kopiervorgang
- Klicken Sie auf Quelle wählen
- Wählen Sie den Ordner aus von dem Sie Daten kopieren wollen und bestätigen Sie die Auswahl
- Klicken Sie auf Kopierpfad wählen
- Wählen Sie den Zielordner aus wohin die Dateien kopiert werden sollen und bestätigen Sie die Auswahl
- (Optional) Klicken Sie auf Backuppfad wählen.
- (Optional) Wählen Sie einen anderen Zielordner aus wohin die Dateien kopiert werden sollen und bestätigen Sie die Auswahl
-  Wählen Sie nun aus der Tabelle die Dateien aus die Sie kopieren möchten
- Klicken Sie auf Kopieren starten

## Was passiert nach dem Klick auf Kopieren starten
Das Programm erfasst Ihre ausgewählten Dateien und kopiert diese an denen von Ihnen gewünschten Zielorte.
Dies wird visualisiert anhand von Fortschritts-leisten und deren Farbe. 
- Blau steht für das Kopieren von Dateien 
- Gelb für die Prüfung von Hash-werten
- Grün für den fehlerfreien Ablauf des Programms  
- Rot für einen Fehler

Sobald das Kopieren fehlerfrei abgelaufen ist, vergleicht das Programm die Hash-werte von der originalen Datei und der Datei am neuen Zielort.
Sie werden benachrichtigt ob der Ablauf fehlerfrei verlief oder ob es zu einem Fehler kam.
![Erfolgreicher Ablauf](https://cdn.discordapp.com/attachments/724282844419194982/724289929320071218/unknown.png)

## Wie öffne ich die Datenbankübersicht
Wenn Sie das Programm mit dem Argument y gestartet haben finden Sie oben rechts einen Button mit der Aufschrift "db". Klicken Sie auf diesen und Ihnen wird ein neues Fenster gezeigt. Sollten Sie eine passende Datenbankdatei vorhanden sein, wird diese mit dem Klick auf "Lese Datenbank" in der Tabelle angezeigt.
![Datenbank](https://cdn.discordapp.com/attachments/724282844419194982/724289276019343360/2.gif)
