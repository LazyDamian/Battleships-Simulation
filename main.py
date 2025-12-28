from src.game_logic import run_random_simulation
from src.game_logic_smart import run_smart_simulation
from src.monte_carlo import run_monte_carlo_simulation
from typing import Dict, Any
import matplotlib.pyplot as plt
import numpy as np
import os

# Set the total number of simulations and the master seed
N_SIMULATIONS = 10000
BASE_SEED = 42


def print_comparison(random_stats: Dict[str, Any], smart_stats: Dict[str, Any]):
    """Prints a comparison table of the simulation results."""
    print("\n" + "=" * 60)
    print(f"{'METRIC':<20} | {'RANDOM STRATEGY':<18} | {'SMART AI':<18}")
    print("-" * 60)

    metrics = [
        ('Average Shots', 'avg'),
        ('Median', 'median'),
        ('Variance', 'variance'),
        ('Std Deviation', 'std_dev')
    ]

    for label, key in metrics:
        print(f"{label:<20} | {random_stats[key]:<18.2f} | {smart_stats[key]:<18.2f}")

    print("-" * 60)
    print(f"{'Minimum Shots':<20} | {int(random_stats['min']):<18} | {int(smart_stats['min']):<18}")
    print(f"{'Maximum Shots':<20} | {int(random_stats['max']):<18} | {int(smart_stats['max']):<18}")
    print("=" * 60)

    improvement = random_stats['avg'] - smart_stats['avg']
    print(f"Summary: The AI is on average {improvement:.2f} shots more efficient.")


def save_histogram(random_data, smart_data, filename="figures/comparison.png"):
    os.makedirs("figures", exist_ok=True)
    plt.figure(figsize=(12, 7))  # Etwas höher für die Beschriftung

    # Durchschnitte berechnen
    avg_random = np.mean(random_data)
    avg_smart = np.mean(smart_data)

    # Bins für diskrete Werte (wie zuvor besprochen)
    all_data = list(random_data) + list(smart_data)
    bins = [i - 0.5 for i in range(int(min(all_data)), int(max(all_data)) + 2)]

    # 1. Die Histogramme zeichnen
    plt.hist(random_data, bins=bins, alpha=0.4, label='Random Strategy', color='red')
    plt.hist(smart_data, bins=bins, alpha=0.5, label='Smart AI', color='blue')

    # 2. Durchschnittslinien einzeichnen (axvline)
    plt.axvline(avg_random, color='red', linestyle='dashed', linewidth=2,
                label=f'Avg Random: {avg_random:.2f}')
    plt.axvline(avg_smart, color='darkblue', linestyle='dashed', linewidth=2,
                label=f'Avg Smart: {avg_smart:.2f}')

    # 3. Text-Labels direkt an die Linien schreiben (optional)
    plt.text(avg_random + 0.5, plt.ylim()[1] * 0.9, f'{avg_random:.2f}', color='red', fontweight='bold')
    plt.text(avg_smart - 3.5, plt.ylim()[1] * 0.9, f'{avg_smart:.2f}', color='darkblue', fontweight='bold')

    # Design-Feinschliff
    plt.title("Comparison: Shots needed to win", fontsize=16)
    plt.xlabel("Number of Shots", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.legend(loc='upper left', frameon=True, shadow=True)
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def main():
    """Main execution flow."""
    print(f"--- Battleship Monte Carlo Analysis (Seed: {BASE_SEED}) ---")

    # 1. Run Simulations
    res_random = run_monte_carlo_simulation(N_SIMULATIONS, run_random_simulation)
    res_smart = run_monte_carlo_simulation(N_SIMULATIONS, run_smart_simulation)

    # 2. Save Visualization
    save_histogram(res_random['raw_data'], res_smart['raw_data'])

    # 3. Print Table
    print_comparison(res_random, res_smart)


if __name__ == "__main__":
    main()

