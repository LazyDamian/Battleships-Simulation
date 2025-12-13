# src/monte_carlo.py (AKTUALISIERTE VERSION)

import numpy as np
import time
# Wir importieren simuliere_spiel NICHT MEHR HIER, sondern übergeben es!
from .game_setup import ANZ_SCHIFFE, FELD_GROESSE


# Die Funktion akzeptiert jetzt 'simulations_funktion' als Argument
def monte_carlo_simulation(anzahl_simulationen, simulations_funktion):
    """
    Führt die Monte-Carlo-Simulation durch und berechnet die Statistiken.

    :param anzahl_simulationen: Die Anzahl der Spiele, die simuliert werden sollen (N).
    :param simulations_funktion: Die Funktion (z.B. simuliere_spiel), die die Logik enthält.
    :return: Ein Dictionary mit den berechneten Statistiken.
    """
    print(f"Starte Monte-Carlo-Simulation mit {anzahl_simulationen} Spielen...")
    start_zeit = time.time()

    ergebnisse = []

    for i in range(anzahl_simulationen):
        # Rufe die übergebene Logik des Einzelspiels auf
        ergebnis = simulations_funktion()  # <-- HIER IST DIE ÄNDERUNG!
        ergebnisse.append(ergebnis)

        # Fortschrittsanzeige
        # ... (Rest der Fortschrittsanzeige bleibt) ...
        if (i + 1) % (anzahl_simulationen // 10 if anzahl_simulationen >= 10 else 1) == 0:
            print(f"  ... {i + 1} von {anzahl_simulationen} Spielen abgeschlossen.")

    ergebnisse_array = np.array(ergebnisse)

    statistiken = {
        "N_Simulationen": anzahl_simulationen,
        "Gesamte Schiffsteile": np.sum([l * ANZ_SCHIFFE[l] for l in ANZ_SCHIFFE]),
        "Feldgröße": f"{FELD_GROESSE[0]}x{FELD_GROESSE[1]}",
        "Durchschnittliche Schüsse": np.mean(ergebnisse_array),
        "Varianz": np.var(ergebnisse_array),
        "Standardabweichung": np.std(ergebnisse_array),
        "Median": np.median(ergebnisse_array),
        "Minimum Schüsse": np.min(ergebnisse_array),
        "Maximum Schüsse": np.max(ergebnisse_array),
    }

    end_zeit = time.time()
    statistiken["Simulationsdauer (Sekunden)"] = end_zeit - start_zeit

    return statistiken