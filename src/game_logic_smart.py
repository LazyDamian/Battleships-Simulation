# src/game_logic_smart.py (STRATEGISCHE KI - MODERNISIERT FÜR SEEDSEQUENCE)

import numpy as np
import time
from collections import deque
from numpy.random import Generator, SeedSequence, PCG64
from .game_setup import erstelle_neues_spielfeld, ANZ_SCHIFFE, FELD_GROESSE

# --- KONSTANTEN ---
STATUS_UNBEKANNT = 0
STATUS_WASSER = 1
STATUS_TREFFER = 2


# --- HILFSFUNKTIONEN ---

def get_nachbarn(z, s, zeilen, spalten):
    """Gibt alle acht umliegenden Nachbarn (inkl. Diagonalen) zurück."""
    nachbarn = []
    for dz in [-1, 0, 1]:
        for ds in [-1, 0, 1]:
            # Die Position selbst überspringen
            if dz == 0 and ds == 0:
                continue
            nz, ns = z + dz, s + ds
            if 0 <= nz < zeilen and 0 <= ns < spalten:
                nachbarn.append((nz, ns))
    return nachbarn


def markiere_versenktes_schiff(z_start, s_start, spielfeld_original, ki_status):
    """
    Prüft, ob das Schiff, das an (z_start, s_start) getroffen wurde, versenkt ist.
    Wenn ja, markiert es den Abstand als Wasser (STATUS_WASSER).
    """
    schiffs_laenge = spielfeld_original[z_start, s_start]
    zeilen, spalten = ki_status.shape

    # Zähle alle Treffer auf den Teilen dieses Schiffstyps
    # Dies funktioniert, da die Schiffs-IDs der Länge entsprechen
    treffer_zaehler = np.sum([ki_status[z, s] == STATUS_TREFFER
                              for z, s in np.argwhere(spielfeld_original == schiffs_laenge)])

    if treffer_zaehler == schiffs_laenge:
        # Schiff ist versenkt: Markiere das umgebende 3x3 Raster jedes Teils als Wasser
        for z_schiff, s_schiff in np.argwhere(spielfeld_original == schiffs_laenge):
            for nz, ns in get_nachbarn(z_schiff, s_schiff, zeilen, spalten):
                if ki_status[nz, ns] == STATUS_UNBEKANNT:
                    ki_status[nz, ns] = STATUS_WASSER
        return True

    return False


# --- HAUPTSIMULATION ---

# NEU: Erwartet das SeedSequence-Objekt (Standardisierung)
def simuliere_spiel_smart(seed_sequence):
    """
    Simuliert ein Schiffe-Versenken-Spiel mit der strategischen KI (Jagd/Ziel-Modus).
    """

    # 1. Erzeuge lokalen Generator aus der übergebenen SeedSequence
    rng = Generator(PCG64(seed_sequence))

    # 2. Feld erstellen (übergibt den Generator)
    feld = erstelle_neues_spielfeld(setup_rng=rng)

    zeilen, spalten = FELD_GROESSE
    spielfeld_original = np.copy(feld)
    spielfeld_zum_beschuss = np.copy(
        feld)  # Kopie wird benötigt, um getroffene Teile zu "entfernen" (wenn nötig, aber hier nicht verwendet)
    gesamte_schiffsteile = np.sum([länge * ANZ_SCHIFFE[länge] for länge in ANZ_SCHIFFE])

    schüsse = 0
    treffer_zaehler = 0

    # ki_status speichert den aktuellen Wissenstand der KI
    ki_status = np.zeros(FELD_GROESSE, dtype=int)
    # ziel_warteschlange speichert Koordinaten, die nach einem Treffer in der Nähe beschossen werden sollen
    ziel_warteschlange = deque()

    while treffer_zaehler < gesamte_schiffsteile:

        # --- BESTIMMEN DES NÄCHSTEN SCHUSSES (Jagd/Ziel) ---
        if ziel_warteschlange:
            # ZIELMODUS
            z, s = ziel_warteschlange.popleft()
            if ki_status[z, s] != STATUS_UNBEKANNT:
                continue  # Bereits beschossen, überspringen
        else:
            # JAGDMODUS (Checkerboard-Strategie)
            z, s = None, None
            alle_unbekannten = [(z_unk, s_unk)
                                for z_unk in range(zeilen)
                                for s_unk in range(spalten)
                                if ki_status[z_unk, s_unk] == STATUS_UNBEKANNT]

            # 1. Suche nach Checkerboard-Positionen
            for z_jagd, s_jagd in alle_unbekannten:
                if (z_jagd + s_jagd) % 2 == 0:
                    z, s = z_jagd, s_jagd
                    break

            # 2. Fallback: Wenn alle Checkerboard-Positionen weg sind, wähle zufällig aus dem Rest
            if z is None and alle_unbekannten:
                # NEU: Nutzt den lokalen Generator (ersetzt np.random.randint)
                zufalls_index = rng.integers(len(alle_unbekannten))
                z, s = alle_unbekannten.pop(zufalls_index)

            if z is None: break  # Spiel ist theoretisch vorbei, falls die Schleife nicht greift

        # --- SCHUSS AUSFÜHREN ---
        schüsse += 1

        if spielfeld_original[z, s] > 0:
            # TREFFER!
            treffer_zaehler += 1
            ki_status[z, s] = STATUS_TREFFER

            # Prüfen, ob das Schiff versenkt wurde
            if markiere_versenktes_schiff(z, s, spielfeld_original, ki_status):
                # Wenn versenkt, leere die Warteschlange, um mit der Jagd fortzufahren
                ziel_warteschlange.clear()

            # Füge die umliegenden (unbeschossenen) orthogonalen Nachbarn der Warteschlange hinzu
            for nz, ns in [(z + 1, s), (z - 1, s), (z, s + 1), (z, s - 1)]:
                if 0 <= nz < zeilen and 0 <= ns < spalten and ki_status[nz, ns] == STATUS_UNBEKANNT:
                    ziel_warteschlange.append((nz, ns))

        else:
            # WASSER
            ki_status[z, s] = STATUS_WASSER

    # Gibt nur die Gesamtzahl der Schüsse zurück
    return schüsse