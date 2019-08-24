from rubik_solver 						import utils
import random
import sympy.combinatorics.permutations as perm
import sympy.combinatorics.generators   as gens
import numpy							as np
from tkinter 							import *

"""
	Created by Jupiterian (aka Jeffery, aka JupiLogy).
	https://github.com/JupiLogy/Roux-Cube-Timer/

	Terms:
		Code may be edited and redistributed,
		but do not remove these terms,
		do not remove the author's name,
		and do not use for monetary gain.

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
	4 (Upper center)	: YELLOW
	13 (Left center)	: BLUE
	22 (Front center)	: RED
	31 (Right center)	: GREEN
	40 (Back center)	: ORANGE
	49 (Down center)	: WHITE
"""

def move_button_press(permutation):
	global cube
	cube = permutation(cube)
	printcube(cube)

def LSE_scramble():
	global cube
	global solved_cube
	global scramble
	global alternating_6
	global odd_6
	global M2
	global y2
	cube   			= solved_cube
	corners			= random.choice(range(4))
	if corners == 1 or corners == 3:
		permn 		= random.choice(odd_6)
	else:
		permn  		= random.choice(alternating_6)
	flip   			= random.choice(range(4))
	orient 			= random.sample(range(6), flip*2)
	m2 				= random.choice(range(2))
	corner_pieces 	= np.array([[11, 6, 18], [20, 8, 27], [29, 2, 36], [38, 0, 9]])
	LSE_pieces 		= np.array([[1, 37], [3, 10], [7, 19], [5, 28], [46, 25], [52, 43]])
	LSE_pieces_new	= LSE_pieces
	for i in orient:
		LSE_pieces_new[i] = perm.Permutation(0,1)(LSE_pieces[i])
	LSE_pieces_new 	= permn(LSE_pieces_new)

	corner_dict		={
		0 : 11,
		1 : 6,
		2 : 18,

		3 : 20,
		4 : 8,
		5 : 27,

		6 : 29,
		7 : 2,
		8 : 36,

		9 : 38,
		10: 0,
		11: 9
	}
	LSE_dict		={
		0 : 1,
		1 : 37,
		2 : 3,
		3 : 10,
		4 : 7,
		5 : 19,
		6 : 5,
		7 : 28,
		8 : 46,
		9 : 25,
		10: 52,
		11: 43 
	}

	edge_perm_list	= perm.Permutation(53).list()
	for i in range(12):
		edge_perm_list[np.asarray(LSE_pieces).reshape(12)[i]] = np.asarray(LSE_pieces_new).reshape(12)[i]

	scramble_perm = perm.Permutation(11,20,29,38)(6,8,2,0)(18,27,36,9)**corners*perm.Permutation(edge_perm_list)

	cube = scramble_perm(cube)
	order 			= scramble_perm.order()
	inv_scramble	= (scramble_perm**(order-2))(cube)
	empty 			= ""
	non_M2_scramble = utils.solve(empty.join(inv_scramble), 'Kociemba')
	M2_scramble = []
	if m2 == 1:
		for mv in non_M2_scramble+["M2"]:
			M2_scramble.append(mv)			#couldn't directly append M2 so did it this way
		cube = M2(cube)
	else:
		M2_scramble = non_M2_scramble
	printcube(cube)
	scramble.set(M2_scramble)

def bad_scramble():
	global cube
	cube = []
	for i in range(54):
		cube.append(random.choice(colours))
	printcube(cube)
	mainloop()

def printcube(cube):
	cubelets = []
	for x in range(3):
		for y in range(3):
			cU = cube_space.create_rectangle(10*x+50,  10*y+10, 10*x+60,  10*y+20,  fill = colour_dict.get(cube[x+3*y   ]))
			cL = cube_space.create_rectangle(10*x+10,  10*y+50, 10*x+20,  10*y+60,  fill = colour_dict.get(cube[x+3*y+9 ]))
			cF = cube_space.create_rectangle(10*x+50,  10*y+50, 10*x+60,  10*y+60,  fill = colour_dict.get(cube[x+3*y+18]))
			cR = cube_space.create_rectangle(10*x+90,  10*y+50, 10*x+100, 10*y+60,  fill = colour_dict.get(cube[x+3*y+27]))
			cB = cube_space.create_rectangle(10*x+130, 10*y+50, 10*x+140, 10*y+60,  fill = colour_dict.get(cube[x+3*y+36]))
			cD = cube_space.create_rectangle(10*x+50,  10*y+90, 10*x+60,  10*y+100, fill = colour_dict.get(cube[x+3*y+45]))

def generate_moves():
	y2 = default_cube
	M2 = default_cube
	M  = default_cube
	Mp = default_cube
	U  = default_cube
	U2 = default_cube
	Up = default_cube

	for cubelet in range(9):
		y2 = y2*perm.Permutation(cubelet,    cubelet+45)							#Swaps U and D faces
	for cubelet in range(4):
		y2 = y2*perm.Permutation(cubelet+27, 35-cubelet)							#Rotates R face
		y2 = y2*perm.Permutation(cubelet+9,  17-cubelet)							#Rotates L face
	for cubelet in range(3):
		y2 = y2*perm.Permutation(cubelet+18, 44-cubelet)							#Puts FU* to BD*
		y2 = y2*perm.Permutation(cubelet+21, 41-cubelet)							#Puts FE* to BE*
		y2 = y2*perm.Permutation(cubelet+24, 38-cubelet)							#Puts FD* to BU*

	for cubelet in [1,4,7]:
		M  = M *perm.Permutation(cubelet,	 44-cubelet, cubelet+45, cubelet+18)	# UM -> FM -> DM -> BM

	U = perm.Permutation(53)(0,2,8,6)(1,5,7,3)										#Rotates U face
	for cubelet in [9,10,11]:
		U  = U *perm.Permutation(cubelet,    cubelet+9,  cubelet+18, cubelet+27)	# FU -> LU -> BU -> RU

	M2 = M*M
	Mp = M2*M

	U2 = U*U
	Up = U2*U

	return [y2, M, M2, Mp, U, U2, Up]

def generate_groups():
	global alternating_6
	global odd_6
	alternating_6	= list(gens.alternating(6))
	odd_6 = [x for x in list(gens.symmetric(6)) if x not in alternating_6]

colours = ["Y","B","R","G","O","W"]
colour_dict = {
	"Y" : "#ffff00",
	"W" : "#ffffff",
	"R" : "#ff0000",
	"O" : "#ffa500",
	"B" : "#2222ff",
	"G" : "#00ff00"
}

default_cube = perm.Permutation(53)

win = Tk()
win.geometry("300x200")
win.title("RouxTimer")

cube_space = Canvas(win , height = 130, width = 170, bg = "#aaaaaa")
cube_space.pack(side=TOP)

solved_cube = []
for colour in colours:
	for cubie in range(9):
		solved_cube.append(colour)
cube = solved_cube

scramble_button = Button(win, text="LSE", command=LSE_scramble)
scramble_button.pack()

y2, M, M2, Mp, U, U2, Up = generate_moves()
generate_groups()

move_buttons = []
move_buttons.append(Button(win, text="y2", command= lambda: move_button_press(y2)))

move_buttons.append(Button(win, text="M",  command= lambda: move_button_press(M )))
move_buttons.append(Button(win, text="M2", command= lambda: move_button_press(M2)))
move_buttons.append(Button(win, text="M'", command= lambda: move_button_press(Mp)))

move_buttons.append(Button(win, text="U",  command= lambda: move_button_press(U )))
move_buttons.append(Button(win, text="U2", command= lambda: move_button_press(U2)))
move_buttons.append(Button(win, text="U'", command= lambda: move_button_press(Up)))

# for b in move_buttons:
# 	b.pack()

scramble = StringVar()
Label(win,textvariable=scramble).pack()

printcube(solved_cube)
mainloop()