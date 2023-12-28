
'''
TicTacToe Game

1 plays first

Board Representation:

red is 1, yellow is -1, nothing is 0

7 columns of length 6 in matrix
'''
import pygame, math

default_position = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
default_filled = [0,0,0,0,0,0,0]

# position class
class Position:
	# initializing
	def __init__(self, spots=default_position, filled=default_filled, turn=1):
		self.spots = spots
		self.filled = filled
		self.turn = turn

	# evaluate position
	def evaluate(self):
		for col in range(7):
			column = self.spots[col]
			for i in range(self.filled[col]):
				if col < 4:
					e1 = self.filled[col+1] > i
					e2 = self.filled[col+2] > i
					e3 = self.filled[col+3] > i
					if e1 and e2 and e3:
						connection = column[i] + self.spots[col+1][i] + self.spots[col+2][i] + self.spots[col+3][i]
						if connection == 4:
							return 1
						elif connection == -4:
							return -1
				if i < self.filled[col]-3:
					connection = column[i] + column[i+1] + column[i+2] + column[i+3]
					if connection == 4:
						return 1
					elif connection == -4: return -1
		return 0

	# making a move
	def move(self, column):
		row = self.filled[column]
		if row >= 6:
			return False
		self.spots[column][row] = self.turn
		self.filled[column] += 1
		if self.turn == 1:
			self.turn = -1
		else: self.turn = 1
		return True

	# finding all legal moves
	def all_moves(self):
		moves = []
		for i in range(7):
			if self.filled[i] < 6:
				moves.append(i)
		return moves

	# copying
	def copy(self):
		new_spots = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
		new_filled = [0,0,0,0,0,0,0]
		for col in range(7):
			for row in range(6):
				new_spots[col][row] = self.spots[col][row]
			new_filled[col] = self.filled[col]
		return Position(new_spots,new_filled,self.turn)


# game class
class ConnectFour:

	def __init__(self, screen, position=Position()):
		self.screen = screen
		self.width = self.screen.get_width()
		self.height = self.screen.get_height()
		self.position = position
		self.victory = False

	def draw_board(self):
		sx = self.width/7
		sy = self.height/6
		self.screen.fill((255,255,255))
		for column in range(7):
			for row in range(6):
				spot = self.position.spots[column][row]
				if spot == 1:
					color = (255,0,0)
				elif spot == -1:
					color = (255,255,0)
				else: color = (255,255,255)
				pygame.draw.rect(self.screen,color,pygame.Rect(sx*column,sy*(5-row),sx,sy))
		pygame.draw.line(self.screen,(0,0,0),(sx,0),(sx,6*sy),width=int(sx/50))
		pygame.draw.line(self.screen,(0,0,0),(2*sx,0),(2*sx,6*sy),width=int(sx/50))
		pygame.draw.line(self.screen,(0,0,0),(3*sx,0),(3*sx,6*sy),width=int(sx/50))
		pygame.draw.line(self.screen,(0,0,0),(4*sx,0),(4*sx,6*sy),width=int(sx/50))
		pygame.draw.line(self.screen,(0,0,0),(5*sx,0),(5*sx,6*sy),width=int(sx/50))
		pygame.draw.line(self.screen,(0,0,0),(6*sx,0),(6*sx,6*sy),width=int(sx/50))
			
		pygame.display.flip()

	def move(self, move):
		moved = self.position.move(move)
		# possible time save if this evaluation can be removed
		if self.position.evaluate() != 0:
			self.victory = True
		if moved:
			return True
		return False

	def mouse_event(self,mx,my):
		column = math.floor(7*mx/self.width)
		moved = self.move(column)
		if moved:
			return True
		return False

	def all_moves(self):
		if not self.victory:
			return self.position.all_moves()
		return []

	def copy(self):
		return ConnectFour(self.screen,self.position.copy())



	


