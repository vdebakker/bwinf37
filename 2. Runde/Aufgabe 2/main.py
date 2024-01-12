from dreieck import *
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from random import seed, choices, random
from time import clock

def zeichne(dreiecke, name):
    # Zeichnet die Dreiecke und speichert das Bild unter dem übergebenen
    # Namen ab
    ax.clear()
    for i, drei in enumerate(dreiecke):
        ax.add_patch(Polygon(drei.ecken(), facecolor=['r', 'yellow', 'green',
                     'orange','lime', 'magenta', 'b'][i%7],
                             edgecolor='black', linewidth=.5))
    ax.autoscale()
    plt.axis("scaled")
    plt.savefig(name, dpi=500)


def schneidet(dreieck, platzierte_dreiecke):
    # Prüft, ob übergebenes Dreieck die bereits platzierten Dreiecke schneidet
    for anderes in platzierte_dreiecke:
        if dreieck.schneidet(anderes): return True
    return False


def einseitig_einordnen(dreieck, winkel, luecke, platzierte_dreiecke):
    # Ordnet das Dreieck an der richtigen Stelle ein und gibt zurück,
    # ob es nicht mit bereits platzierten Dreiecken kollidiert
    dreieck.einordnen(winkel, luecke)
    if not schneidet(dreieck, platzierte_dreiecke):
        platzierte_dreiecke.append(dreieck)
        dreieck.platziert = True
        return True
    return False

def dreieck_einordnen(dreieck, winkel, luecke, platzierte_dreiecke):
    # Versucht das Dreieck an die gegebene Position einzuordnen. Falls das
    # nicht gelingt, wird das Dreieck gespiegelt und wiederholt eingeordnet
    if einseitig_einordnen(dreieck, winkel, luecke, platzierte_dreiecke):
        return True
    dreieck.spiegeln()
    return einseitig_einordnen(dreieck, winkel, luecke, platzierte_dreiecke)

def alle_einordnen(rechts, links, luecken, platzierte_dreiecke, zu_verteilen):
    # Versucht alle Dreiecke einzuordnen

    # Anzahl an Dreiecken, die vorher noch nicht platziert wurden und nun
    # erfolgreich platziert wurden
    platziert = 0
    # Anzahl an Dreiecken, die im jeweiligen Durchlauf erfolgreich platziert
    # wurden
    hinzugefuegt = 1

    # Es kann abgebrochen werden, wenn in einem Durchlauf keine Dreiecke
    # hinzugefügt wurden oder alle Dreiecke erfolgreich platziert wurden
    while hinzugefuegt > 0 and platziert != len(zu_verteilen):
        # In diesem Durchlauf wurden bisher 0 Dreiecke platziert
        hinzugefuegt = 0
        # Jedes Dreieck wird aufgerufen
        for drei in zu_verteilen:
            # Das Dreieck wird übersprungen, wenn es bereits platziert wurde
            if drei.platziert: continue
            # Jede Lücke wird getestet
            for l in range(len(luecken)):
                # Das Dreieck wird bei der l-ten Lücke von vorne auf der
                # linken Seite eingeordnet
                if rechts[l] - links[l] >= drei.kleinster_winkel():
                    # Der Winkel der Lücke ist groß genug, um das neue
                    # Dreieck einzuordnen
                    if dreieck_einordnen(drei, -links[l], luecken[l],
                                         platzierte_dreiecke):
                        # Das Dreieck wurde erfolgreich eingeordnet und der
                        # Winkel in der Lücke muss aktualisiert werden
                        links[l] += drei.kleinster_winkel() + 0.0001
                        break

                # Das Dreieck wird bei der l-ten Lücke von hinten auf der
                # linken Seite eingeordnet
                if rechts[-l - 1] - links[-l - 1] >= drei.kleinster_winkel():
                    # Der Winkel der Lücke ist groß genug, um das neue
                    # Dreieck einzuordnen
                    if dreieck_einordnen(drei, -rechts[-l - 1] +
                       drei.kleinster_winkel(), luecken[-l - 1],
                                         platzierte_dreiecke):
                        # Das Dreieck wurde erfolgreich eingeordnet und der
                        # Winkel in der Lücke muss aktualisiert werden
                        rechts[-l - 1] -= drei.kleinster_winkel() + 0.0001
                        break
            hinzugefuegt += drei.platziert
        platziert += hinzugefuegt
    # Es wird zurückgegeben, ob alle Dreieck eingeordnet werden konnten
    return platziert == len(zu_verteilen)

# Seed wird festgelegt, damit die gleichen Ergebnisse wieder erzielt werden
# können
seed(42)

# Eingabe- und Ausgabedateinamen
in_datei = "dreiecke_in.txt"
out_datei = "dreiecke_out.txt"
out_grafik = "dreiecke_out.pdf"

out = open(out_datei, "w")  # Ausgabedatei wird geöffnet

fig, ax = plt.subplots()  # Subplots der Anzeige

# Die Anzahl an Lösungen, die das Programm konstruieren soll
max_durchlaeufe = 5000

# Maximale Anzahl an Sekunden, sodass das Programm nach dieser Zeit
# automatisch beendet wird. Bei großen Beispielen brauchen einzelne Lösungen
# länger und es wird nach dieser Zeit abgebrochen
max_sekunden = 30

''' Eingabe einlesen '''

# Eingabe wird geöffnet und Zeilen werden eingelesen und in Liste gespeichert
input_list = open(in_datei).readlines()

d = int(input_list[0])  # Azahl d an Dreiecken

dreiecke = []  # Liste mit allen Dreiecken in Anfangsposition
gesamt = 0  # Summe aller kleinsten Winkel
for i in range(d):
    # Zeile wird nach Leerzeichen getrennt, in Ganzzahlen umgewandelt und in
    # einer Liste gespeichert
    getrennt = [int(s) for s in input_list[i + 1].split(' ')]

    # Die verschiedenen Eckpunkte A, B und C
    A, B, C = getrennt[1:3], getrennt[3:5], getrennt[5:7]

    # Dreieck wird der Liste angehängt
    dreiecke.append(Dreieck(A, B, C, "D" + str(i + 1)))
    # Kleinster Winkel des letzen Dreiecks wird entsprechend addiert
    gesamt += dreiecke[-1].kleinster_winkel()

''' Lösung suchen '''

# Der kürzeste Abstand, der bisher gefunden wurde, zu Beginn sehr groß
kuerzester_abstand = 1000000
# Speichert die betse Konstellation von Dreiecken, die bisher gefunden wurde
beste_konstellation = []
durchlauf = 1  # Variable um den Durchlauf zu zählen
while clock() < max_sekunden and durchlauf <= max_durchlaeufe:
    # Summe an Winkel, die verfügbar sind um die verbleibenden Dreiecke zu
    # platzieren. Dies sind die Winkel in den Lücken und am Rand
    verfuegbar = 180
    # Summe an Winkel die mindestens benötigt werden, um die verbleibenden
    # Dreiecke zu platzieren. Das ist jeweils der kleinste Winkel der
    # verbleibenden Dreiecke
    benoetigt = gesamt

    # Liste mit den X-Koordinaten der Lücken. Bei jedem Index steht,
    # bei welcher X-Koordinate eine Lücke ist
    luecken = [0]

    # Liste mit Winkeln der Lücken. In der Liste links steht, bei welchem
    # Winkel die Lücke anfägt. In der Liste rechts steht, bei welchdm Winkel
    # die Lücke aufhört. Zu Beginn gibt es eine Lücke, die bei 0 Grad
    # anfängt und bei 180 Grad aufhört
    links, rechts = [0], [180]

    # Bei den ersten 50 Durchläufen werden die Dreiecke sortiert, danach
    # zufällig gewählt
    zufaellig = durchlauf > 50

    # Eine Funktion wird definiert, um die Dreiecke zu sortieren bzw. zufällig
    # zu ordnen. Die Funktion gibt an, in welcher Reihenfolge die
    # verbleibenden Dreiecke in die Lücken gefüllt werden sollen
    if zufaellig: funktion = lambda d: - d.o * d.o * random()
    else: funktion = lambda d: - d.o

    # Liste mit Dreiecken, die noch verteilt werden müssen und mit der
    # vorhin definierten Funktion sortiert wurden. Die Dreiecke füllen die
    # Lücken in dieser Reihenfolge
    zu_verteilen = sorted((d.kopie() for d in dreiecke), key=funktion)
    platziert = []  # Liste mit Dreiecken, die bereits platziert wurden

    # Liste mit Gewichten um zu entscheiden, welches Dreieck als nächstes
    # fest platziert werden soll
    gewichte = [d.kleinster_winkel() * d.kleinster_winkel() for d in zu_verteilen]

    # Es wird weiter gesucht solange die Länge der momentanen Lösung kleiner
    # ist als die Länge der besten Lösung
    while luecken[-1] < kuerzester_abstand:
        if verfuegbar >= benoetigt:
            # Wenn es mehr verfügbare Winkel gibt als benötigt werden kann
            # versucht werden, alle verbleibenden Dreiecke einzuordnen
            if alle_einordnen(rechts[:], links[:], luecken, platziert[:],
                              zu_verteilen):
                # Wenn das Einordnen erfolgreich war, wird die Schleife
                # abgebrochen
                break
            # Wenn das Einordnen nicht erfolgreich war sind die Dreiecke
            # nicht mehr platziert
            for drei in zu_verteilen: drei.platziert = False

        # Ein Dreieck wird ausgewählt, das nun platziert wird. Die Auswahl
        # ist entweder sortiert oder zufällig
        if zufaellig:
            zu_platzieren = choices(range(len(zu_verteilen)), weights=gewichte)[0]
        else:
            zu_platzieren = max(range(len(zu_verteilen)), key=lambda i: gewichte[i])

        # Das neue Dreieck wird aus den Gewichten und den noch nicht
        # platzierten Dreiecken entfernt und den platzierten Dreiecken hinzugefügt
        platziert.append(zu_verteilen.pop(zu_platzieren))
        gewichte.pop(zu_platzieren)

        # Das platzierte Dreieck wird entsprechend positioniert. Die
        # X-Koordinate ist festgelegt, die Spiegelung und Basis sind zufällig
        platziert[-1].platziert = True
        if random() > .5: platziert[-1].spiegeln()
        platziert[-1].zufallsbasis()
        platziert[-1].nach_rechts(luecken[-1] - platziert[-1].punkt_links()[0])

        # Die neue Lücke liegt bei der X-Koordinate des rechten Punktes des
        # neuen Dreiecks
        luecken.append(platziert[-1].punkt_rechts()[0])

        # Die Winkel der Lücken werden aktualisiert. Dabei wird ein
        # Sicherheitsabstand von 0.0001 Grad hinzugefügt
        links.append(platziert[-1].winkel_rechts() + 0.0001)
        rechts[-1] -= platziert[-1].winkel_links() + 0.0001
        rechts.append(180)

        # Die verfügbare Winkelsumme und die Summe der benötigten Winkel
        # werden aktualisiert, da nun eine Lücke mehr verfügbar ist und ein
        # Dreieck weniger platziert werden muss
        verfuegbar += platziert[-1].winkel_oben()
        benoetigt -= platziert[-1].kleinster_winkel()

    if luecken[-1] < kuerzester_abstand:
        # Eine neue beste Verteilung wurde gefunden, da der Gesamtabstand
        # kleiner ist
        kuerzester_abstand = luecken[-1]
        beste_konstellation = platziert + zu_verteilen

    durchlauf += 1

''' Ausgabe '''

# Beste Konstellation wird nach Position für Ausgabe sortiert
beste_konstellation.sort(key=lambda d: d.winkel_strasse())
beste_konstellation.sort(key=lambda d: d.beruehrung_strasse())
zeichne(beste_konstellation, out_grafik)  # Grafische Ausgabe
# Ausgabe in Textform
print("%.3f" % kuerzester_abstand, file=out)
for drei in beste_konstellation:
    print(drei.ID, end="  ", file=out)
    for ecke in drei.ecken(): print("%d %d" % (ecke[0]+.5, ecke[1]+.5), end=" ", file=out)
    print(file=out)