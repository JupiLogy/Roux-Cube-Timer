from test_context import full_to_mu, mu_to_full
import pytest
import random


def test_full_to_mu_0():
    assert full_to_mu(["U"] * 9 + ["L"] * 9 + ["F"] * 9 + ["R"] * 9 + ["B"] * 9 + ["D"] * 9) == [
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


def test_mu_to_full_0():
    assert mu_to_full([
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
    ]) == ["U"] * 9 + ["L"] * 9 + ["F"] * 9 + ["R"] * 9 + ["B"] * 9 + ["D"] * 9


def test_gen_transformations_generic():
    for test_no in range(3):
        mu_state = []
        full_state = ["U"] * 9 + ["L"] * 9 + ["F"] * 9 + ["R"] * 9 + ["B"] * 9 + ["D"] * 9
        for mu_pieces in range(20):
            mu_state.append(random.choice(["U", "F", "L", "R", "B", "D"]))
        for full_pieces in [1, 3, 4, 5, 7, 9, 10, 18, 19, 27, 28, 36, 37, 22, 25, 40, 43, 46, 49, 52]:
            full_state[full_pieces] = random.choice(["U", "F", "L", "R", "B", "D"])
        for dupe_full_pieces in [9, 18, 27, 36]:
            full_state[dupe_full_pieces + 2] = full_state[dupe_full_pieces]

        assert mu_state == full_to_mu(mu_to_full(mu_state))
        assert full_state == mu_to_full(full_to_mu(full_state))
