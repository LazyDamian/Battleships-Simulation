# main.py

import numpy as np
from src.monte_carlo import monte_carlo_simulation
# NEUE IMPORTE
from src.game_logic import simuliere_spiel as simuliere_zufall
from src.game_logic_smart import simuliere_spiel_smart as simuliere_smart

N_SIMULATIONEN = 10000  # Hohe Zahl für stabile Statistik


def main():
    # 1. Simulation: Zufallsstrategie
    print("--- 1. Starte Simulation: ZUFALLSSTRATEGIE ---")
    # Hier wird die angepasste Funktion aus src/monte_carlo.py verwendet, die die simuliere_funktion erwartet.
    statistiken_zufall = monte_carlo_simulation(N_SIMULATIONEN, simuliere_zufall)

    # 2. Simulation: STRATEGISCHE KI
    print("\n--- 2. Starte Simulation: STRATEGISCHE KI ---")
    statistiken_smart = monte_carlo_simulation(N_SIMULATIONEN, simuliere_smart)

    print("\n=======================================================")
    print("                VERGLEICH DER ERGEBNISSE               ")
    print("=======================================================")

    print(f"Simulationen pro Strategie: {N_SIMULATIONEN}")
    print("-" * 80)

    # NEUE, DETAILLIERTE TABELLE
    print(f"{'Metrik':<25} | {'Zufallssuche':<25} | {'Strategische KI':<25}")
    print("-" * 80)

    def r(val):
        # Hilfsfunktion zum Runden auf zwei Dezimalstellen
        return round(val, 2)

    print(
        f"{'Durchschnittl. Schüsse':<25} | {r(statistiken_zufall['Durchschnittliche Schüsse']):<25} | {r(statistiken_smart['Durchschnittliche Schüsse']):<25}")
    print(f"{'Median Schüsse':<25} | {r(statistiken_zufall['Median']):<25} | {r(statistiken_smart['Median']):<25}")
    print(
        f"{'Standardabweichung':<25} | {r(statistiken_zufall['Standardabweichung']):<25} | {r(statistiken_smart['Standardabweichung']):<25}")

    # HIER KOMMEN DIE NEUEN WERTE:
    print(f"{'Varianz':<25} | {r(statistiken_zufall['Varianz']):<25} | {r(statistiken_smart['Varianz']):<25}")
    print(
        f"{'Maximum Schüsse':<25} | {r(statistiken_zufall['Maximum Schüsse']):<25} | {r(statistiken_smart['Maximum Schüsse']):<25}")
    print(
        f"{'Minimum Schüsse':<25} | {r(statistiken_zufall['Minimum Schüsse']):<25} | {r(statistiken_smart['Minimum Schüsse']):<25}")

    differenz = statistiken_zufall['Durchschnittliche Schüsse'] - statistiken_smart['Durchschnittliche Schüsse']
    print("-" * 80)
    print(
        f"Verbesserung durch KI: {r(differenz)} Schüsse ({r(differenz / statistiken_zufall['Durchschnittliche Schüsse'] * 100)} %)")
    print("-" * 80)


if __name__ == "__main__":
    main()