"""
    States in list should be of form [state, scramble]
    Cube and piece naming for generator:
                _____________
                | 12| 4 |   |
                |___|___|___|
           _______________________
           |   ||   | 0 |   || 13|
           |___||___|___|___||___|
           | 7 || 3 | 16| 1 || 5 |
           |___||___|___|___||___|
           | 15||   | 2 |   ||   |
           |___||___|___|___||___|
                ____________
                |   | 6 | 14|
                |___|___|___|
                    | 17|
                    |___|
                    | 10|
                    |___|
                    _____
                    | 8 |
                    |___|
                    | 18|
                    |___|
                    | 9 |
                    |___|
                    _____
                    | 11|
                    |___|
                    | 19|
                    |___|

    Cube and piece naming for pruning table:
                _____________
                |   | 4 |   |
                |___|___|___|
           _______________________
           |   ||   | 0 |   ||   |
           |___||___|___|___||___|
           | 7 || 3 | 11| 1 || 5 |
           |___||___|___|___||___|
           |   ||   | 2 |   ||   |
           |___||___|___|___||___|
                ____________
                |   | 6 | 10|
                |___|___|___|
                    |   |
                    |___|
                    | 9 |
                    |___|
                    _____
                    | 8 |
                    |___|
                    |   |
                    |___|
                    |   |
                    |___|
                    _____
                    |   |
                    |___|
                    |   |
                    |___|

"""

import sympy.combinatorics.permutations as perm
from progress.bar import Bar

                 # 0, 1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11
p_state_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 16]


def _get_p_state(state):
    return ''.join([state[x] for x in p_state_indices])


def _generate_mu_moves():
    U = perm.Permutation(19)(1, 2, 3, 0)(5, 6, 7, 4)(12, 13, 14, 15)
    U2 = U * U
    Up = U2 * U

    M = perm.Permutation(0, 6, 8, 11)(2, 10, 9, 4)(16, 17, 18, 19)
    M2 = M * M
    Mp = M2 * M

    return [U, U2, Up, M, M2, Mp]


MOVES = _generate_mu_moves()
SOLVED_CUBE = [
    "U",
    "U",
    "U",
    "U",
    "B",
    "R",
    "F",
    "L",
    "D",
    "D",
    "F",
    "B",
    "B",
    "R",
    "F",
    "L",
    "U",
    "F",
    "D",
    "B",
]

p_tab = {_get_p_state(SOLVED_CUBE): 0}

depth = 0
frontier = [SOLVED_CUBE]

bar = Bar('Generating MU scrambles...', max = 20)
while frontier != []:
    old_frontier = frontier.copy()
    frontier = []

    depth += 1

    for state in old_frontier:
        for move in MOVES:
            if _get_p_state(move(state)) not in p_tab:
                p_tab[_get_p_state(move(state))] = depth
                frontier.append(move(state))
    bar.next()
bar.finish()
