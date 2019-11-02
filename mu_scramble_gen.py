"""
States in list should be of form [state, scramble]
Cube and piece naming:
            _____________
            |   | 4 |   |
            |___|___|___|
       _______________________
       |   ||   | 0 |   ||   |
       |___||___|___|___||___|
       | 7 || 3 |   | 1 || 5 |
       |___||___|___|___||___|
       |   ||   | 2 |   ||   |
       |___||___|___|___||___|
            ____________
            |   | 6 |   |
            |___|___|___|
                |   |
                |___|
                | 10|
                |___|
                _____
                | 8 |
                |___|
                |   |
                |___|
                | 9 |
                |___|
                _____
                | 11|
                |___|
"""

import numpy
import random
import sympy.combinatorics.permutations as perm
import sympy.combinatorics.generators as gens


def _generate_mu_moves():
    U = perm.Permutation(11)(1, 2, 3, 0)(5, 6, 7, 4)
    U2 = U * U
    Up = U2 * U

    M = perm.Permutation(0, 6, 8, 11)(2, 10, 9, 4)
    M2 = M * M
    Mp = M2 * M

    return [U, "U"], [U2, "U2"], [Up, "U'"], [M, "M"], [M2, "M2"], [Mp, "M'"]


MOVES = _generate_mu_moves()
SOLVED_CUBE = ["U" * 4, "B", "R", "F", "L", "D" * 2, "F", "B"]


def _expand(frontier, visited):
    new_frontier = []
    for state_scramble in frontier:
        for move_index in range(len(MOVES)):
            new_state_scramble = [
                MOVES[move_index][0](state_scramble[0]),
                state_scramble[1].append(MOVES[move_index][1]),
            ]
            if new_state_scramble[0] not in frontier.union(visited):
                new_frontier.append(new_state_scramble)
    visited = visited.union(frontier)
    frontier = new_frontier
    return visited, frontier


def ida_lse(state):
    visited = frontier = [[state, ""]]
    while True:
        for state_index in range(len(frontier)):
            if SOLVED_CUBE == frontier[state_index][0]:
                return frontier[state_index][1]
        visited, frontier = _expand(frontier, visited)
