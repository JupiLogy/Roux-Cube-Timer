"""
States in list should be of form [state, scramble]
Cube and piece naming:
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
"""

import sympy.combinatorics.permutations as perm


def _generate_mu_moves():
    U = perm.Permutation(19)(1, 2, 3, 0)(5, 6, 7, 4)(12, 13, 14, 15)
    U2 = U * U
    Up = U2 * U

    M = perm.Permutation(0, 6, 8, 11)(2, 10, 9, 4)(16, 17, 18, 19)
    M2 = M * M
    Mp = M2 * M

    return [U, "U"], [U2, "U2"], [Up, "U'"], [M, "M"], [M2, "M2"], [Mp, "M'"]


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


def _expand(visited, frontier):
    print('exploring...')
    new_frontier = []
    for state_scramble in frontier:
        for move_index in range(len(MOVES)):
            new_state_scramble = [
                MOVES[move_index][0](state_scramble[0]),
                [MOVES[move_index][1]] + state_scramble[1],
            ]
            if new_state_scramble[0] not in [
                symmetries(old_state[0]) for old_state in (frontier + visited + new_frontier)
            ]:
                new_frontier.append(new_state_scramble)
    visited = visited + frontier
    frontier = new_frontier
    print(len(visited))
    return visited, frontier


def symmetries(state):
    x_symmetry = perm.Permutation(19)(1, 3)(5, 7)(13, 15)
    y_symmetry = perm.Permutation(0, 2)(4, 6)(8, 9)(10, 11)(17, 19)

    def x_flip(state):
        for piece in state:
            if piece == 'R':
                piece = 'L'
            elif piece == 'L':
                piece = 'R'
        return state

    def y_flip(state):
        for piece in state:
            if piece == 'F':
                piece = 'B'
            elif piece == 'B':
                piece = 'F'
        return state

    x_state = x_symmetry(x_flip(state))
    y_state = y_symmetry(y_flip(state))
    xy_state = x_symmetry(y_symmetry(state))

    return state, x_state, y_state, xy_state


def ida_lse(state):
    visited = frontier = [[state, [""]]]
    while True:
        for state_index in range(len(frontier)):
            if SOLVED_CUBE == frontier[state_index][0]:
                return frontier[state_index][1][:-1]
        visited, frontier = _expand(visited, frontier)
