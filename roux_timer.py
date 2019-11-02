"""
    https://github.com/JupiLogy/Roux-Cube-Timer/

    Cube:
                      ----------------
                      | 0  | 1  | 2  |
                      ----------------
                      | 3  | 4  | 5  |
                      ----------------
                      | 6  | 7  | 8  |
                      ----------------
    ----------------  ----------------  ----------------  ----------------
    | 9  | 10 | 11 |  | 18 | 19 | 20 |  | 27 | 28 | 29 |  | 36 | 37 | 38 |
    ----------------  ----------------  ----------------  ----------------
    | 12 | 13 | 14 |  | 21 | 22 | 23 |  | 30 | 31 | 32 |  | 39 | 40 | 41 |
    ----------------  ----------------  ----------------  ----------------
    | 15 | 16 | 17 |  | 24 | 25 | 26 |  | 33 | 34 | 35 |  | 42 | 43 | 44 |
    ----------------  ----------------  ----------------  ----------------
                      ----------------
                      | 45 | 46 | 47 |
                      ----------------
                      | 48 | 49 | 50 |
                      ----------------
                      | 51 | 52 | 53 |
                      ----------------
    U = [0,8]
    L = [9,17]
    F = [18,26]
    R = [27,35]
    B = [36,44]
    D = [45,53]

    Kociemba solver needs the following cubies at place:
    4 (Upper center)    : YELLOW
    13 (Left center)    : BLUE
    22 (Front center)    : RED
    31 (Right center)    : GREEN
    40 (Back center)    : ORANGE
    49 (Down center)    : WHITE
"""

import random
from tkinter.colorchooser import askcolor
import numpy as np
import sympy.combinatorics.permutations as perm
import sympy.combinatorics.generators as gens
from tkinter import *
from rubik_solver import utils

COLOUR_NAMES = ["Y", "B", "R", "G", "O", "W"]
FACE_DICT = {"U": "Y", "L": "B", "F": "R", "R": "G", "B": "O", "D": "W"}

DEFAULT_CUBE = perm.Permutation(53)
SOLVED_CUBE = []
for colour in COLOUR_NAMES:
    for cubie in range(9):
        SOLVED_CUBE.append(colour)

DEFAULT_PERM = perm.Permutation(53)


def generate_moves():
    """ This function generates the permutations representing the moves of faces
        or slices performed on the cube, eg. U, F', M2. These permutations can
        then be applied to a generated cube.
    """
    y2 = DEFAULT_CUBE
    M2 = DEFAULT_CUBE
    M = DEFAULT_CUBE
    Mp = DEFAULT_CUBE
    U = DEFAULT_CUBE
    U2 = DEFAULT_CUBE
    Up = DEFAULT_CUBE

    for cubelet in range(9):
        y2 = y2 * perm.Permutation(cubelet, cubelet + 45)  # Swaps U and D faces
    for cubelet in range(4):
        y2 = y2 * perm.Permutation(cubelet + 27, 35 - cubelet)  # Rotates R face
        y2 = y2 * perm.Permutation(cubelet + 9, 17 - cubelet)  # Rotates L face
    for cubelet in range(3):
        y2 = y2 * perm.Permutation(cubelet + 18, 44 - cubelet)  # Puts FU* to BD*
        y2 = y2 * perm.Permutation(cubelet + 21, 41 - cubelet)  # Puts FE* to BE*
        y2 = y2 * perm.Permutation(cubelet + 24, 38 - cubelet)  # Puts FD* to BU*

    for cubelet in [1, 4, 7]:
        M = M * perm.Permutation(
            cubelet, 44 - cubelet, cubelet + 45, cubelet + 18
        )  # UM -> FM -> DM -> BM

    U = perm.Permutation(53)(0, 2, 8, 6)(1, 5, 7, 3)  # Rotates U face
    for cubelet in [9, 10, 11]:
        U = U * perm.Permutation(
            cubelet, cubelet + 9, cubelet + 18, cubelet + 27
        )  # FU -> LU -> BU -> RU

    M2 = M * M
    Mp = M2 * M

    U2 = U * U
    Up = U2 * U

    return [y2, M, M2, Mp, U, U2, Up]


def generate_groups():
    alternating_6 = list(gens.alternating(6))
    odd_6 = [x for x in list(gens.symmetric(6)) if x not in alternating_6]
    return alternating_6, odd_6


y2, M, M2, Mp, U, U2, Up = generate_moves()
a_6, o_6 = generate_groups()


class RouxTimer:
    def __init__(self):

        self.win = Tk()
        self.win.geometry("450x190+400+200")
        self.win.title("RouxTimer")

        self.left_win = Frame(self.win, borderwidth=1, relief="solid", width=50)
        self.right_win = Frame(self.win, borderwidth=0, relief="solid")

        self.cube_space = Canvas(self.left_win, height=130, width=170, bg="#aaaaaa")
        self.solved_cube_button = Button(
            self.left_win, text="Show solved cube", command=self.reset_cube
        )
        self.scramble_button = Button(
            self.right_win, text="LSE", command=self.LSE_scramble
        )

        self.change_scheme_button = Button(
            self.left_win, text="Change colour scheme", command=self.change_scheme
        )
        self.colour_colours = [
            "#ffff00",
            "#2222ff",
            "#ff0000",
            "#00ff00",
            "#ffa500",
            "#ffffff",
        ]
        self.update_colour_dict()

        self.scramble = StringVar()

        self.left_win.pack(side="left", fill="y")
        self.right_win.pack(side="right", expand=True, fill="both")

        self.cube_space.pack()
        Label(self.right_win, textvariable=self.scramble).pack()
        self.scramble_button.pack()
        self.solved_cube_button.pack()
        self.change_scheme_button.pack()

        self.reset_cube()  # Generates solved self.cube
        self.print_cube()
        mainloop()

    def reset_cube(self):
        self.cube = SOLVED_CUBE
        self.print_cube()

    def change_particular_colour(self, face):
        c = FACE_DICT.get(face)
        for idx, name in enumerate(COLOUR_NAMES):
            if c == name:
                self.colour_colours[idx] = askcolor(
                    initialcolor=self.colour_colours[idx],
                    title="Set %s face colour for LSE" % (face),
                )[1]
                self.update_colour_dict()
                self.print_cube()
                self.colour_win.destroy()
                self.change_scheme()

    def update_colour_dict(self):
        self.colour_dict = {
            "Y": self.colour_colours[0],
            "B": self.colour_colours[1],
            "R": self.colour_colours[2],
            "G": self.colour_colours[3],
            "O": self.colour_colours[4],
            "W": self.colour_colours[5],
        }

    def change_scheme(self):
        self.colour_win = Tk()
        self.colour_win.geometry("300x200+450+250")
        self.colour_win.title("Edit Colour Scheme | RouxTimer")
        colour_canv = Canvas(self.colour_win, height=130, width=170, bg="#aaaaaa")
        colour_canv.pack()
        self.reset_cube()
        for bn in self.generic_print_cube(colour_canv, 30, 0, 0):
            colour_canv.tag_bind(
                bn[0], "<ButtonPress-1>", lambda _: self.change_particular_colour(bn[1])
            )

    def LSE_scramble(self):
        self.cube = SOLVED_CUBE
        corners = random.choice(range(4))
        if corners == 1 or corners == 3:
            permn = random.choice(o_6)
        else:
            permn = random.choice(a_6)
        flip = random.choice(range(4))
        orient = random.sample(range(6), flip * 2)
        m2 = random.choice(range(2))
        LSE_pieces = np.array([[1, 37], [3, 10], [7, 19], [5, 28], [46, 25], [52, 43]])
        LSE_pieces_new = LSE_pieces
        for i in orient:
            LSE_pieces_new[i] = perm.Permutation(0, 1)(LSE_pieces[i])
        LSE_pieces_new = permn(LSE_pieces_new)

        edge_perm_list = perm.Permutation(53).list()
        for i in range(12):
            edge_perm_list[np.asarray(LSE_pieces).reshape(12)[i]] = np.asarray(
                LSE_pieces_new
            ).reshape(12)[i]

        scramble_perm = perm.Permutation(11, 20, 29, 38)(6, 8, 2, 0)(
            18, 27, 36, 9
        ) ** corners * perm.Permutation(edge_perm_list)

        self.cube = scramble_perm(self.cube)
        order = scramble_perm.order()
        inv_scramble = (scramble_perm ** (order - 2))(self.cube)
        empty = ""
        non_M2_scramble = utils.solve(empty.join(inv_scramble), "Kociemba")
        M2_scramble = []
        if m2 == 1:
            for mv in non_M2_scramble + ["M2"]:
                M2_scramble.append(mv)  # couldn't directly append M2 so did it this way
            self.cube = M2(self.cube)
        else:
            M2_scramble = non_M2_scramble
        self.print_cube()
        self.scramble.set(M2_scramble)

    def print_cube(self):
        for x in range(3):
            for y in range(3):
                self.generic_print_cube(self.cube_space, 10, x, y)

    def generic_print_cube(self, canv, dim, x, y):
        csU = canv.create_rectangle(
            10 * x + 50,
            10 * y + 10,
            10 * x + 50 + dim,
            10 * y + 10 + dim,
            fill=self.colour_dict.get(self.cube[x + 3 * y]),
        )
        csL = canv.create_rectangle(
            10 * x + 10,
            10 * y + 50,
            10 * x + 10 + dim,
            10 * y + 50 + dim,
            fill=self.colour_dict.get(self.cube[x + 3 * y + 9]),
        )
        csF = canv.create_rectangle(
            10 * x + 50,
            10 * y + 50,
            10 * x + 50 + dim,
            10 * y + 50 + dim,
            fill=self.colour_dict.get(self.cube[x + 3 * y + 18]),
        )
        csR = canv.create_rectangle(
            10 * x + 90,
            10 * y + 50,
            10 * x + 90 + dim,
            10 * y + 50 + dim,
            fill=self.colour_dict.get(self.cube[x + 3 * y + 27]),
        )
        csB = canv.create_rectangle(
            10 * x + 130,
            10 * y + 50,
            10 * x + 130 + dim,
            10 * y + 50 + dim,
            fill=self.colour_dict.get(self.cube[x + 3 * y + 36]),
        )
        csD = canv.create_rectangle(
            10 * x + 50,
            10 * y + 90,
            10 * x + 50 + dim,
            10 * y + 90 + dim,
            fill=self.colour_dict.get(self.cube[x + 3 * y + 45]),
        )
        return ([csU, "U"], [csL, "L"], [csF, "F"], [csR, "R"], [csB, "B"], [csD, "D"])


timer = RouxTimer()
