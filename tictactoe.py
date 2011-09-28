#! /usr/bin/env python

#tictactoe
# Tic Tac Toe game that will eventually have a computer player
#	Control is done with the mouse
#
# v1.0 - Game Works, Two humans only 
# v2.0 - Added Computer Player, but it just picks the first available space
# v2.1 - Computer plans its moves a little, but it isn't great (don't think it is possible to win 3x3)
# v2.2 - Rewrote Some of the functions (CheckWin and CalculateDesire) Same functionality but cleaner code
# v2.3 - Rewrote CalculateDesire again to account for multiple win/lose scenarios in the same line, will make future upgrades easier
#	v2.4 - The Calculations are as good as I can get them, It would be fun if it could learn, but that seems impossible. I don't think you can win without an early trick that is impossible to beat
# v3.0 - Connect Four - AI not the best, still on tic tac toe. AI should think about building

from Tkinter import *
from random import *
import sys

######################################
#Constants

#The size of each section, ie where the X or O goes
SECTIONSIZE = 75

#The number in a row it takes to win
WINNUM = int(sys.argv[2])

#The sqrt of the number of playing spaces, or the length of one side
PLAYSIZE = int(sys.argv[1])

#The dimensions of the board in pixels
BOARDSIZE = SECTIONSIZE * PLAYSIZE

#PLACEHOLDERS to use in the games storage tables
EMPTY = 0  
CIRCLE = 1
CROSS = 2
GAMEOVER = 3

EMPTYCOUNT = 1
SAMECOUNT = 3  #must be > EMPTYCOUNT +1
OPPCOUNT = 4

root = Tk()

#Set the initial player, CIRLCE was Previous so CROSS is up
Previous = CIRCLE

#initialize the storage table, 2D array initialization is one of the few things that is a pain in python, using it is standard though
Table = []
for i in range(PLAYSIZE):
 	Row = []
	for j in range(PLAYSIZE):
		Row.append(0)	
	Table.append(Row)



################################
#      FindSection(X,Y)
# Converts Pixel coordinates into Section Coordinates
# Inputs (X,Y)
# X - X Coordinate in Pixels
# Y - Y Coordinate in Pixels
#
# Outputs
# (X,Y)
# X - X Coordinate in Sections
# Y - Y Coordinate in Sections

def FindSection(X,Y):
	section = []
	for i in range(BOARDSIZE):
		if X < SECTIONSIZE * (i+1):
			section.append(i)
			break
	for i in range(BOARDSIZE):
		if Y < SECTIONSIZE * (i+1):
			section.append(i)
			break
	return section



################################
#      Checkwin(X,Y)
# Takes a section and determines if that section is involved in a Win Scenario (WINNUM in a row)
# Inputs (X,Y)
# X - X Coordinate in Sections
# Y - Y Coordinate in Sections
#
# Outputs
# ((X1,Y1),(X2,Y2))
# X1 - X Coordinate in Sections of one of the endpoints of a line
# Y1 - Y Coordinate in Sections of one of the endpoints of a line
# X2 - X Coordinate in Sections of one of the endpoints of a line
# Y2 - Y Coordinate in Sections of one of the endpoints of a line

def CheckWin(X,Y):
	global Table

	Type = Table[X][Y]  
	XChange = (1,0,1,-1)
	YChange = (0,1,1,1)		
	
	for k in range(4):
		Top = (X,Y)	
		Bottom = (X,Y)
		Count = 1

		i = X + XChange[k]
		j = Y + YChange[k]

		while(0 <= i <= (PLAYSIZE-1) and 0 <= j <= (PLAYSIZE-1) and Table[i][j] == Type): #While the range is in bounds and the Type (X or O) is the same
			Count = Count + 1
			Top = (i,j)
			i = i + XChange[k]
			j = j + YChange[k]


		i = X - XChange[k]
		j = Y - YChange[k]
		while(0 <= i <= (PLAYSIZE-1) and 0 <= j <= (PLAYSIZE-1) and Table[i][j] == Type): #Same as above, but it is checking the opposite direction
			Count = Count + 1
			Bottom = (i,j)
			i = i - XChange[k]
			j = j - YChange[k]


		if (Count >= WINNUM):
			return (Top,Bottom)

	return 0;

################################
#      
# Draws a red line through a set of squares, also sets the Table so no more plays are allowed
# Inputs (Canvas,(X1,Y1),(X2,Y2))
# Canvas - The Canvas to Draw on
# X1 - X Coordinate in Sections of one of the endpoints of a line
# Y1 - Y Coordinate in Sections of one of the endpoints of a line
# X2 - X Coordinate in Sections of one of the endpoints of a line
# Y2 - Y Coordinate in Sections of one of the endpoints of a line
#
#

def redline(Canvas, Top, Bottom):
	global Table
	
	Canvas.create_line(Top[0]*SECTIONSIZE+SECTIONSIZE/2,Top[1]*SECTIONSIZE+SECTIONSIZE/2,Bottom[0]*SECTIONSIZE+SECTIONSIZE/2,Bottom[1]*SECTIONSIZE+SECTIONSIZE/2,width = 10, fill = "red")
	for i in range(PLAYSIZE):
		for j in range(PLAYSIZE):
			Table[i][j] = GAMEOVER
	print "Game Over"

################################
#      
# Draws a 'X' on the play surface at the coordinates given
# Inputs (Canvas,X,Y)
# Canvas - The Canvas to Draw on
# X - X Coordinate in Sections
# Y - Y Coordinate in Sections

def DrawCross(Canvas, X,Y):
	X1 = X*SECTIONSIZE
	Y1 = Y*SECTIONSIZE
	EXTRA = SECTIONSIZE

	Canvas.create_line(X1,Y1,X1 + EXTRA,Y1+EXTRA,width = 3)
	Canvas.create_line(X1+EXTRA,Y1,X1,Y1+EXTRA,width = 3)


################################
#      
# Draws a circle on the play surface at the coordinates given
# Inputs (Canvas,X,Y)
# Canvas - The Canvas to Draw on
# X - X Coordinate in Sections
# Y - Y Coordinate in Sections
#

def DrawCircle(Canvas, X,Y):
	X1 = X*SECTIONSIZE
	Y1 = Y*SECTIONSIZE
	EXTRA = SECTIONSIZE

	Canvas.create_oval(X1,Y1,X1+EXTRA,Y1+EXTRA,width = 3)

################################
#      CalculateDesire()
# Determines the Desire to place a token in the given space, Higher the Better
# Inputs (X,Y, Type)
# X - X Coordinate in Sections
# Y - Y Coordinate in Sections
# Type - The Type of tile (Cross or Circle)
#

def CalculateDesire(X,Y,Same):
	global Table
  

	if Same == CROSS:
		Opposite = CIRCLE
	else:
		Opposite = CROSS

	Desire = 0	

	XChange = (1,0,1,-1)
	YChange = (0,1,1,1)		


########################
# Create Lines for the Four Directions -,|,\,/
#

	for k in range(4):
		Line = ['O']


		i = X + XChange[k]
		j = Y + YChange[k]
		for m in range(WINNUM-1):
			if (0 <= i < PLAYSIZE and 0 <= j < PLAYSIZE):
				Line.append(Table[i][j])
			else:
				Line.append('X')
			i = i + XChange[k]
			j = j + YChange[k]


		i = X - XChange[k]
		j = Y - YChange[k]

		for m in range(WINNUM-1):
			if (0 <= i < PLAYSIZE and 0 <= j < PLAYSIZE):
				Line.insert(0,Table[i][j])
			else:
				Line.insert(0,'X')

			i = i - XChange[k]
			j = j - YChange[k]


#################
# For both the same type and opposite calculate all of the possible win/lose scenarios
# Currently doesn't take empties spaces into account. 
#

		for OppType in [Same,Opposite]:
			for i in range(WINNUM): 
				j = 0
				Count = 1
				while (j < WINNUM and Line[i+j] != OppType and Line[i+j] != 'X'):  #Add up a whole win scenario length
					if Line[i+j] == EMPTY:
						Count += EMPTYCOUNT
					elif OppType != Same:
						Count *= SAMECOUNT
					else:
						Count *= OPPCOUNT
					j += 1

				if j != WINNUM:
					Count = 0

				if OppType != Same and Count >= (SAMECOUNT**WINNUM):	#if there is an immediate win/lose scenarion take it
						print Line[i:i+j],":",Count
						return(1000000000+100000)

				elif Count >= (OPPCOUNT**WINNUM):
						print Line[i:i+j],":",Count
						return(100000000)



				Desire += Count**2

		


	return Desire

################################
#      AI()
# Determines where the Cirrcle should go on the board
# Inputs (Canvas)
# Canvas - The Canvas to Draw on
#
#

def AI(Canvas):
	global Table
	global Previous

	OpenSpaces = []
	SpaceDesire = []
	temptable = [] # temp
	for i in range(PLAYSIZE):
		temprow = []  #temp
		for j in range(PLAYSIZE): #temp
			temprow.append(0)  #temp
		temptable.append(temprow)   #temp
		j = PLAYSIZE-1
		while(Table[i][j] != EMPTY and j != 0):
			j += -1
		if Table[i][j] == EMPTY:
			OpenSpaces.append((i,j))

	if OpenSpaces == []:
		print "Game Over!"
		return(0,0)

	for Space in OpenSpaces:
		SpaceDesire.append(CalculateDesire(Space[0],Space[1],CIRCLE))

	i = 0  #temp
	for Space in OpenSpaces:										#temp
		temptable[Space[1]][Space[0]] = SpaceDesire[i] # temp
		i = i+1
	for row in temptable:  #temp
		print row	#temp
	print
  
	(X,Y) = OpenSpaces[SpaceDesire.index(max(SpaceDesire))]
	DrawCircle(Canvas,X,Y)
	Table[X][Y] = CIRCLE
	Previous = CIRCLE

	return(X,Y)


################################
#      
# Bound to the Mouse click, Interprets the mouse click as a play by the user
# Inputs (event)
# event - The Event generate by Tk
#
#

def play(event):

	global Previous
	global Table
	Canvas = event.widget
	X = event.x
	Y = event.y
	Section = FindSection(X,Y)

	j = PLAYSIZE-1
	while(Table[Section[0]][j] != EMPTY and j != 0):
		j += -1

	Section[1] = j

	LineX = SECTIONSIZE * Section[0]
	LineY = SECTIONSIZE * Section[1]


	if Table[Section[0]][Section[1]] == EMPTY:
		if (Previous == CIRCLE):
			DrawCross(Canvas,Section[0],Section[1])
			Table[Section[0]][Section[1]] = CROSS
			Previous = CROSS

			Win = CheckWin(Section[0],Section[1])
			if Win != 0: #Human Win
				redline(Canvas, Win[0], Win[1])
			else:			
				Section = AI(Canvas)
				Win = CheckWin(Section[0],Section[1])
				if Win != 0: #AI Win
					redline(Canvas, Win[0], Win[1])


################################
#      
# Bound to the R Mouse click, Interprets the rmouse click as cheat to calulate the desire of that spot
# Inputs (event)
# event - The Event generate by Tk
#
#

def cheat(event):

	global Previous
	global Table
	Canvas = event.widget
	X = event.x
	Y = event.y
	Section = FindSection(X,Y)

	j = PLAYSIZE-1
	while(Table[Section[0]][j] != EMPTY and j != 0):
		j += -1

	Section[1] = j



	if Table[Section[0]][Section[1]] == EMPTY:
		print(CalculateDesire(Section[0],Section[1],CROSS))


page = Canvas(root, width = BOARDSIZE, height = BOARDSIZE)
page.grid()

for i in range(1,PLAYSIZE):
	page.create_line(SECTIONSIZE*i, 0,SECTIONSIZE*i, BOARDSIZE, width = 5)
	page.create_line(0, SECTIONSIZE*i,BOARDSIZE, SECTIONSIZE*i, width = 5)

page.bind("<Button-1>", play)
page.bind("<Button-3>", cheat)

root.mainloop()
  
