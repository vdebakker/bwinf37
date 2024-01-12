import itertools
from time import clock


def s(r1, r2):
    """ Gibt den Wert der seriellen Schaltung der zwei Widerstände zurück """
    return r1 + r2


def p(r1, r2):
    """ Gibt den Wert der parallelen Schaltung der zwei Widerstände zurück """
    return 1 / (1 / r1 + 1 / r2)


def s_ausgabe(s1, s2):
    """ Gibt den Bauplan der seriellen Schaltung von zwei kleineren
        Schaltungen zurück """
    return "seriell(" + str(s1) + ", " + str(s2) + ")"


def p_ausgabe(s1, s2):
    """ Gibt den Bauplan der parallelen Schaltung von zwei kleineren
        Schaltungen zurück """
    return "parallel(" + str(s1) + ", " + str(s2) + ")"


def funktionen(k):
    """ Gibt alle möglichen Funktionen zur Erzeugung von neuen Widerstände
        aus genau k Widerständen zurück."""
    if k == 1: # Bei einem Widerstand kann nur dieser Widerstand erzeugt werden
        yield lambda x: x
    elif k == 2:
        # Bei zwei Widerständen können diese nur parallel oder seriell
        # geschaltet werden
        yield p
        yield s
    elif k == 3:
        # Bei drei Widerständen können die folgenden vier unterschiedlichen
        # Kombinationen erstellt werden
        yield lambda r1, r2, r3: p(p(r1, r2), r3)
        yield lambda r1, r2, r3: s(p(r1, r2), r3)
        yield lambda r1, r2, r3: p(s(r1, r2), r3)
        yield lambda r1, r2, r3: s(s(r1, r2), r3)
    elif k == 4:
        # Bei vier Widerständen können die folgenden zwölf unterschiedlichen
        # Kombinationen erstellt werden
        yield lambda r1, r2, r3, r4: p(p(r1, r2), s(r3, r4))
        yield lambda r1, r2, r3, r4: p(s(r1, r2), s(r3, r4))
        yield lambda r1, r2, r3, r4: s(p(r1, r2), p(r3, r4))

        yield lambda r1, r2, r3, r4: p(p(p(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: s(p(p(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: p(s(p(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: s(s(p(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: p(p(s(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: s(p(s(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: p(s(s(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: s(s(s(r1, r2), r3), r4)


def bauplaene(k):
    """ Gibt alle möglichen Baupläne zur Erzeugung von neuen Widerstände
        aus genau k Widerständen zurück."""
    if k == 1:  # Bei einem Widerstand kann es nur einen Bauplan geben
        yield lambda x: str(x)
    elif k == 2:
        # Bei zwei Widerständen können diese nur parallel oder seriell
        # geschaltet werden
        yield p_ausgabe
        yield s_ausgabe
    elif k == 3:
        # Bei drei Widerständen können die folgenden vier unterschiedlichen
        # Kombinationen erstellt werden
        yield lambda r1, r2, r3: p_ausgabe(p_ausgabe(r1, r2), r3)
        yield lambda r1, r2, r3: s_ausgabe(p_ausgabe(r1, r2), r3)
        yield lambda r1, r2, r3: p_ausgabe(s_ausgabe(r1, r2), r3)
        yield lambda r1, r2, r3: s_ausgabe(s_ausgabe(r1, r2), r3)
    elif k == 4:
        # Bei vier Widerständen können die folgenden zwölf unterschiedlichen
        # Kombinationen erstellt werden
        yield lambda r1,r2,r3,r4: p_ausgabe(p_ausgabe(r1,r2),s_ausgabe(r3,r4))
        yield lambda r1,r2,r3,r4: p_ausgabe(s_ausgabe(r1,r2),s_ausgabe(r3,r4))
        yield lambda r1,r2,r3,r4: s_ausgabe(p_ausgabe(r1,r2),p_ausgabe(r3,r4))

        yield lambda r1, r2, r3, r4: p_ausgabe(p_ausgabe(p_ausgabe(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: s_ausgabe(p_ausgabe(p_ausgabe(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: p_ausgabe(s_ausgabe(p_ausgabe(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: s_ausgabe(s_ausgabe(p_ausgabe(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: p_ausgabe(p_ausgabe(s_ausgabe(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: s_ausgabe(p_ausgabe(s_ausgabe(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: p_ausgabe(s_ausgabe(s_ausgabe(r1, r2), r3), r4)
        yield lambda r1, r2, r3, r4: s_ausgabe(s_ausgabe(s_ausgabe(r1, r2), r3), r4)

clock()
""" Eingabe wird geöffnet und eingelesen """


# Eingabe und Ausgabe werden geöffnet
eingabe_datei = "widerstaende.txt"
eingabe = open(eingabe_datei).readlines()
ausgabe = open("bauplaene.txt", "w")
print("Ergebnisse", file=ausgabe)

# Widerstnde und benötigte Widerstände werden eingelesen
widerstaende = [int(w) for w in eingabe]
benoetigt = [int(i) for i in open("benoetigt.txt")]


""" Schaltungen  finden """

# Listen für Wert der besten Schaltung und zugehörige Schaltung werden erstellt
# Der Eintrag bei Index i ist die Schaltung für den i. benötigten Widerstand
beste_werte = [9e9] * len(benoetigt)
beste_bauplaene = [""] * len(benoetigt)

# For-Schleife probiert Schaltung mit genau 1, 2 .. k Widerständen aus
for anzahl_widerstande in range(1, 5):
    # Die Kombinationen aus genau anzahl_widerstande Widerständen werden
    # erstellt.
    kombinationen = list(itertools.permutations(widerstaende, anzahl_widerstande))
    # Alle möglichen Baupläne und dazugehörigen Funktionen werden ausprobiert
    for bauplan, funktion in zip(bauplaene(anzahl_widerstande),
                             funktionen(anzahl_widerstande)):
        # Jede Kombination an Widerständen wird ausprobiert
        for kombination in kombinationen:
            # Der Wert dieser Schaltung wird errechnet
            wert = funktion(*kombination)
            # Alle benötigten Widerstände werden durchgegangen
            for j in range(len(benoetigt)):
                # Ist der neue Wert besser als der alte Wert, werden Bauplan
                #  und ihr Wert abgespeichert.
                if abs(wert - benoetigt[j]) < abs(benoetigt[j] - beste_werte[j]):
                    beste_werte[j] = wert
                    beste_bauplaene[j] = bauplan(*kombination)

    # Baupläne und die dazugehörigen Werte werden ausgegeben
    print("\nMax. Anzahl Widerstände: k=", anzahl_widerstande, file=ausgabe)
    for ziel, wert, bauplan in zip(benoetigt, beste_werte, beste_bauplaene):
        print("Ziel: %d Ohm | Schaltung: %s | Erreicht: %.4f Ohm | Differenz: %.4f Ohm" %
                (ziel, bauplan, wert, ziel-wert), file=ausgabe)
print(clock())