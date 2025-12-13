# main.py
from src.monte_carlo import monte_carlo_simulation


def main():
    """Hauptfunktion zur Konfiguration und Ausführung der Simulation."""

    # Konfigurieren Sie hier die Anzahl der Simulationen
    N_SIMULATIONEN = 10000

    statistiken = monte_carlo_simulation(N_SIMULATIONEN)

    print("\n--- Endergebnisse der Monte-Carlo-Simulation ---")
    print("-" * 40)
    for key, value in statistiken.items():
        if isinstance(value, float):
            print(f"{key:<30}: {value:>.4f}")
        else:
            print(f"{key:<30}: {value}")


if __name__ == "__main__":
    main()