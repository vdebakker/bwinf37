from math import sqrt, acos, pi


def vektor(pos1, pos2):
    return pos1[0] - pos2[0], pos1[1] - pos2[1]  # Vektor von Position 1 zu 2

def laenge(v):
    return sqrt(v[0] ** 2 + v[1] ** 2)  # Länge eines Vektos

def skalar(vektor1, vektor2):
    # Skalarprodukt von zwei Vektoren
    return vektor1[0] * vektor2[0] + vektor1[1] * vektor2[1]

def kreux_produkt_Z(vektor1, vektor2):
    # Berechnet nur die Z-Koordiante des Kreuzprodukts zwischen zwei Vektoren
    return vektor1[0] * vektor2[1] - vektor1[1] * vektor2[0]

def winkel(vektor1, vektor2):
    # Berechnet Winkel in Grad zwischen zwei Vektoren
    skalar_produkt = skalar(vektor1, vektor2)
    laengen = laenge(vektor1) * laenge(vektor2)
    return acos(skalar_produkt / laengen) / pi * 180


class Strecke:
    """
    Klasse, die eine Strecke mit den Endpunkten A und B darstellt. Es kann
    überprüft werden, ob diese Strecke eine andere Strecke schneidet
    """
    def __init__(self, a, b):
        # Zwei Endpunkte der Strecke: A und B
        self.a = a
        self.b = b
        self.v = vektor(self.a, self.b)  # Vektor von A zu B

    def update_vektor(self):
        # Funktion um den Vektor zu aktualisieren, falls die Punkte verändert
        # wurden
        self.v = vektor(self.a, self.b)

    def schneidet(self, andere):
        """
        Methode die überprüft, ob diese Strecke eine andere Strecke schneidet.
        Falls die Strecken gleiche Start- oder Endpunkte haben schneiden sich
        die Strecken nicht.
        :param andere: Andere Kante
        :return: Wahrheitswert, ob diese Kante die andere schneidet
        """
        # Die Endpunkte A und B der eigenen Gerade und die Endpunkte C und D
        # der andere Kante
        a, b = self.a, self.b
        c, d = andere.a, andere.b

        # Bei einem gleichen Endpunkt schneiden sich die Strecken nicht
        if a == c or a == d or b == c or b == d: return False

        # Die Z-Koordinaten der Kreuzprodukte werden berechnet. Die Z
        # Koordianten geben an, auf welcher Seite die Punkte C und D der
        # Gerade durch A und B liegen
        ac = kreux_produkt_Z(self.v, vektor(a, c))
        ad = kreux_produkt_Z(self.v, vektor(a, d))

        # Wenn beide z-Koordinaten positiv bzw. negativ sind, liegen C und D
        # auf der gleichen Seite und die Strecken schneiden sich nicht
        if (ac >= 0 and ad >= 0) or (ac <= 0 and ad <= 0): return False

        # Die Z-Koordinaten der Kreuzprodukte werden berechnet.
        ca = kreux_produkt_Z(andere.v, vektor(c, a))
        cb = kreux_produkt_Z(andere.v, vektor(c, b))

        # Es wird zurück gegeben, ob die Z-Koordinaten unterschiedlich sind
        # bzw. die Punkt A und B auf verschiedenen Seiten liegen
        return (ca > 0 and cb < 0) or (ca < 0 and cb > 0)