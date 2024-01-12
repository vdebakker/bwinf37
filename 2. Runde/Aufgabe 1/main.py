from kante import Kante

from math import asin, tan
from random import random

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Polygon

''' Eingabe und Ausgabe öffnen '''

in_datei = "lisarennt.txt"  # Eingabedatei
out_datei = "lisarennt_out.txt"  # Ausgabedatei
grafik_datei = "lisarennt_out.pdf"  # Datei der Ausgabegrafik

input_list = open(in_datei, "r").readlines()  # Liste mit eingelesenen Zeilen
out = open(out_datei, "w")  # Ausgabedatei wird geöffnet
fig, ax = plt.subplots()  # Subplots werden erstellt

''' Konstanten festlegen '''

# Farben werden festgelegt
farbe_weg = "red"
farbe_polygone = "grey"
farbe_start_ende = "green"
farbe_bus = "blue"

INF = 1000000  # 'Unendlich': Sehr große Zahl für Dijkstra

# Startzeit des Bus in Stunden, Minuten, Sekunden
startzeit_bus = [7, 30, 0]

# Startzeit wird zu Sekunden umgerechnet
startzeit_bus = startzeit_bus[0] * 3600 + startzeit_bus[1] * 60 \
                + startzeit_bus[2]

# Startkoordinaten des Busses. Lisa kann nocht vor dem Startpunkt einsteigen
startpunkt_bus = (0, 0)

# Koordinaten der Schule. Lisa kann nicht hinter der Schule einsteigen
schule = (0, 3000)

# Geschindigkeiten in km/h
v_lisa = 15
v_bus = 30

# Geschwindigkeiten werden von km/h in m/s umgerechnet
v_lisa /= 3.6
v_bus /= 3.6

# Lisas Geschwindigkeit muss kleiner als die des Busses sein
if v_lisa > v_bus:
    print("Es gibt keine optimale Lösung, da die Geschwindigkeit von Lisa "
          "größer ist als die des Busses.", file=out)
    exit(0)
elif v_lisa == v_bus:
    print("Es gibt keine optimale Lösung, da die Geschwindigkeit von Lisa "
          "gleich der des Busses ist.", file=out)
    exit(0)

# Winkel für optimalen Laufweg von Lisa zur Straße
optimaler_winkel = asin(v_lisa / v_bus)


''' Zuordnung der Eingabeinformationen zu Variablen '''

p = int(input_list[0])  # Anzahl p der Polygone
haus = [int(s) for s in input_list[-1].split(' ')]  # Position von Lisas Haus
knoten = [haus]  # Liste mit Positionen aller Knoten

# Liste mit allen Polygonen, die wiederum jeweils als Listen gespeichert
# werden
polygone = []

# Liste mit Nummern der Polygone, zu denen die Punkte der Liste "knoten"
# gehören. Das Haus gehört zu keinem Polygon, ihm  wird deshalb der Wert -1
# zugeordnet
gehoert_zu = [-1]


''' Listen mit Koordinaten der Polygone und Kanten erstellen '''

# Polygone werden eingelesen
for i in range(p):
    # Zeile wird zerteilt und in Zahlen umgewandelt
    zerteilt = [int(s) for s in input_list[i + 1].split(' ')]

    n = zerteilt[0]  # Anzahl n der Ecken eines Polygons
    polygon = []  # Liste mit Eckpunkten dieses neuen Polygons
    for j in range(n):
        # X und Y Koordinate des jeweiligen Eckpunkts
        x = zerteilt[j * 2 + 1]
        y = zerteilt[j * 2 + 2]

        # Eckpunkt wird der Liste "polygon" angehängt
        polygon.append((x, y))

        # Neuer Eckpunkt gehört zu Polygon i
        gehoert_zu.append(i)

    # Neues Polygon wird an Liste mit Polygonen angehängt
    polygone.append(polygon)

    # Liste mit allen Knoten wird erweitert
    knoten.extend(polygon)

''' Kanten der Polygone berechnen '''

alle_kanten = []  # Liste mit allen Kanten der Polygone
polygon_kanten = []  # Liste mit Kanten gruppiert nach Polygonen. Jede Liste
# enthält Kanten eines Polygons

# Kanten der Polygone werden berechnet
for polygon in polygone:
    neue_kanten = []  # Liste mit Kanten dieses neuen Polygons
    for i in range(len(polygon) - 1):
        # Kante zwischen Eckpunkten i und i + 1 wird erstellt
        neue_kanten.append(Kante(polygon[i], polygon[i + 1]))
    # Kante zwischen dem ersten und letzten Eckpunkt wird erstellt
    neue_kanten.append(Kante(polygon[-1], polygon[0]))

    # Alle Knoten der Liste "neue_kanten" werden an "alle_kanten" angehängt
    alle_kanten.extend(neue_kanten)
    # Liste "neue_kanten" wird als ganze Liste an "polygon_kanten" angehängt
    polygon_kanten.append(neue_kanten)


''' Adjazenzmatrix berechnen '''

adj = []  # Adjazenzmatrix
for i, punkt1 in enumerate(knoten):
    adj.append([])  # Neue Zeile wird hinzugefügt
    for j, punkt2 in enumerate(knoten):
        if i > j:
            # Zelle wurde bereits berechnet
            adj[i].append(adj[j][i])
            continue
        # Falls Punkte gleich sind, wird 0 angehängt. Keine Prüfung notwendig
        if punkt1 == punkt2:
            adj[i].append(0)
            continue
        # Neue Kante zwischen Punkt1 und Punkt2 wird erstellt
        neue_kante = Kante(punkt1, punkt2)
        # Es wird überprüft, ob die Kante durch ein Polygon führt
        durch_polygon = False
        for andere_kante in alle_kanten:
            if neue_kante.schneidet(andere_kante):
                # Falls die Kante eine andere Kante schneidet, geht die neue
                # Kante durch ein Polygon und es kann abgebrochen werden
                durch_polygon = True
                break
        if durch_polygon:
            # Falls die Kante durch ein Polygon führt ist dieser Weg
            # unmöglich und es wird eine große Zahl hinzugefügt
            adj[i].append(INF)
        elif gehoert_zu[i] != gehoert_zu[j]:
            # Falls die Kante nicht durch ein Polygon führt ist dieser
            # Weg möglich und es wird die Länge der Kante angehängt
            adj[i].append(neue_kante.laenge())
        elif neue_kante in polygon_kanten[gehoert_zu[i]]:
            # Falls die neue Kante die Kante eines Polygons ist, kann die 
            # Länge angehängt werden
            adj[i].append(neue_kante.laenge())
        else:
            mitte = neue_kante.mitte()  # Mitte der Kante wird ermitelt
            # Kante von der Mitte zu einem zufälligen Punkt wird erstellt.
            # Die Kante endet definitiv außerhalb des Polygons
            zufallskante = Kante(mitte, (random() * 1000000, 1000000))

            # Es wird gezählt, wie viele Kanten des Polygons von der
            # zufälligen Kante geschnitten werden.
            zaehler = 0
            for andere_kante in polygon_kanten[gehoert_zu[i]]:
                if zufallskante.schneidet(andere_kante):
                    zaehler += 1
            if zaehler % 2 == 0:
                # Wenn die zufällige Kante eine gerade Anzahl an Kanten
                # geschnitten hat, liegt die Kante außerhalb des Polygons
                adj[i].append(neue_kante.laenge())
            else:
                # Wenn die zufällige Kante eine ungerade Anzahl an Kanten
                # geschnitten hat, liegt die Kante innerhalb des Polygons
                adj[i].append(INF)


''' Kürzeste Wege berechnen '''

abstand = [INF] * len(knoten)  # Der Abstand jedes Knotens zu Lisas Haus

# Der Index des letzten Knotens auf dem kürzesten Weg von Lisas Haus zum
# jeweiligen Knoten
vorgaenger = [-1] * len(knoten)

# Liste mit Wahrheitswerten, ob die kürzesten Pfade mit dem jeweiligen Knoten
# bereits eweitert wurden
erweitert = [False] * len(knoten)
abstand[0] = 0  # Der Abstand zu Lisas Haus ist 0

# Dijkstra Algorithmus für kürzeste Pfade
for i in range(len(knoten)):
    # Index des Knoten mit kleinsten Abstand zu Lisas Haus, der noch nicht
    # expandiert wurde
    kuerzester = -1
    kleinster_abstand = INF  # Kleinster Abstand zu Lisas Haus
    for j in range(len(knoten)):
        if abstand[j] < kleinster_abstand and not erweitert[j]:
            # Kleinster Abstand und Index werden neu gesetzt
            kuerzester = j
            kleinster_abstand = abstand[j]

    # Kürzester Pfad an diesem Knoten wird nun expandiert
    erweitert[kuerzester] = True
    for j in range(len(knoten)):
        if abstand[j] > abstand[kuerzester] + adj[kuerzester][j]:
            # Wenn der bisher kleinste Anstand zum Knoten j gößer ist als
            # der Abstand zum kürzesten Knoten + die Kante zwischen dem
            # kürzesten Knoten und j, wurde ein kürzerer Pfad gefunden

            # Kürzester Abstand zu Knoten j wird aktualisiert
            abstand[j] = abstand[kuerzester] + adj[kuerzester][j]

            # Vorgänger von j wird anf Knoten gesetzt
            vorgaenger[j] = kuerzester


''' Treffpunkte und benötigte Zeiten berechnen '''

# Liste mit den idealen Treffpunkten für Bus und Lisa
treffpunkte = []

# Listen mit Zeit in Sekunden, die Lisa und der Bus zum jeweiligen
# Treffpunkt benötigen
zeit_bus = []
zeit_lisa = []
for i in range(len(knoten)):
    # Idealer Treffpunkt wird berechnet für den Fall, dass Lisa über Knoten i
    # geht
    treffpunkt = (startpunkt_bus[0], knoten[i][1] + tan(optimaler_winkel) *
                  abs(knoten[i][0] - startpunkt_bus[0]))

    if treffpunkt[1] < startpunkt_bus[1]: treffpunkt = startpunkt_bus
    if treffpunkt[1] > schule[1]: treffpunkt = schule

    # Letzte Kante zwischen Knoten i und Treffpunkt
    letzte_kante = Kante(knoten[i], treffpunkt)

    # Es wird überprüft, ob diese Kante nicht durch ein Polygon führt
    durch_polygon = False
    for andere_kante in alle_kanten:
        if letzte_kante.schneidet(andere_kante):
            durch_polygon = True
            break
    if not durch_polygon:
        # Abstand von Lisa zum Treffpunkt über Knoten i
        abstand[i] += letzte_kante.laenge()
        # Zeit, die der Bus und Lisa zum Teffpunkt benötigen
        zeit_bus.append((treffpunkt[1] - startpunkt_bus[1]) / v_bus)
        zeit_lisa.append(abstand[i] / v_lisa)
    else:
        zeit_bus.append(-INF)
        zeit_lisa.append(INF)
    # Treffpunkt wird gespeichert
    treffpunkte.append(treffpunkt)


''' 'Besten' Weg finden '''

# "Bester" Pfad wird herausgesucht. Der Index des letzten Knoten des besten
# Pfades wird gespeichert
bester = 0
for i in range(len(knoten)):
    # Wenn die Zeitdifferenz geringer ist, ist ein neuer Weg gefunden
    if zeit_lisa[i] - zeit_bus[i] < zeit_lisa[bester] - zeit_bus[bester]:
        bester = i

''' Graphische Ausgabe der Ergebnisse '''

for polygon in polygone:
    # Polygon wird gezeichnet
    ax.add_patch(Polygon(polygon, fill=True, color=farbe_polygone, linewidth=0))

pfad = [bester]  # Pfad wird gespeichert

# Momentaner und letzter Knoten
momentan = vorgaenger[bester]
letzter = bester
# Wege werden gezeichnet
while momentan != -1:
    # X- und Y-Koordinaten der Kante
    x = (knoten[momentan][0], knoten[letzter][0])
    y = (knoten[momentan][1], knoten[letzter][1])
    # Kante wird gezeichnet
    ax.add_line(Line2D(x, y, color=farbe_weg))
    # Pfad wird verlängert
    pfad.append(momentan)
    # Letzter und momentaner Knoten werden auf die nächste Kante gesetzt
    letzter = momentan
    momentan = vorgaenger[momentan]

# Kante zwischen Treffpunkt und letztem Punkt wird eingezeichnet
x = (knoten[bester][0], treffpunkte[bester][0])
y = (knoten[bester][1], treffpunkte[bester][1])
ax.add_line(Line2D(x, y, color=farbe_weg))

x = (startpunkt_bus[0], treffpunkte[bester][0])
y = (startpunkt_bus[1], treffpunkte[bester][1])

# Busfahrt, Haus, Treffpunkt und Busstartpunkt werden eingezeichnet
ax.add_line(Line2D(x, y, color=farbe_bus))
ax.add_patch(Circle(haus, 7, color=farbe_start_ende))
ax.add_patch(Circle(treffpunkte[bester], 7, color=farbe_start_ende))
ax.add_patch(Circle(startpunkt_bus, 7, color=farbe_start_ende))

# Bild wird automatisch auf richtige Größe gebracht und gespeichert
ax.autoscale()
plt.savefig(grafik_datei)


''' Start- und Treffzeit werden berechnet '''

# Treffzeit und Startzeit von Lisa in Sekunden
treffzeit = startzeit_bus + zeit_bus[bester]
startzeit_lisa = treffzeit - zeit_lisa[bester]

# Treffzeit in Stunden, Minuten und Sekunden umrechnen
treffzeit = [treffzeit // 3600, treffzeit // 60, treffzeit]
startzeit_lisa = [startzeit_lisa // 3600, startzeit_lisa // 60, startzeit_lisa]

treffzeit[0] %= 24
startzeit_lisa[0] %= 24
treffzeit[1] %= 60
startzeit_lisa[1] %= 60
treffzeit[2] %= 60
startzeit_lisa[2] %= 60
treffzeit[2] = round(treffzeit[2])
startzeit_lisa[2] = round(startzeit_lisa[2])


''' Textausgabe der Ergebnisse '''

pfad = pfad[::-1]  # Pfad wird umgedreht

# Ausgabe aller relevanten Daten im richtigen Format
print("Lisas Startzeit: %d:%2d:%2d Uhr" % (startzeit_lisa[0],
    startzeit_lisa[1], startzeit_lisa[2]), file=out)
print("Treffzeit: %d:%2d:%2d Uhr" % (treffzeit[0], treffzeit[1],
                                        treffzeit[2]), file=out)
print("Koordinaten Treffpunkt (x, y): (%dm, %dm)" % (round(treffpunkte[bester][
                                                             0]),
      round(treffpunkte[bester][1])), file=out)
print("Lisa benötigt %dmin %dsec" % (zeit_lisa[bester] // 60,
                                 round(zeit_lisa[bester] % 60)), file=out)
print("Lisa läuft %dm" % round(abstand[bester]), file=out)
print("Sie läuft über die Knoten: ", file=out)
gehoert_zu[0] = "L (Lisas Haus)"
print("  Punkt: (%d, %d)  %s" % (knoten[0][0], knoten[0][1],
                                            str(gehoert_zu[0])), file=out)

for i in pfad:
    if i != 0: print("  Punkt: (%d, %d)  Polygon: P%s" % (knoten[i][0], knoten[\
            i][1], str(gehoert_zu[i] + 1)), file=out)

out.close()