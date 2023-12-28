'''
TicTacToe Game

x plays first

Board Representation:

x's are 1s o's are -1s

x o 
o x o
  o x

[[1,-1,0],[-1,1,-1],[0,-1,1]
'''
import pygame

# position class
class Position:
	# initializing
	def __init__(self, squares=[[0,0,0],[0,0,0],[0,0,0]], turn=1):
		self.squares = squares
		self.turn = turn

	# defining display
	def __str__(self):
		s = ''
		for row in self.squares:
			for column in row:
				s += ('x' if column == 1 else ("o" if column == -1 else ' ')) + ' '
			s += '\n'
		s += ('x' if self.turn == 1 else 'o') + ' to move'
		return 

	# evaluate position
	def evaluate(self):
		# check rows
		for row in self.squares:
			total = 0
			for square in row:
				total += square
			if total == 3:
				return 1
			elif total == -3:
				return -1

		# check columns
		for column in [0,1,2]:
			total = 0
			for row in self.squares:
				total += row[column]
			if total == 3:
				return 1
			elif total == -3:
				return -1

		# check diagonals
		d1 = self.squares[0][0] + self.squares[1][1] + self.squares[2][2]
		d2 = self.squares[0][2] + self.squares[1][1] + self.squares[2][0]
		if d1 == 3 or d2 == 3:
			return 1
		if d1 == -3 or d2 == -3:
			return -1

		# base case
		return 0

	# making a move
	def move(self, row, column):
		if self.squares[row][column] == 0:
			self.squares[row][column] = self.turn
			self.turn = -self.turn

	# finding all legal moves
	def all_moves(self):
		move_list = []
		for row in [0,1,2]:
			for column in [0,1,2]:
				if self.squares[row][column] == 0:
					move_list.append((row,column))
		return move_list

	# copying
	def copy(self):
		new_squares = [[0,0,0],[0,0,0],[0,0,0]]
		for row in [0,1,2]:
			for column in [0,1,2]:
				new_squares[row][column] = self.squares[row][column]
		return Position(new_squares,self.turn)


# game class
class TicTacToe:

	def __init__(self, screen, position=Position()):
		self.screen = screen
		self.width = self.screen.get_width()
		self.height = self.screen.get_height()
		self.position = position
		self.victory = False

	def draw_board(self):
		width = self.width
		height = self.height
		self.screen.fill((255,255,255))
		for row in [0,1,2]:
			for column in [0,1,2]:
				if self.position.squares[row][column] == 1:
					image = pygame.transform.scale(pygame.image.load('Images/x.jpeg'),(width/3,height/3))
					self.screen.blit(image,(column*width/3,row*height/3))
				elif self.position.squares[row][column] == -1:
					image = pygame.transform.scale(pygame.image.load('Images/o.jpeg'),(width/3,height/3))
					self.screen.blit(image,(column*width/3,row*height/3))
		pygame.draw.line(self.screen,(0,0,0),(width/3,0),(width/3,height),width=int(width/100))
		pygame.draw.line(self.screen,(0,0,0),(2*width/3,0),(2*width/3,height),width=int(width/100))
		pygame.draw.line(self.screen,(0,0,0),(0,height/3),(width,height/3),width=int(height/100))
		pygame.draw.line(self.screen,(0,0,0),(0,2*height/3),(width,2*height/3),width=int(height/100))
		pygame.display.flip()

	def move(self, move):
		self.position.move(move[0],move[1])
		if self.position.evaluate() != 0:
			self.victory = True

	def mouse_event(self,mx,my):
		if mx/self.width < 1/3:
			column = 0
		elif mx/self.width < 2/3:
			column = 1
		else: column = 2
		if my/self.height < 1/3:
			row = 0
		elif my/self.width < 2/3:
			row = 1
		else: row = 2
		moved = False
		if self.position.squares[row][column] == 0:
			moved = True
		self.move((row,column))
		return moved

	def all_moves(self):
		if not self.victory:
			return self.position.all_moves()
		return []

	def copy(self):
		return TicTacToe(self.screen,self.position.copy())



	


