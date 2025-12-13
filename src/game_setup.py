# src/game_setup.py

import numpy as np
import random
from numpy.random import Generator, SeedSequence, PCG64

# Konstanten (sollten in einer eigenen Datei liegen, aber hier zur Übersichtlichkeit)
FELD_GROESSE = (10, 10)  # 10x10 Feld
ANZ_SCHIFFE = {
    5: 1,  # Schlachtschiff
    4: 1,  # Kreuzer
    3: 2,  # Zerstörer
    2: 1  # U-Boot
}


def ist_platz_frei(feld, reihe, spalte, laenge, horizontal):
    """Prüft, ob ein Schiff an der gegebenen Position platziert werden kann."""
    zeilen, spalten = FELD_GROESSE

    if horizontal:
        if spalte + laenge > spalten:
            return False
        # Prüfen auf Überlappung und Abstand
        for s in range(spalte, spalte + laenge):
            # Prüfen des Bereichs inkl. Nachbarn im 3x3 Block um jedes Schiffsteil
            for r_offset in [-1, 0, 1]:
                for s_offset in [-1, 0, 1]:
                    nr, ns = reihe + r_offset, s + s_offset
                    if 0 <= nr < zeilen and 0 <= ns < spalten and feld[nr, ns] != 0:
                        return False
    else:
        if reihe + laenge > zeilen:
            return False
        for r in range(reihe, reihe + laenge):
            for r_offset in [-1, 0, 1]:
                for s_offset in [-1, 0, 1]:
                    nr, ns = r + r_offset, spalte + s_offset
                    if 0 <= nr < zeilen and 0 <= ns < spalten and feld[nr, ns] != 0:
                        return False

    return True


# NEU: Die Funktion nimmt jetzt ein Generator-Objekt entgegen
def erstelle_neues_spielfeld(setup_rng):
    """
    Erstellt ein leeres Spielfeld (0) und platziert die Schiffe.
    """
    feld = np.zeros(FELD_GROESSE, dtype=int)
    zeilen, spalten = FELD_GROESSE

    schiffslaengen = []
    for laenge, anzahl in ANZ_SCHIFFE.items():
        schiffslaengen.extend([laenge] * anzahl)

    # Wir mischen die Längen, damit die Platzierung reproduzierbar ist
    # NEU: Nutzt den lokalen Generator
    schiffslaengen = setup_rng.permutation(schiffslaengen)

    for laenge in schiffslaengen:
        platziert = False
        versuche = 0
        while not platziert and versuche < 1000:
            versuche += 1

            # NEU: Nutzt den lokalen Generator für die Zufallswerte

            # 1. Orientierung: boolsche Werte sind im Generator nicht direkt, daher choice
            ist_horizontal = setup_rng.choice([True, False])

            # 2. Startposition: nutzt integers (ersetzt np.random.randint)
            if ist_horizontal:
                max_r = zeilen - 1
                max_s = spalten - laenge
            else:
                max_r = zeilen - laenge
                max_s = spalten - 1

            reihe = setup_rng.integers(0, max_r + 1)
            spalte = setup_rng.integers(0, max_s + 1)

            if ist_platz_frei(feld, reihe, spalte, laenge, ist_horizontal):
                if ist_horizontal:
                    feld[reihe, spalte:spalte + laenge] = laenge
                else:
                    feld[reihe:reihe + laenge, spalte] = laenge
                platziert = True

        if not platziert:
            raise RuntimeError("Schiff konnte nicht platziert werden. Falsche Konstanten?")

    return feld