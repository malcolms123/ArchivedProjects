import time,math

inf = 1000

class MinimaxAI:

	def __init__(self, depth, timer=False, evaluation=False, lines=False, progress=False, signature = '', dynamic_depth=False):
		self.depth = depth
		self.timer = timer
		self.evaluation = evaluation
		self.lines = lines
		self.progress = progress
		self.signature = signature
		self.dynamic_depth = dynamic_depth

	def move(self, game):
		# preparing timer
		start_time = time.time()
		# saving turn value and calculating all moves
		turn = game.position.turn
		options = game.all_moves()
		# exiting if no available moves
		if len(options) == 0:
			return
		total_moves = len(options)
		new_depth = self.depth - 1
		# calculating and removing first node
		new_game = game.copy()
		new_game.move(options[0])
		values = [self.alphabeta(new_game,new_depth,-inf,inf,-turn)*turn]
		move_counter = 1
		ordered_options = [options[0]]
		options.pop(0)
		if self.progress:
			print('\nSearched ' + str(move_counter) + ' of ' + str(total_moves) + ' moves.')
		for option in options:
			# calculating subsequent nodes
			new_game = game.copy()
			new_game.move(option)
			new_value = self.alphabeta(new_game,new_depth,-inf,inf,-turn)*turn

			inserted = False
			for index in range(len(values)):
				if new_value > values[index]:
					values.insert(index,new_value)
					ordered_options.insert(index,option)
					inserted = True
					break
			if not inserted:
				values.append(new_value)
				ordered_options.append(option)

			move_counter += 1
			if self.progress:
				print('Searched ' + str(move_counter) + ' of ' + str(total_moves) + ' moves.')

		if self.timer or self.evaluation or self.lines:
			print('\n-----MOVE DETAILS-----' + self.signature)
		if self.timer:
			print('Calculation Time: %s seconds' % round(time.time()-start_time,5))
		if self.evaluation:
			print('Move Evaluation: %s' % round(values[0],5))
		if self.lines:
			print('1. %s   Evaluation: %s' % (ordered_options[0], round(values[0],5)))
			if len(values) > 1:
				print('2. %s   Evaluation: %s' % (ordered_options[1], round(values[1])))
			if len(values) > 2:
				print('3. %s   Evaluation: %s' % (ordered_options[2], round(values[2])))
		return ordered_options[0]

	def alphabeta(self,game,depth,alpha,beta,turn):
		options = game.all_moves()
		if depth == 0 or len(options) == 0:
			return game.position.evaluate()
		if turn == 1:
			value = -inf
			for option in options:
				new_game = game.copy()
				new_game.move(option)
				value = max([value, self.alphabeta(new_game,depth-1,alpha,beta,-1)])
				if value >= beta:
					break
				alpha = max([alpha,value])
			return value
		else:
			value = inf
			for option in options:
				new_game = game.copy()
				new_game.move(option)
				value = min([value,self.alphabeta(new_game,depth-1,alpha,beta,1)])
				if value <= alpha:
					break
				beta = min([beta,value])
			return value

