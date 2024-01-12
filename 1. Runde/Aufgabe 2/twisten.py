import io
from random import randint

def twisten(wort):
    """ Funktion die ein gegebenes Wort twistet """

    wort = list(wort)  # Wort wird zu Liste von Buchstaben
    for i in range(1, len(wort) - 1):
        # Alle Buchstaben außer der erste und der letzte Buchstabe werden
        # einmal mit einem zufälligen Buchstaben getauscht
        zufallszahl = randint(i, len(wort) - 2)
        wort[i], wort[zufallszahl] = wort[zufallszahl], wort[i]
    return "".join(wort)  # Fertiges Wort wird zurückgegeben


datei = "twist.txt"  # Name der Eingabe Datei
# Ausgabe wird geöffnet
ausgabe = io.open("getwistet.txt", mode="w", encoding='utf-8')
# Set mit allen Buchstaben des Alphabets
alphabet = set("abcdefghijklmnopqrstuvwxyzäöüßABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ")
# Gesamter zu twistender Text
text = io.open(datei, mode="r", encoding='utf-8').read()
neuer_text = ""  # Variable für den neuen Text

# Alle Zeichen des Textes werden durchgegangen
i = 0
while i < len(text):
    # Wort wird gesucht, solange die Zeichen im Alphabet sind gehören sie
    # zum Wort und werden dem Wort angehängt
    wort = ""
    while i < len(text) and text[i] in alphabet:
        wort += text[i]
        i += 1
    # Dem neuen Text wird das getwistete Wort angehängt
    neuer_text += twisten(wort)

    # Solange Zeichen nicht im Alphabet sind, werden sie einfach dem Text
    # angehängt
    while i < len(text) and text[i] not in alphabet:
        neuer_text += text[i]
        i += 1
print(neuer_text, file=ausgabe, end="")  # Fertiger Text wird gespeichert
