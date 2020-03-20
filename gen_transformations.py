import sympy.combinatorics.permutations as perm


MU_DICT = {
    0: 1,
    1: 5,
    2: 7,
    3: 3,
    4: 37,
    5: 28,
    6: 19,
    7: 10,
    8: 46,
    9: 52,
    10: 25,
    11: 43,
    12: 38,
    13: 29,
    14: 20,
    15: 11,
    16: 4,
    17: 22,
    18: 49,
    19: 40,
}


def mu_to_full(mu_state):
    full_state = ["U"] * 9 + ["L"] * 9 + ["F"] * 9 + ["R"] * 9 + ["B"] * 9 + ["D"] * 9
    for i in range(20):
        if i in [12, 13, 14, 15]:
            full_state[9 * (16 - i)] = mu_state[i]
            full_state[9 * (16 - i) + 2] = mu_state[i]
        else:
            full_state[MU_DICT.get(i)] = mu_state[i]
    return full_state


def full_to_mu(full_state):
    mu_state = []
    for i in range(20):
        mu_state.append(full_state[MU_DICT.get(i)])
    return mu_state
