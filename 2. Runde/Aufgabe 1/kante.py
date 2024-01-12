from math import sqrt


def vektor(a, b):
    """
    Erstellt einen Verktor vom Punkt A zu Punkt B
    :param a: Erster Punkt
    :param b: Zweiter Punkt
    :return: Vektor von Punkt A zu Punkt B
    """
    return b[0] - a[0], b[1] - a[1]


def kreux_produkt_Z(vektor1, vektor2):
    """
    Berechnet nur die Z-Koordiante des Kreuzprodukts zwischen zwei Vektoren
    :param vektor1: Erster Vektor
    :param vektor2: Zweiter Vektor
    :return: Z-Koordinate der Kreuzprodukts
    """
    return vektor1[0] * vektor2[1] - vektor1[1] * vektor2[0]


class Kante:
    """
    Klasse die eine Kante mit den Endpunkten A und B darstellt. Es können
    die Länge und der Punkt in der Mitte der Kante abgefragt werden.
    Zusätzlich kann überprüft werden, ob eine andere Kante geschnitten wird.
    """
    def __init__(self, a, b):
        # Zwei Endpunkte der Kante: A und B
        self.a = a
        self.b = b
        self.v = vektor(a, b)

    def schneidet(self, andere):
        """
        Methode die überprüft, ob diese Kante eine andere Kante schneidet.
        Falls die Kanten gleiche Start- oder Endpunkte haben schneiden sich
        die Kanten nicht.
        :param andere: Andere Kante
        :return: Wahrheitswert, ob eine Kante die andere schneidet
        """
        # Die Endpunkte A und B der eigenen Gerade und die Endpunkte C und D
        # der andere Kante
        a, b = self.a, self.b
        c, d = andere.a, andere.b

        # Falls zwei Punkte unterschiedlicher Kanten gleich sind schneiden
        # sich die Kanten nicht
        if a == c or a == d or b == c or b == d:
            return False

        # Vektoren zwischen den Punkten AB, AC und AD werden berechnet
        ac = vektor(a, c)
        ad = vektor(a, d)

        # Die Z-Koordinaten der Kreuzprodukte werden berechnet. Die Z
        # Koordianten geben an, auf welcher Seite die Punkte C und D der
        # Gerade durch A und B liegen
        ab_ac = kreux_produkt_Z(self.v, ac)
        ab_ad = kreux_produkt_Z(self.v, ad)

        # Wenn C und D auf gleichen Seite der Geraden AB liegen haben beide
        # Kreuzprodukte das selbe Vorzeichen
        cd_gleiche_seiten = (ab_ac > 0 and ab_ad > 0) or \
                            (ab_ac < 0 and ab_ad < 0)

        # Wenn C und D auf der selben Seite liegen kann abgebochen werden,
        # die Kanten schneiden sich nicht
        if cd_gleiche_seiten: return False

        # Vektoren zwischen den Punkten CD CA und CB werden berechnet
        ca = vektor(c, a)
        cb = vektor(c, b)

        # Die Z-Koordinaten der Kreuzprodukte werden berechnet.
        cd_ca = kreux_produkt_Z(andere.v, ca)
        cd_cb = kreux_produkt_Z(andere.v, cb)

        # Wenn A und B auf gleichen Seite der Geraden CD liegen haben beide
        # Kreuzprodukte das selbe Vorzeichen
        ab_gleiche_seiten = (cd_ca > 0 and cd_cb > 0) or \
                            (cd_ca < 0 and cd_cb < 0)

        # Es wird zurückgegeben, ob A und B auf verschiedenen Seiten liegen
        return not ab_gleiche_seiten

    def mitte(self):
        """
        Mitte der Kante wird berechnet
        :return: Mittelpunkt
        """
        # Zur Berechnung werden jeweils die X- und Y-Koordinate der
        # Endpunkte addiret und durch 2 geteilt
        return (self.a[0] + self.b[0]) / 2, (self.a[1] + self.b[1]) / 2

    def laenge(self):
        """
        Länge der Kante wird berechnet
        :return: Länge
        """
        # Die Länge entspricht der Wurzel aus deltax^2 + deltay^2
        return sqrt(self.v[0] ** 2 + self.v[1] ** 2)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b or \
               self.b == other.a and self.a == other.b

    def __repr__(self):
        return str(self.a) + ", " + str(self.b)