

'''
Chess

Board Representation:
8x8 array holding piece classes and 0's for empty squares
castling rights are owned by rooks and kings
last move part of position for en passant


Team representation:
white is 1 black is -1




'''

import pygame,math,random

# Constants
light_color = (238,238,210)
dark_color = (118,150,86)
valid_color = (255,0,0)
lm_color = (0,255,0)

king_value = [[-30,-40,-40,-50,-50,-40,-40,-30],
			  [-30,-40,-40,-50,-50,-40,-40,-30],
			  [-30,-40,-40,-50,-50,-40,-40,-30],
			  [-30,-40,-40,-50,-50,-40,-40,-30],
			  [-20,-30,-30,-40,-40,-30,-30,-20],
			  [-10,-20,-20,-20,-20,-20,-20,-10],
			  [ 20, 20,  0,  0,  0,  0, 20, 20],
			  [ 20, 30, 10,  0,  0, 10, 30, 20]]

queen_value = [[-20,-10,-10, -5, -5,-10,-10,-20],
			   [-10,  0,  0,  0,  0,  0,  0,-10],
			   [-10,  0,  5,  5,  5,  5,  0,-10],
			   [ -5,  0,  5,  5,  5,  5,  0, -5],
			   [  0,  0,  5,  5,  5,  5,  0, -5],
			   [-10,  5,  5,  5,  5,  5,  0,-10],
			   [-10,  0,  5,  0,  0,  0,  0,-10],
			   [-20,-10,-10, -5, -5,-10,-10,-20]]

rook_value = [[ 0,  0,  0,  0,  0,  0,  0,  0],
			  [ 5, 10, 10, 10, 10, 10, 10,  5],
			  [-5,  0,  0,  0,  0,  0,  0, -5],
			  [-5,  0,  0,  0,  0,  0,  0, -5],
			  [-5,  0,  0,  0,  0,  0,  0, -5],
			  [-5,  0,  0,  0,  0,  0,  0, -5],
			  [-5,  0,  0,  0,  0,  0,  0, -5],
			  [ 0,-10,  0,  5,  5,  0,-10,  0]]

knight_value = [[-50,-40,-30,-30,-30,-30,-40,-50],
				[-40,-20,  0,  0,  0,  0,-20,-40],
				[-30,  0, 10, 15, 15, 10,  0,-30],
				[-30,  5, 15, 20, 20, 15,  5,-30],
				[-30,  0, 15, 20, 20, 15,  0,-30],
				[-30,  5, 10, 15, 15, 10,  5,-30],
				[-40,-20,  0,  5,  5,  0,-20,-40],
				[-50,-40,-30,-30,-30,-30,-40,-50]]

bishop_value = [[-20,-10,-10,-10,-10,-10,-10,-20],
				[-10,  0,  0,  0,  0,  0,  0,-10],
				[-10,  0,  5, 10, 10,  5,  0,-10],
				[-10,  5,  5, 10, 10,  5,  5,-10],
				[-10,  0, 10, 10, 10, 10,  0,-10],
				[-10, 10, 10, 10, 10, 10, 10,-10],
				[-10,  5,  0,  0,  0,  0,  5,-10],
				[-20,-10,-10,-10,-10,-10,-10,-20]]
 
pawn_value = [[ 0,  0,  0,  0,  0,  0,  0,  0],
			  [50, 50, 50, 50, 50, 50, 50, 50],
			  [10, 10, 20, 30, 30, 20, 10, 10],
 			  [ 5,  5, 10, 25, 25, 10,  5,  5],
			  [ 0,  0,  0, 20, 20,  0,  0,  0],
			  [ 5, -5,-10,  0,  0,-10, -5,  5],
			  [ 5, 10, 10,-20,-20, 10, 10,  5],
			  [ 0,  0,  0,  0,  0,  0,  0,  0]]

for row in range(8):
	for col in range(8):
		pawn_value[row][col] = 1 + pawn_value[row][col]/100
		knight_value[row][col] = 3 + knight_value[row][col]/100
		bishop_value[row][col] = 3.5 + bishop_value[row][col]/100
		rook_value[row][col] = 5 + rook_value[row][col]/100
		queen_value[row][col] = 9 + queen_value[row][col]/100
		king_value[row][col] = 100 + king_value[row][col]/100




class King:
	def __init__(self, color, location, moved=False):
		self.location = location
		self.color = color
		self.moved = moved
		if self.color == 1:
			self.image = 'Images/Chess_klt60.png'
		else: self.image = 'Images/Chess_kdt60.png'

	def all_moves(self, board):
		moves = []
		directions = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
		for direction in directions:
			spot = (self.location[0]+direction[0],self.location[1]+direction[1])
			if spot[0] >=0 and spot[0] <= 7 and spot[1] >= 0 and spot[1] <= 7 and (board[spot[0]][spot[1]] == 0 or board[spot[0]][spot[1]].color != self.color):
				moves.append([(self.location,spot)])
		if not self.moved:
			if board[self.location[0]][self.location[1]+1] == 0 and board[self.location[0]][self.location[1]+2] == 0 and type(board[self.location[0]][self.location[1]+3]) == Rook and not board[self.location[0]][self.location[1]+3].moved:
				moves.append([(self.location,(self.location[0],self.location[1]+2)),((self.location[0],7),(self.location[0],5))])
			if board[self.location[0]][self.location[1]-1] == 0 and board[self.location[0]][self.location[1]-2] == 0 and board[self.location[0]][self.location[1]-3] == 0 and type(board[self.location[0]][self.location[1]-4]) == Rook and not board[self.location[0]][self.location[1]-4].moved:
				moves.append([(self.location,(self.location[0],self.location[1]-2)),((self.location[0],0),(self.location[0],3))])
		return moves

	def value(self):
		if self.color == 1:
			return king_value[self.location[0]][self.location[1]]
		else: return king_value[7-self.location[0]][self.location[1]]
		
	def move(self, spot):
		self.location = spot
		self.moved = True

	def copy(self):
		return King(self.color, self.location, self.moved)

class Queen:
	def __init__(self, color, location):
		self.location = location
		self.color = color
		if self.color == 1:
			self.image = 'Images/Chess_qlt60.png'
		else: self.image = 'Images/Chess_qdt60.png'

	def all_moves(self, board):
		moves = []
		directions = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
		for direction in directions:
			spot = (self.location[0]+direction[0],self.location[1]+direction[1])
			while spot[0] >=0 and spot[0] <= 7 and spot[1] >= 0 and spot[1] <= 7 and (board[spot[0]][spot[1]] == 0 or board[spot[0]][spot[1]].color != self.color):
				moves.append([(self.location,spot)])
				if board[spot[0]][spot[1]] != 0:
					break
				spot = (spot[0]+direction[0],spot[1]+direction[1])
		return moves

	def move(self, spot):
		self.location = spot

	def value(self):
		if self.color == 1:
			return queen_value[self.location[0]][self.location[1]]
		else: return queen_value[7-self.location[0]][self.location[1]]

	def copy(self):
		return Queen(self.color, self.location)

class Bishop:
	def __init__(self, color, location):
		self.location = location
		self.color = color
		if self.color == 1:
			self.image = 'Images/Chess_blt60.png'
		else: self.image = 'Images/Chess_bdt60.png'

	def all_moves(self, board):
		moves = []
		directions = [(1,1),(1,-1),(-1,-1),(-1,1)]
		for direction in directions:
			spot = (self.location[0]+direction[0],self.location[1]+direction[1])
			while spot[0] >=0 and spot[0] <= 7 and spot[1] >= 0 and spot[1] <= 7 and (board[spot[0]][spot[1]] == 0 or board[spot[0]][spot[1]].color != self.color):
				moves.append([(self.location,spot)])
				if board[spot[0]][spot[1]] != 0:
					break
				spot = (spot[0]+direction[0],spot[1]+direction[1])
		return moves

	def move(self, spot):
		self.location = spot

	def value(self):
		if self.color == 1:
			return bishop_value[self.location[0]][self.location[1]]
		else: return bishop_value[7-self.location[0]][self.location[1]]

	def copy(self):
		return Bishop(self.color, self.location)

class Knight:
	def __init__(self, color, location):
		self.location = location
		self.color = color
		if self.color == 1:
			self.image = 'Images/Chess_nlt60.png'
		else: self.image = 'Images/Chess_ndt60.png'

	def all_moves(self, board):
		moves = []
		combinations = [(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2),(1,2)]
		for combo in combinations:
			square = (self.location[0]+combo[0],self.location[1]+combo[1])
			if (square[0] >= 0 and square[0] <= 7) and (square[1] >= 0 and square[1] <= 7):
				if board[square[0]][square[1]] == 0 or board[square[0]][square[1]].color != self.color:
					moves.append([(self.location,square)])
		return moves

	def move(self, spot):
		self.location = spot

	def value(self):
		if self.color == 1:
			return knight_value[self.location[0]][self.location[1]]
		else: return knight_value[7-self.location[0]][self.location[1]]

	def copy(self):
		return Knight(self.color, self.location)

class Rook:
	def __init__(self, color, location, moved=False):
		self.location = location
		self.color = color
		self.moved = moved
		if self.color == 1:
			self.image = 'Images/Chess_rlt60.png'
		else: self.image = 'Images/Chess_rdt60.png'

	def all_moves(self, board):
		moves = []
		directions = [(0,1),(1,0),(0,-1),(-1,0)]
		for direction in directions:
			spot = (self.location[0]+direction[0],self.location[1]+direction[1])
			while spot[0] >=0 and spot[0] <= 7 and spot[1] >= 0 and spot[1] <= 7 and (board[spot[0]][spot[1]] == 0 or board[spot[0]][spot[1]].color != self.color):
				moves.append([(self.location,spot)])
				if board[spot[0]][spot[1]] != 0:
					break
				spot = (spot[0]+direction[0],spot[1]+direction[1])
		return moves

	def value(self):
		if self.color == 1:
			return rook_value[self.location[0]][self.location[1]]
		else: return rook_value[7-self.location[0]][self.location[1]]

	def move(self, spot):
		self.location = spot
		self.moved = True

	def copy(self):
		return Rook(self.color, self.location, self.moved)

class Pawn:
	def __init__(self, color, location, moved=False):
		self.location = location
		self.color = color
		self.moved = moved
		if self.color == 1:
			self.image = 'Images/Chess_plt60.png'
		else: self.image = 'Images/Chess_pdt60.png'

	def all_moves(self, board):
		direction = -self.color
		moves = []
		up1 = (self.location[0]+direction, self.location[1])
		# can take this check out once promoting is in the game
		if up1[0] <= 7 and up1[0] >= 0 and board[up1[0]][up1[1]] == 0:
			moves.append([(self.location,up1)])
			up2 = (up1[0]+direction,up1[1])
			if not self.moved and board[up2[0]][up2[1]] == 0:
				moves.append([(self.location,up2)])
		if up1[1]-1 >= 0 and board[up1[0]][up1[1]-1] != 0 and board[up1[0]][up1[1]-1].color != self.color:
			moves.append([(self.location,(up1[0],up1[1]-1))])
		if up1[1]+1 <= 7 and board[up1[0]][up1[1]+1] != 0 and board[up1[0]][up1[1]+1].color != self.color:
			moves.append([(self.location,(up1[0],up1[1]+1))])
		return moves

	def value(self):
		if self.color == 1:
			return pawn_value[self.location[0]][self.location[1]]
		else: return pawn_value[7-self.location[0]][self.location[1]]

	def move(self, spot):
		self.location = spot
		self.moved = True

	def copy(self):
		return Pawn(self.color, self.location, self.moved)



default_white_king = King(1,(7,4))
default_black_king = King(-1,(0,4))

default_position = [
[Rook(-1,(0,0)),Knight(-1,(0,1)),Bishop(-1,(0,2)),Queen(-1,(0,3)),default_black_king,Bishop(-1,(0,5)),Knight(-1,(0,6)),Rook(-1,(0,7))],
[Pawn(-1,(1,0)),Pawn(-1,(1,1)),  Pawn(-1,(1,2)),  Pawn(-1,(1,3)), Pawn(-1,(1,4)),Pawn(-1,(1,5)),  Pawn(-1,(1,6)),  Pawn(-1,(1,7))],
[0,             0,               0,               0,              0,             0,               0,               0],
[0,             0,               0,               0,              0,             0,               0,               0],
[0,             0,               0,               0,              0,             0,               0,               0],
[0,             0,               0,               0,              0,             0,               0,               0],
[Pawn(1,(6,0)), Pawn(1,(6,1)),   Pawn(1,(6,2)),   Pawn(1,(6,3)),  Pawn(1,(6,4)), Pawn(1,(6,5)),   Pawn(1,(6,6)),   Pawn(1,(6,7))],
[Rook(1,(7,0)), Knight(1,(7,1)), Bishop(1,(7,2)), Queen(1,(7,3)), default_white_king, Bishop(1,(7,5)), Knight(1,(7,6)), Rook(1,(7,7))]]
default_white_pieces = []
default_black_pieces = []
for row in default_position:
	for piece in row:
		if piece != 0:
			if piece.color == 1:
				default_white_pieces.append(piece)
			else: default_black_pieces.append(piece)

def piece_sort(piece):
	return -piece.value()

default_white_pieces.sort(key=piece_sort)
default_black_pieces.sort(key=piece_sort)




class Position:
	def __init__(self, board=default_position, turn=1, lm=0, white_pieces=default_white_pieces, black_pieces=default_black_pieces, white_king=default_white_king, black_king=default_black_king):
		self.board = board
		self.turn = turn
		self.lm = lm
		self.white_pieces = white_pieces
		self.black_pieces = black_pieces
		self.white_king = white_king
		self.black_king = black_king

	def evaluate(self):
		evaluation = 0
		for piece in self.white_pieces:
			evaluation += piece.value()
			#evaluation += len(piece.all_moves(self.board))*random.randrange(0,20)*0.01
		for piece in self.black_pieces:
			evaluation -= piece.value()
			#evaluation -= len(piece.all_moves(self.board))*random.randrange(0,20)*0.01
		return random.uniform(0.9,1.1)*evaluation

	def sort_key(self,move):
		new = self.copy()
		new.move(move)
		return -new.evaluate()*self.turn

	def all_moves(self):
		if self.turn == 1:
			if self.white_pieces.count(self.white_king) == 0:
				return []
			piece_list = self.white_pieces
		else:
			if self.black_pieces.count(self.black_king) == 0:
				return []
			piece_list = self.black_pieces
		moves = []
		for piece in piece_list:
			piece_moves = piece.all_moves(self.board)
			for move in piece_moves:
				moves.append(move)
		return moves

	def pull_square(self,square):
		return self.board[square[0]][square[1]]

	def move(self, move):
		for mv in move:
			piece = self.pull_square(mv[0])
			end_square = self.pull_square(mv[1])
			if end_square != 0:
				if end_square.color == 1:
					self.white_pieces.remove(end_square)
				else: self.black_pieces.remove(end_square)
			if type(piece) == Pawn and (mv[1][0] == 0 or mv[1][0] == 7):
				queen = Queen(piece.color, piece.location)
				if self.turn == 1:
					self.white_pieces.append(queen)
					self.white_pieces.remove(piece)
				else:
					self.black_pieces.append(queen)
					self.black_pieces.remove(piece)
				piece = queen
			self.board[mv[1][0]][mv[1][1]] = piece
			self.board[mv[0][0]][mv[0][1]] = 0
			piece.move(mv[1])

		self.turn = -self.turn
		self.lm = [move]

	def copy(self):
		new_board = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
		
		for row in range(8):
			for column in range(8):
				if self.board[row][column] != 0:
					new_board[row][column] = self.board[row][column].copy()

		new_white_pieces = []
		new_black_pieces = []
		new_white_king = 0
		new_black_king = 0
		for row in new_board:
			for piece in row:
				if piece != 0:
					if piece.color == 1:
						new_white_pieces.append(piece)
						if type(piece) == King:
							new_white_king = piece
					else:
						new_black_pieces.append(piece)
						if type(piece) == King:
							new_black_king = piece

		return Position(new_board,self.turn,self.lm,new_white_pieces,new_black_pieces,new_white_king,new_black_king)









class Chess:
	def __init__(self, screen, position=Position()):
		self.screen = screen
		self.width = screen.get_width()
		self.height = screen.get_height()
		self.position = position
		self.victory = False
		self.selected_piece = 0
		self.legal_moves = []

	def draw_board(self):
		sx = self.width/8
		sy = self.height/8
		self.screen.fill(light_color)
		for row in range(8):
			if row % 2 == 0:
				offset = 1
			else: offset = 0
			for column in range(4):
				pygame.draw.rect(self.screen,dark_color,pygame.Rect(sx*(2*column+offset),sy*row,sx,sy))

		if self.position.lm != 0:
			for moves in self.position.lm:
				for move in moves:
					for square in move:
						pygame.draw.rect(self.screen,lm_color,pygame.Rect(sx*square[1],sy*square[0],sx,sy))

		for moves in self.legal_moves:
			for move in moves:
				pygame.draw.rect(self.screen,valid_color,pygame.Rect(sx*move[1][1],sy*move[1][0],sx,sy))

		
		# piece based drawing
		pieces = self.position.white_pieces + self.position.black_pieces
		for piece in pieces:
			image = pygame.transform.scale(pygame.image.load(piece.image),(sx,sy))
			self.screen.blit(image,(piece.location[1]*sx,piece.location[0]*sy))
		'''
		# board based drawing
		for row in range(8):
			for column in range(8):
				if self.position.board[row][column] != 0:
					piece = self.position.board[row][column]
					image = pygame.transform.scale(pygame.image.load(piece.image),(sx,sy))
					self.screen.blit(image,(piece.location[1]*sx,piece.location[0]*sy))
		'''

		pygame.display.flip()

	def copy(self):
		return Chess(self.screen, self.position.copy())

	def mouse_event(self,mx,my):
		row = math.floor(8*my/self.height)
		column = math.floor(8*mx/self.width)
		pos = (row, column)
		square = self.position.pull_square(pos)
		for moves in self.legal_moves:
			for move in moves:
				if move[1] == pos:
					self.move(moves)
					self.selected_piece = 0
					self.legal_moves = []
					return moves
		if square != 0 and square.color == self.position.turn:
			self.selected_piece = square
			self.legal_moves = square.all_moves(self.position.board)
		else:
			self.selected_piece = 0
			self.legal_moves = []
		return False

	def all_moves(self):
		moves = self.position.all_moves()
		if len(moves) == 0:
			self.victory == True
		return moves

	def move(self,move):
		self.position.move(move)
