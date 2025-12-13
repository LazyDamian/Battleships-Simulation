# src/game_logic.py

import numpy as np
import random
from numpy.random import Generator, SeedSequence, PCG64  # NEU
from .game_setup import erstelle_neues_spielfeld, ANZ_SCHIFFE, FELD_GROESSE


# NEU: Erwartet das SeedSequence Objekt
def simuliere_spiel(seed_sequence):
    # 1. Erzeuge lokalen Generator
    rng = Generator(PCG64(seed_sequence))

    # 2. Feld erstellen (übergibt den Generator)
    feld = erstelle_neues_spielfeld(setup_rng=rng)

    spielfeld_zum_beschuss = np.copy(feld)
    gesamte_schiffsteile = np.sum([länge * ANZ_SCHIFFE[länge] for länge in ANZ_SCHIFFE])
    schüsse = 0
    treffer_zaehler = 0

    zeilen, spalten = FELD_GROESSE
    alle_koordinaten = [(z, s) for z in range(zeilen) for s in range(spalten)]

    # NEU: Mischen der Koordinaten über den Generator
    alle_koordinaten = list(rng.permutation(alle_koordinaten))

    while treffer_zaehler < gesamte_schiffsteile:
        if not alle_koordinaten: break

        z, s = alle_koordinaten.pop()
        schüsse += 1

        if spielfeld_zum_beschuss[z, s] > 0:
            treffer_zaehler += 1

    return schüsse