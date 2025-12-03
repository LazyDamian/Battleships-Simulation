import numpy as np

def ist_bereich_frei_mit_abstand(feld, z, s, form):
    zeilen, spalten = feld.shape
    z1 = max(0, z - 1)
    s1 = max(0, s - 1)
    z2 = min(zeilen, z + form[0] + 1)
    s2 = min(spalten, s + form[1] + 1)

    # prüft Schiff plus Randring
    return np.all(feld[z1:z2, s1:s2] == 0)



spielfeld = np.zeros((10, 10), dtype=int)
anzahl = {5:1, 4:2, 3:3, 2:4}

def schiffe_platzieren():
    zeilen_feld, spalten_feld = spielfeld.shape

    for länge in sorted(anzahl.keys(), reverse=True):
        nummer = anzahl[länge]
        for i in range(nummer):
            platziert = False


            for richtung in np.random.permutation(["vert", "horiz"]):

                if richtung == "vert":
                    form = (länge, 1)
                else:
                    form = (1, länge)

                mögliche_platzierung = [
                    (z, s)
                    for z in range(zeilen_feld - form[0] + 1)
                    for s in range(spalten_feld - form[1] + 1)
                    if ist_bereich_frei_mit_abstand(spielfeld, z, s, form)]

                if mögliche_platzierung:

                    z, s = mögliche_platzierung[np.random.randint(len(mögliche_platzierung))]
                    if richtung == "vert":
                        spielfeld[z:z + länge, s:s + 1] = länge
                    else:
                        spielfeld[z:z + 1, s:s + länge] = länge
                    platziert = True
                    break

            if not platziert:
                for z in range(zeilen_feld - länge + 1):
                    for s in range(spalten_feld - länge + 1):
                        if np.all(spielfeld[z:z + länge, s:s + 1] == 0):
                            spielfeld[z:z + länge, s:s + 1] = länge
                            platziert = True
                            break
                    if platziert:
                        break

    return spielfeld

spielfeld = schiffe_platzieren()

np.set_printoptions(linewidth=120)
print(spielfeld)