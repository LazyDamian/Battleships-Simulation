# main.py

from src.game_logic import simuliere_spiel as simuliere_zufall
from src.monte_carlo import monte_carlo_simulation
from src.game_logic_smart import simuliere_spiel_smart as simuliere_smart

N_SIMULATIONEN = 10000


def main():
    HAUPT_SEED = 42

    # --- Simulationen durchführen ---

    print(f"--- Starte Simulation mit Basis-Seed {HAUPT_SEED} ---\n")

    # 1. Zufallssuche
    print("--- 1. Simulation: ZUFALLSSTRATEGIE ---")
    statistiken_zufall = monte_carlo_simulation(N_SIMULATIONEN, simuliere_zufall, basis_seed=HAUPT_SEED)

    # 2. Strategische KI
    print("\n--- 2. Simulation: STRATEGISCHE KI ---")
    statistiken_smart = monte_carlo_simulation(N_SIMULATIONEN, simuliere_smart, basis_seed=HAUPT_SEED)

    # --- Ausgabe der Ergebnisse ---
    print("\n=======================================================")
    print("                ERGEBNIS VERGLEICH                     ")
    print("=======================================================")

    def r(val): return round(val, 2)

    # Header
    print(f"{'Metrik':<25} | {'Zufallssuche':<25} | {'Strategische KI':<25}")
    print("-" * 80)

    # Daten
    print(
        f"{'Durchschnitt':<25} | {r(statistiken_zufall['Durchschnittliche Schüsse']):<25} | {r(statistiken_smart['Durchschnittliche Schüsse']):<25}")
    print(f"{'Median':<25} | {r(statistiken_zufall['Median']):<25} | {r(statistiken_smart['Median']):<25}")
    print(f"{'Varianz':<25} | {r(statistiken_zufall['Varianz']):<25} | {r(statistiken_smart['Varianz']):<25}")
    print(
        f"{'Standardabweichung':<25} | {r(statistiken_zufall['Standardabweichung']):<25} | {r(statistiken_smart['Standardabweichung']):<25}")

    print("-" * 80)

    # Min und Max als Integer
    print(
        f"{'Minimum Schüsse':<25} | {int(statistiken_zufall['Minimum Schüsse']):<25} | {int(statistiken_smart['Minimum Schüsse']):<25}")
    print(
        f"{'Maximum Schüsse':<25} | {int(statistiken_zufall['Maximum Schüsse']):<25} | {int(statistiken_smart['Maximum Schüsse']):<25}")

    # Fazit
    diff = statistiken_zufall['Durchschnittliche Schüsse'] - statistiken_smart['Durchschnittliche Schüsse']
    print("-" * 80)
    print(f"Verbesserung: Die KI benötigt im Schnitt {r(diff)} Schüsse weniger.")


if __name__ == "__main__":
    main()