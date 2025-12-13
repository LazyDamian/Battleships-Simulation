# src/monte_carlo.py (BEREINIGTE PARALLELE VERSION)

import numpy as np
import time
from numpy.random import SeedSequence, PCG64, Generator
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from .game_setup import ANZ_SCHIFFE, FELD_GROESSE


# --- HILFSFUNKTION FÜR DEN POOL (Bleibt unverändert) ---
def _simuliere_einzelspiel(args):
    """
    Hilfsfunktion, die ein einzelnes Spiel ausführt.
    Args: (simulations_funktion, spiel_seed_sequence)
    Returns: Schüsse
    """
    simulations_funktion, spiel_seed_sequence = args
    return simulations_funktion(seed_sequence=spiel_seed_sequence)


def monte_carlo_simulation(anzahl_simulationen, simulations_funktion, basis_seed=42):
    # 1. Nur die Essenz ausgeben
    print(f"Starte Simulation: {anzahl_simulationen} Spiele  ...")
    start_zeit = time.time()

    ANZ_PROZESSE = multiprocessing.cpu_count()

    # 1. Erzeuge die Haupt-Sequenz und die Unter-Sequenzen
    haupt_sequenz = SeedSequence(basis_seed)
    kind_sequenzen = haupt_sequenz.spawn(anzahl_simulationen)

    # 2. Erstelle die Liste der Argumente für jeden Prozess
    aufgaben = [(simulations_funktion, seq) for seq in kind_sequenzen]

    # --- Fortschrittsanzeige initialisieren ---
    ergebnisse = []
    chunksize = max(1, anzahl_simulationen // (ANZ_PROZESSE * 5))  # Chunk von 5 mal der Kernanzahl

    # --- PARALLELISIERUNG START ---
    with ProcessPoolExecutor(max_workers=ANZ_PROZESSE) as executor:

        # Nutzen von executor.map und Speichern des Ergebnisses
        # map gibt einen Iterator zurück, wir wandeln ihn in eine Liste um
        future_map = executor.map(_simuliere_einzelspiel, aufgaben, chunksize=chunksize)

        # Manuelle Fortschrittsanzeige für parallele Ausführung
        counter = 0
        n_schritte = max(10,
                         anzahl_simulationen // 1000)  # Ein Schritt pro 1000 Simulationen oder mindestens 10 Schritte

        for ergebnis in future_map:
            ergebnisse.append(ergebnis)
            counter += 1

            # Ausgabe alle 10% der Simulationen
            if counter % (anzahl_simulationen // n_schritte) == 0:
                prozent = round((counter / anzahl_simulationen) * 100)
                print(f"  ... {counter} von {anzahl_simulationen} Spielen abgeschlossen ({prozent}%)")

    # --- PARALLELISIERUNG ENDE ---

    ergebnisse_array = np.array(ergebnisse)
    simulations_dauer = time.time() - start_zeit

    print(f"  ... 100% abgeschlossen. Dauer: {round(simulations_dauer, 2)}s.")  # Abschließende Meldung

    # Statistik
    statistiken = {
        'Durchschnittliche Schüsse': np.mean(ergebnisse_array),
        'Median': np.median(ergebnisse_array),
        'Varianz': np.var(ergebnisse_array),
        'Standardabweichung': np.std(ergebnisse_array),
        'Minimum Schüsse': np.min(ergebnisse_array),
        'Maximum Schüsse': np.max(ergebnisse_array),
        'Simulationsdauer': round(simulations_dauer, 4),
    }

    return statistiken