from test_context import ida_lse, _expand
import pytest


def test_mu_scramble_0():
    assert (
        ida_lse(
            [
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
        )
        == []
    )


def test_mu_scramble_1():
    assert ida_lse(
        [
            "B",
            "U",
            "B",
            "U",
            "D",
            "R",
            "U",
            "L",
            "F",
            "F",
            "U",
            "D",
            "B",
            "R",
            "F",
            "L",
            "B",
            "U",
            "F",
            "D",
        ]
    ) == ["M"]


def test_mu_scramble_2():
    assert ida_lse(
        [
            "U",
            "U",
            "U",
            "U",
            "L",
            "B",
            "R",
            "F",
            "D",
            "D",
            "F",
            "B",
            "L",
            "B",
            "R",
            "F",
            "U",
            "F",
            "D",
            "B",
        ]
    ) == ["U"]


def test_mu_scramble_3():
    assert ida_lse(
        [
            "U",
            "B",
            "U",
            "B",
            "R",
            "U",
            "L",
            "D",
            "F",
            "F",
            "U",
            "D",
            "R",
            "F",
            "L",
            "B",
            "B",
            "U",
            "F",
            "D",
        ]
    ) == ["M", "U'"]


def test_mu_scramble_4():
    assert ida_lse(
        [
            "F",
            "U",
            "F",
            "R",
            "U",
            "B",
            "D",
            "U",
            "L",
            "D",
            "U",
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
    ) == ["M'", "U'", "M", "U"]


def test_mu_expand_0():
    assert (
        len(
            _expand(
                [],
                [
                    [
                        [
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
                        ],
                        [""],
                    ]
                ],
            )[0]
        )
        == 1
    )


def test_mu_expand_1():
    assert (
        len(
            _expand(
                [],
                [
                    [
                        [
                            "B",
                            "U",
                            "B",
                            "U",
                            "D",
                            "R",
                            "U",
                            "L",
                            "F",
                            "F",
                            "U",
                            "D",
                            "B",
                            "R",
                            "F",
                            "L",
                            "B",
                            "U",
                            "F",
                            "D",
                        ],
                        ["", "M"],
                    ],
                    [
                        [
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
                        ],
                        [""],
                    ],
                ],
            )[1]
        )
        == 8
    )
