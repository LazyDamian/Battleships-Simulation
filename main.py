from src.game_logic import run_random_simulation
from src.game_logic_smart import run_smart_simulation
from src.monte_carlo import run_monte_carlo_simulation
from typing import Dict, Any

N_SIMULATIONS = 10000
BASE_SEED = 42


def print_comparison(random_stats: Dict[str, Any], smart_stats: Dict[str, Any]) -> None:
    """Prints a formatted comparison table."""
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
    print(f"Result: The AI is on average {improvement:.2f} shots more efficient.")


def main():
    print(f"--- Battleship Monte Carlo (Seed: {BASE_SEED}) ---")

    # 1. Random Strategy
    random_results = run_monte_carlo_simulation(N_SIMULATIONS, run_random_simulation, BASE_SEED)

    # 2. Smart AI
    smart_results = run_monte_carlo_simulation(N_SIMULATIONS, run_smart_simulation, BASE_SEED)

    print_comparison(random_results, smart_results)


if __name__ == "__main__":
    main()