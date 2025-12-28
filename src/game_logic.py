import numpy as np
from numpy.random import Generator, PCG64, SeedSequence
from typing import List, Tuple
from .game_setup import create_new_board, SHIP_CONFIG, BOARD_SIZE


def run_random_simulation(seed_sequence: SeedSequence) -> int:
    """
    Simulates a game using a purely random shooting strategy.

    Args:
        seed_sequence: SeedSequence for the local generator.

    Returns:
        Total number of shots fired to sink all ships.
    """
    rng = Generator(PCG64(seed_sequence))
    board = create_new_board(rng=rng)

    total_targets = np.sum([l * count for l, count in SHIP_CONFIG.items()])
    shots_fired = 0
    hits_count = 0

    rows, cols = BOARD_SIZE
    coordinates = [(r, c) for r in range(rows) for c in range(cols)]
    coordinates = list(rng.permutation(coordinates))

    while hits_count < total_targets:
        if not coordinates: break
        r, c = coordinates.pop()
        shots_fired += 1

        if board[r, c] > 0:
            hits_count += 1

    return shots_fired