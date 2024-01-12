import io
from time import clock

def anzahl_buchstaben(wort):
    """ Erzeugt ein Dictionary mit der Anzahl des jeweiligen Buchstabens """

    anzahl = {buchstabe: 0 for buchstabe in wort}
    for buchstabe in wort:
        anzahl[buchstabe] += 1
    return anzahl


def kandidaten_testen(wort, kandidaten):
    """ Testet alle Kandidaten für ein Wort. Wenn ein Kandidat die selbe
    Länge hat und die selben Buchstaben benutzt, wird dieses Wort
    zurückgegeben. Wenn kein passendes Wort gefunden wurde wird None
    zurückgegeben. """

    # Anzahl an Buchstaben vom übergebenen Wort
    anzahl = anzahl_buchstaben(wort)
    for kandidat in kandidaten:
        # Ein Kandidat wird nur geteset, wenn er die gleiche Länge wie das
        # Wort hat
        if len(wort) == len(kandidat):
            # Anzahl des Kandidaten wird entweder berechnet und gespeichert
            # oder geladen, falls es bereits einmal berechnet wurde
            anzahl_kandidat = anzahl_buchstaben(kandidat)
            # Wenn die selben Buchstaben benutzt werden, wird der Kandidat
            # zurückgegeben
            if anzahl == anzahl_kandidat: return kandidat
    return None  # Es wurde kein passendes Wort gefunden


def enttwisten(wort):
    """ Übernimmt ein Wort und gibt die enttwistete Version zurück """

    buchstaben = (wort[0], wort[-1])  # Erster und letzter Buchstabe
    # Erster und letzter Buchstaben, kleingeschrieben
    buchstaben_klein = (wort[0].lower(), wort[-1])
    # Zuerst werden Wörter mit den exakt gleichen Anfangs- und Endbuchstaben
    # überprüft
    if buchstaben in sort_woerterbuch:
        # Liste mit Kandidaten wird geladen
        kandidaten = sort_woerterbuch[buchstaben]
        # Kandidaten werden getestet
        ergebnis = kandidaten_testen(wort, kandidaten)
        # Wenn ein Kandidat gepasst hat wird dieser zurückgegeben
        if ergebnis: return ergebnis
    # Wenn das Wort großgeschrieben ist, wird ebenfalls die kleingeschriebene
    # Version getestet
    if wort[0] != wort[0].lower() and buchstaben_klein in sort_woerterbuch:
        # Liste mit Kandidaten wird geladen
        kandidaten = sort_woerterbuch[buchstaben_klein]
        # Kandidaten werden getestet
        ergebnis = kandidaten_testen(wort.lower(), kandidaten)
        # Wenn ein Kandidat gepasst hat wird dieser
        # großgeschrieben zurückgegeben
        if ergebnis: return ergebnis[0].capitalize() + ergebnis[1:]
    # Kein Kandidat hat gepasst, deshalb wird das ursprüngliche Wort
    # zurückgegeben
    return wort


clock()
eingabe_datei = "twist5lsg.txt"
# Gesamter Text der Eingabedatei
eingabe = io.open(eingabe_datei, "r", encoding="utf-8").read()
# Ausgabedatei wird geöffnet
ausgabe = io.open("enttwistet.txt", "w", encoding="utf-8")
# Alphabet wird festgelegt
alphabet = "abcdefghijklmnopqrstuvwxyzäöüßABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ"
# Liste mit jeweiligen Zeilen des Wörterbuchs
woerterbuch = io.open("woerterliste.txt", "r", encoding="utf-8").readlines()


neuer_text = ""  # Variable für den neuen Text
sort_woerterbuch = {} # Dictionary für das "sortierte" Wörterbuch

# "\n"-Zeichen am Ende aller Worte werden gelöscht
woerterbuch = [wort[:-1] for wort in woerterbuch]


for wort in woerterbuch:
    buchstaben = (wort[0], wort[-1])  # Erster und letzter Buchstabe

    # Wort wird ins Wörterbuch aufgenommen. Falls es diese
    # Buchstabenkombination bereits gab, wird das Wort an die Liste
    # angehängt, sonst wird eine neue Liste erstellt
    if buchstaben in sort_woerterbuch:
        sort_woerterbuch[buchstaben].append(wort)
    else:
        sort_woerterbuch[buchstaben] = [wort]


# Alle Zeichen des Textes werden durchgegangen
i = 0
while i < len(eingabe):
    # Wort wird gesucht, solange die Zeichen im Alphabet sind gehören sie
    # zum Wort und werden dem Wort angehängt
    wort = ""
    while i < len(eingabe) and eingabe[i] in alphabet:
        wort += eingabe[i]
        i += 1
    if wort != "":
        # Dem neuen Text wird das enttwistete Wort angehängt
        neuer_text += enttwisten(wort)
    # Solange Zeichen nicht im Alphabet sind, werden sie einfach dem Text
    # angehängt
    while i < len(eingabe) and eingabe[i] not in alphabet:
        neuer_text += eingabe[i]
        i += 1
print(neuer_text, file=ausgabe, end="")  # Fertiger Text wird gespeichert
print (clock())