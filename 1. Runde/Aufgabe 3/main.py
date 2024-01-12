def median(bereich):
    """ Gibt den Median/die mittlere Zahl der Glückszahlen zurück """
    return glueckszahlen[(bereich[0] + bereich[1]) // 2]

""" Eingabe wird eingelesen """

datei = "beispiel3"  # Name der Eingabedatei
eingabe = open(datei + ".txt").readlines()  # Liste mit Reihen der Eingabedatei
# Sortiert Glückszahlen der Teilnehmer
glueckszahlen = sorted([int(zeile) for zeile in eingabe])
ausgabe = open(datei + "lsg.txt", "w")
# Anzahl a Teilnehmern wird bestimmt
personen = len(glueckszahlen)
anzahl = 10  # Anzahl an Zahlen, die Al wählen soll

""" Kosten für alle möglichen Bereich wird berechnet """
# Ein Dictionary mit Bereich als Key und den Kosten für den jeweiligen
# Bereich als Value, die Kosten sind die Summe von allen Abständen zum Median
kosten = {}

# Kosten für Bereiche mit nur einer Zahl sind 0
for i in range(personen):
    kosten[(i, i)] = 0

# Kosten für alle möglichen Bereiche wird berechnet
for laenge in range(1, personen):
    # Alle möglichen Startpositionen des Bereichs werden erzeugt
    for start in range(personen - laenge):
        ende = start + laenge  # Ende des neuen Berecihs wird berechnet
        bereich_neu = (start, ende)  # Tupel des neuen Bereichs
        # Kosten für den neuen Bereich sind Kosten für den Bereich ohne die
        # letzte Zahl plus den Abstand der neuen Zahl vom Median
        kosten[bereich_neu] = kosten[(start, ende - 1)] + glueckszahlen[ende]\
                              - median(bereich_neu)

""" Auszahlung für meherere Breiche wird berechnet """

# Tabellen für Auszahlung und Bereiche werden festgelegt
auszahlung = [[]]
als_zahlen = [[]]

# Erste Zeile wird hinzugefügt
for ende in range(personen):
    # Erste Zeile der Auszahlung sind einfach nur die Kosten für den
    # entsprechenden Bereich
    auszahlung[0].append(kosten[(0, ende)])
    # Erste Zeile der Bereiche sind einfach nur einzelne Bereiche
    als_zahlen[0].append([median((0, ende))])

# Restliche Zeilen werden nacheinander berechnet
for reihe in range(2, anzahl + 1):
    # Neue Zeilen werden hinzugefügt
    auszahlung.append([])
    als_zahlen.append([])
    for ende in range(personen):
        # -1 als Flag für die Kosten und eine leere Liste von Bereichen
        # werden hinzugefügt
        auszahlung[reihe - 1].append(auszahlung[reihe - 2][ende])
        als_zahlen[reihe - 1].append(als_zahlen[reihe - 2][ende] + [-1])
        # Alle möglichen Startpunkte für den letzten Bereich werden berechnet
        # Die alten Bereiche hören bei grenze - 1 auf, der neue Bereich geht
        # von grenze bis ende. Die Grenze wird jeweils verschoben
        for grenze in range(1, ende + 1):
            neuer_bereich = (grenze, ende)
            # Die neue Auszahlung sind die gesamten Kosten für die alten
            # Bereiche plus die Kosten für den neuen Bereich
            neue_auszahlung = auszahlung[reihe - 2][grenze - 1] + \
                              kosten[neuer_bereich]
            if auszahlung[reihe - 1][ende] > neue_auszahlung:
                # Es wurde eine neue geringste Auszahlung gefunden
                auszahlung[reihe - 1][ende] = neue_auszahlung
                # Bereiche werden entrsprechend berechnet und gespeichert
                neue_mediane = als_zahlen[reihe - 2][grenze - 1] + \
                               [median(neuer_bereich)]
                als_zahlen[reihe - 1][ende] = neue_mediane

# Falls Anzahl der Teilnehmer kleiner ist als die Anzahl der Zahlen von Al:
# Al wählt die kleinste noch nicht vergebenen Zahl, Startpunkt = 1
nicht_gewaehlt = 1
fertige_zahlen = als_zahlen[anzahl - 1][personen - 1]
for i in range(anzahl):
    if fertige_zahlen[i] == -1:
        while nicht_gewaehlt in fertige_zahlen:
            nicht_gewaehlt += 1
        fertige_zahlen[i] = nicht_gewaehlt

# Lösung wird ausgegeben
print("Al sollte die Zahlen:", ", ".join([str(i) for i in fertige_zahlen]),
      "wählen.", file=ausgabe)
print("Er muss", auszahlung[anzahl - 1][personen - 1],
      "€ auszahlen und macht einen Gewinn von", personen * 25 -
      auszahlung[anzahl - 1][personen - 1], "€.", file=ausgabe)
ausgabe.close()