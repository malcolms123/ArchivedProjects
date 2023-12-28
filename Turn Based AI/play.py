import pygame, time
from Games.TicTacToe.GameTTT import *
from Games.Chess.GameChess import *
from Games.ConnectFour.GameConnectFour import *
from AIs.Minimax import *

size = 1000,1000

pygame.init()
screen = pygame.display.set_mode(size)


game = Chess(screen) # choose the game being played


ai = MinimaxAI(4,evaluation=True,progress=True,timer=True)


players = [0,ai]
current_player = 0

running = True
game.draw_board()
move_list = []

while running:
	if players[current_player] != 0:
		move = players[current_player].move(game)
		if move is not None:
			game.move(move)
			move_list.append(move)
			if current_player == 0:
				current_player = 1
			else: current_player = 0
			game.draw_board()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN and players[current_player] == 0 and not game.victory:
			mx,my = pygame.mouse.get_pos()
			moved = game.mouse_event(mx,my)
			if moved:
				move_list.append(moved)
				if current_player == 0:
					current_player = 1
				else: current_player = 0
			game.draw_board()


print(move_list)