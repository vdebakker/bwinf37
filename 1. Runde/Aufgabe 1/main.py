''' Einlesen der Datei '''

ausgabe_datei = "dialog.txt"
fobj_out = open(ausgabe_datei, "w")

eingabe_datei = "superstar.txt"

# Liste mit Zeilen der Eingabe
eingabe = [zeile.split(" ") for zeile in open(eingabe_datei, "r").readlines()]

# Liste mit allen Namen, die in der ersten Zeile der Eingabe stehen
namen = [name.strip() for name in eingabe[0]]

# Bestimmung der Spaltenbreite zur formatierten Ausgabe
max_laenge = max([len(name) for name in namen])
spaltenbreite = 2*max_laenge + 15

# Dictionary mit Namen als Key und
# Set mit Namen, denen die erste Person folgt, als Value
folgt = {name: set() for name in namen}
for beziehung in eingabe[1:]:
    # Erster Name der Zeile folgt zweitem Namen und wird in Dictionary
    # gespeichert
    folgt[beziehung[0]].add(beziehung[1].strip())


''' 1.Phase: Eingrenzen der möglichen Superstars auf eine Person '''

# Zu Beginn könnten alle Personen Superstar sein, keine Person kann
# ausgeschlossen werden
moeglich = set(namen)

# Set mit Tupeln von Paaren, die bereits getestet wurden
getestet = set()

# Solange es mehr als eine mögliche Person gibt
while len(moeglich) > 1:

    # Zwei zufällige unterschiedliche Personen werden aus Set entfernt
    erste_person = moeglich.pop()
    zweite_person = moeglich.pop()

    # Abfrage
    print("Folgt %s %s?" % (erste_person, zweite_person))
    ausgabe = ("Folgt %s %s?" % (erste_person, zweite_person))
    fobj_out.write(("{0:"+str(spaltenbreite)+"}").format(ausgabe))
    getestet.add((erste_person, zweite_person))
    if zweite_person in folgt[erste_person]:
        print("Ja")
        fobj_out.write("Ja\n")
        # Erste Person folgt der zweiten Person und kann kein Superstar sein
        # Die zweite Person kann aber immer noch Superstar sein
        moeglich.add(zweite_person)
    else:
        print("Nein")
        fobj_out.write("Nein\n")
        # Zweite Person folgt der ersten Person und kann kein Superstar sein
        # Die erste Person kann aber immer noch Superstar sein
        moeglich.add(erste_person)

''' 2.Phase: Überprüfen der letzten Person '''

# Letzte Person, die noch Superstar sein könnte
superstar_kandidat = moeglich.pop()

superstar = True  # Boolean, ob Kandidat aus Phase 1 Superstar ist
i = 0
while superstar and i < len(namen):
    andere_person = namen[i]  # Andere Person, die überprüft werden muss
    if andere_person != superstar_kandidat:
        # Andere Person ist nicht gleichzeitig Superstar-Kandidat

        if(andere_person, superstar_kandidat) not in getestet:
            # Kombination noch nicht getestet
            # Abfrage
            print("Folgt %s %s?" % (andere_person, superstar_kandidat))
            ausgabe = ("Folgt %s %s?" % (andere_person, superstar_kandidat))
            fobj_out.write(("{0:"+str(spaltenbreite)+"}").format(ausgabe))
            if superstar_kandidat in folgt[andere_person]:
                print("Ja")
                fobj_out.write("Ja\n")
            else:  # Letzte Person kann kein Superstar sein
                print("Nein")
                fobj_out.write("Nein\n")
                superstar = False
                break

        if (superstar_kandidat, andere_person) not in getestet:
            # Kombination noch nicht getestet
            # Abfrage
            print("Folgt %s %s?" % (superstar_kandidat, andere_person))
            ausgabe = ("Folgt %s %s?" % (superstar_kandidat, andere_person))
            fobj_out.write(("{0:"+str(spaltenbreite)+"}").format(ausgabe))
            if andere_person in folgt[superstar_kandidat]:
                # superstar_kandidat kann kein Superstar sein
                print("Ja")
                fobj_out.write("Ja\n")
                superstar = False
            else:
                print("Nein")
                fobj_out.write("Nein\n")
    i += 1

''' Ergebnis ausgeben '''

# Ergebnis wird ausgegeben
if superstar:
    print(superstar_kandidat + " ist ein Superstar!")
    fobj_out.write("\n" + superstar_kandidat + " ist ein Superstar!\n")
else:
    print("Es gibt keinen Superstar")
    fobj_out.write("\nEs gibt keinen Superstar")

fobj_out.close()