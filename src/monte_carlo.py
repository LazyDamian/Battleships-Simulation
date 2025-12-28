import numpy as np
import time
import multiprocessing
from numpy.random import SeedSequence
from concurrent.futures import ProcessPoolExecutor
from typing import Callable, Tuple, List, Dict, Any

# Type alias for the simulation function
SimFunc = Callable[[SeedSequence], int]


def _worker_task(args: Tuple[SimFunc, SeedSequence]) -> int:
    """Helper for process pool execution."""
    func, seq = args
    return func(seed_sequence=seq)


def run_monte_carlo_simulation(
        n_simulations: int,
        sim_function: SimFunc,
        base_seed: int = 42
) -> Dict[str, Any]:
    """
    Executes simulations in parallel using a modern SeedSequence approach.

    Args:
        n_simulations: Number of games to run.
        sim_function: The logic function to execute.
        base_seed: Master seed for reproducibility.

    Returns:
        Statistical metrics of the results.
    """
    print(f"Starting Simulation: {n_simulations} games (Parallel) ...")
    start_time = time.time()
    n_cores = multiprocessing.cpu_count()

    master_seq = SeedSequence(base_seed)
    child_sequences = master_seq.spawn(n_simulations)
    tasks = [(sim_function, seq) for seq in child_sequences]

    with ProcessPoolExecutor(max_workers=n_cores) as executor:
        chunk = max(1, n_simulations // (n_cores * 5))
        results_list = list(executor.map(_worker_task, tasks, chunksize=chunk))

    results = np.array(results_list)
    duration = time.time() - start_time
    print(f"Simulation finished. Duration: {round(duration, 2)}s.")

    return {
        'avg': np.mean(results),
        'median': np.median(results),
        'variance': np.var(results),
        'std_dev': np.std(results),
        'min': np.min(results),
        'max': np.max(results),
        'duration': round(duration, 4),
    }