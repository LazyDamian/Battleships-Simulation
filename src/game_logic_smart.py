import numpy as np
from collections import deque
from numpy.random import Generator, PCG64, SeedSequence
from typing import Tuple, List, Optional, Deque
from .game_setup import create_new_board, SHIP_CONFIG, BOARD_SIZE

# --- STATUS CONSTANTS ---
STATE_UNKNOWN = 0
STATE_MISS = 1
STATE_HIT = 2


def get_neighbors(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    """Returns all 8 surrounding neighbors (3x3 area)."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors


def mark_sunken_ship(r: int, c: int, original_board: np.ndarray, knowledge: np.ndarray) -> bool:
    """Checks if a ship is sunk and marks the surrounding buffer as misses."""
    ship_id = original_board[r, c]
    rows, cols = knowledge.shape

    hits_on_this_ship = np.sum([knowledge[nr, nc] == STATE_HIT
                                for nr, nc in np.argwhere(original_board == ship_id)])

    if hits_on_this_ship == ship_id:
        for nr, nc in np.argwhere(original_board == ship_id):
            for adj_r, adj_c in get_neighbors(nr, nc, rows, cols):
                if knowledge[adj_r, adj_c] == STATE_UNKNOWN:
                    knowledge[adj_r, adj_c] = STATE_MISS
        return True
    return False


def run_smart_simulation(seed_sequence: SeedSequence) -> int:
    """Simulates a game using a smart Hunt & Target strategy."""
    rng = Generator(PCG64(seed_sequence))
    board = create_new_board(rng=rng)

    rows, cols = BOARD_SIZE
    total_targets = np.sum([l * count for l, count in SHIP_CONFIG.items()])

    shots_fired = 0
    hits_count = 0
    knowledge = np.zeros(BOARD_SIZE, dtype=int)
    target_queue: Deque[Tuple[int, int]] = deque()

    while hits_count < total_targets:
        if target_queue:
            r, c = target_queue.popleft()
            if knowledge[r, c] != STATE_UNKNOWN: continue
        else:
            # HUNT MODE: Checkerboard
            r, c = None, None
            unknown_cells = [(ur, uc) for ur in range(rows) for uc in range(cols)
                             if knowledge[ur, uc] == STATE_UNKNOWN]

            for ur, uc in unknown_cells:
                if (ur + uc) % 2 == 0:
                    r, c = ur, uc
                    break

            if r is None and unknown_cells:
                idx = rng.integers(len(unknown_cells))
                r, c = unknown_cells.pop(idx)

            if r is None: break

        shots_fired += 1
        if board[r, c] > 0:
            hits_count += 1
            knowledge[r, c] = STATE_HIT
            if mark_sunken_ship(r, c, board, knowledge):
                target_queue.clear()

            # Add orthogonal neighbors to queue
            for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
                if 0 <= nr < rows and 0 <= nc < cols and knowledge[nr, nc] == STATE_UNKNOWN:
                    target_queue.append((nr, nc))
        else:
            knowledge[r, c] = STATE_MISS

    return shots_fired