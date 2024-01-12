from math import cos, sin
from random import choice
from strecke import *

class Dreieck:
    def __init__(self, A, B, C, ID):
        self.A, self.B, self.C = A, B, C  # Eckpunkte des Dreiecks
        self.ID = ID  # ID(Bezeichnung) des Dreiecks
        # Kanten werden berechnet
        self.ab = Strecke(self.A, self.B)
        self.bc = Strecke(self.B, self.C)
        self.ca = Strecke(self.C, self.A)

        # Seitenlängen(a. b, c), Umfang(u) und Oberfläche(o) werden berechnet
        a, b, c = laenge(self.bc.v), laenge(self.ca.v), laenge(self.ab.v)
        u = a + b + c
        self.o = sqrt((u / 2) * (u / 2 - a) * (u / 2 - b) * (u / 2 - c))

        # Winkel werden berechnet
        self.alpha = 180 - winkel(self.ab.v, self.ca.v)
        self.beta = 180 - winkel(self.bc.v, self.ab.v)
        self.gamma = 180 - winkel(self.ca.v, self.bc.v)

        self.platziert = False  # Boolean, ob dieses Dreieck bereits
                                # platziert wurde

    def update_kanten(self):
        # Aktualisiert die Kanten
        for kante in self.ab, self.bc, self.ca: kante.update_vektor()

    def ecken(self):
        return self.A, self.B, self.C

    def runden(self):
        # Rundet die Koordinaten der Eckpunkte auf 6 Nachkommastellen
        for ecke in self.ecken():
            ecke[0], ecke[1] = round(ecke[0], 6), round(ecke[1], 6)

    def kleinster_winkel(self):
        return min(self.alpha, self.beta, self.gamma)

    def groesster_winkel(self):
        return max(self.alpha, self.beta, self.gamma)

    def kopie(self):
        return Dreieck(self.A[:], self.B[:], self.C[:], self.ID)

    def anstrasse(self):
        # Verschiebt das Dreieck entlang der Y-Achse so, dass es danach an
        # der Straße liegt
        temp = min(self.A[1], self.B[1], self.C[1])
        for ecke in self.ecken(): ecke[1] -= temp
        self.runden()

    def beruehrung_strasse(self):
        # Berechnet den Berührungspunkt mit der Straße
        if self.A[1] == 0: return self.A
        if self.B[1] == 0: return self.B
        return self.C

    def winkel_strasse(self):
        # Berechnet den Winkel zwischen Straße und Dreieck ausgehend vom
        # Punkt an der Straße
        if self.A[1] == 0:
            return min(winkel(vektor(self.A, self.B), (100, 0)),
                       winkel(vektor(self.A, self.C), (100, 0)))
        if self.B[1] == 0:
            return min(winkel(vektor(self.B, self.A), (100, 0)),
                       winkel(vektor(self.B, self.C), (100, 0)))
        return min(winkel(vektor(self.C, self.A), (100, 0)),
                   winkel(vektor(self.C, self.B), (100, 0)))

    def nach_rechts(self, distanz):
        # Verschiebt das Dreieck um eine bestimmte Distanz nach rechts
        for ecke in self.ecken(): ecke[0] += distanz
        self.runden()

    def punkt_oben(self):
        # Gibt den höchsten Punkt des Dreiecks zurück
        return max(self.ecken(), key=lambda p: p[1])

    def punkt_rechts(self):
        # Gibt den rechten Eckpunkt des Dreiecks aus
        return [max(self.A[0], self.B[0], self.C[0]), 0]

    def punkt_links(self):
        # Gibt den linken Eckpunkt des Dreiecks aus
        return [min(self.A[0], self.B[0], self.C[0]), 0]

    def winkel_oben(self):
        # Berechnet den Winkel am oberen Eckpunkt
        return winkel(vektor(self.punkt_oben(), self.punkt_links()),
                      vektor(self.punkt_oben(), self.punkt_rechts()))

    def winkel_rechts(self):
        # Berechnet den Winkel am rechten Eckpunkt
        return winkel(vektor(self.punkt_rechts(), self.punkt_oben()),
                      vektor(self.punkt_rechts(), self.punkt_links()))

    def winkel_links(self):
        # Berechnet den Winkel am linken Eckpunkt
        return winkel(vektor(self.punkt_links(), self.punkt_oben()),
                      vektor(self.punkt_links(), self.punkt_rechts()))

    def spiegeln(self):
        # Spiegelt das Dreieck an der Y-Achse
        for ecke in self.ecken(): ecke[0] = - ecke[0]
        self.update_kanten()

    def basis(self, seite):
        # Sorgt dafür, dass eine übegebene Seite Basis des Dreiecks wird,
        # also das Dreieck mit dieser gesamten Seite an der Straße liegt

        # Gegenüberliegender Punkt wird berechnet
        if seite == self.bc: punkt = self.A
        elif seite == self.ca: punkt = self.B
        else: punkt = self.C

        # Dreieck wird so gedreht, dass die Seite parallel zur Straße ist
        if seite.v[1] < 0: self.drehen(winkel([100, 0], seite.v))
        else: self.drehen(-winkel([100, 0], seite.v))
        self.anstrasse()

        if punkt[1] == 0:
            # Wenn der gegenüberliegende Punkt an der Straße
            # liegt, liegt die Seite nicht an der Straße und das Dreieck
            # muss um 180 Grad gedreht werden
            self.drehen(180)
            self.anstrasse()

    def zufallsbasis(self):
        # Die Basis wird zufällig gewählt. Dabei werden nur Seiten
        # berücksichtigt deren anliegende Seiten kleiner gleich 90 Grad sind
        poss = []
        if self.alpha <= 90 and self.beta <= 90: poss.append(self.ab)
        if self.beta <= 90 and self.gamma <= 90: poss.append(self.bc)
        if self.alpha <= 90 and self.gamma <= 90: poss.append(self.ca)
        self.basis(choice(poss))

    def drehen(self, w):
        # Dreht das Dreieck um den Mittelpunkt mit dem Winkel w

        # Mittelpunkt
        mittex = (self.A[0] + self.B[0] + self.C[0]) / 3
        mittey = (self.A[1] + self.B[1] + self.C[1]) / 3

        w *= pi / 180  # Winkel wird in Radian umgerechnet

        sinus, cosinus = sin(w), cos(w)  # Sinus und Cosinus wird berechnet

        # Für jede Ecke wird die Position neu berechnet
        for ecke in self.ecken():
            ecke[0] -= mittex
            ecke[1] -= mittey

            x = ecke[0] * cosinus - ecke[1] * sinus
            y = ecke[0] * sinus + ecke[1] * cosinus

            ecke[0], ecke[1] = mittex + x, mittey + y
        self.runden() # Die Eckpunkte werden gerundet
        self.update_kanten()  # Die Kanten werden aktualisiert

    def schneidet(self, anderes):
        # Prüft, ob dieses Dreieck das andere übergebene Dreieck schneidet.
        # Berührungen werden nicht als Schnittpunkte gewertet
        if self.punkt_links() >= anderes.punkt_rechts() or \
           self.punkt_rechts() <= anderes.punkt_links():
            # Wenn dieses Dreieck rechts oder links neben dem anderen
            # Dreieck liegt, kann abgebroche werden
            return False
        # Für alle Kanten wird geprüft, ob sie sich schneiden
        for kante in anderes.ab, anderes.bc, anderes.ca:
            if self.ab.schneidet(kante) or self.bc.schneidet(kante) or \
               self.ca.schneidet(kante): return True
        return False

    def einordnen(self, w, x):
        # Ordnet das Dreieck so ein, dass die kleinste Ecke die X-Koordinate
        # x hat, an der Straße liegt und die anliegende Seite den Winkel w
        # zur Straße hat
        temp = self.kleinster_winkel()
        # Anliegende Seite und Punkt an der Ecke mit dem kleinsten Winkel
        # werden gesucht
        if self.alpha == temp: seite, punkt = self.ab, self.A
        elif self.beta == temp: seite, punkt = self.bc, self.B
        else: seite, punkt = self.ca, self.C
        self.basis(seite) # Anliegende Seite wird als Berührungskante gewählt
        if punkt[0] <= self.punkt_links()[0] + 0.001:
            # Kleinste Ecke ist auf der linken statt rechten Seite
            w += 180 - temp
        # Dreieck wird mit bestimmten Winkel zur Straße positioniert
        self.drehen(w)
        # Dreieck wird zur richtigen X-Koordinate geschoben
        self.nach_rechts(x - punkt[0])
        self.anstrasse()
