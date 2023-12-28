import random

class RandomPlayAI:

	def __init__(self):
		pass

	def move(self, game):
		move_choices = game.all_moves()
		if len(move_choices) != 0:
			return random.choice(move_choices)
