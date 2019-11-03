from test_context import ida_lse, _expand
import pytest


def test_mu_scramble_0():
    assert ida_lse(["U", "U", "U", "U", "B", "R", "F", "L", "D", "D", "F", "B"]) == []


def test_mu_scramble_1():
    assert ida_lse(["B", "U", "B", "U", "D", "R", "U", "L", "F", "F", "U", "D"]) == [
        "M"
    ]


def test_mu_scramble_2():
    assert ida_lse(["U", "U", "U", "U", "L", "B", "R", "F", "D", "D", "F", "B"]) == [
        "U"
    ]


def test_mu_expand_0():
    assert (
        len(
            _expand(
                [[["U", "U", "U", "U", "B", "R", "F", "L", "D", "D", "F", "B"], [""]]],
                [],
            )[0]
        )
        == 1
    )


def test_mu_expand_1():
    assert (
        len(
            _expand(
                [
                    [
                        ["B", "U", "B", "U", "D", "R", "U", "L", "F", "F", "U", "D"],
                        ["", "M'"],
                    ],
                    [
                        ["U", "U", "U", "U", "B", "R", "F", "L", "D", "D", "F", "B"],
                        [""],
                    ],
                ],
                [],
            )[1]
        )
        == 8
    )
