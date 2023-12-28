import threading, tqdm

# class for handling threading
class ThreadHandler():
	def __init__(self):
		# this max threads value will be different for all computers
		# 1000 is a lowball estimate to prevent errors, higher means faster scanning
		self.maxThreads = 1000
		self.initialThreads = threading.active_count()

	# attempt to add a thread
	def add(self, target, args, name):
		# trying repeatedly until success
		notAdded = True
		while notAdded:
			# check if extra threads available
			if self.maxThreads > threading.active_count():
				# add thread
				notAdded = False
				try:
					newThread = threading.Thread(target=target, args=args, name=name)
					newThread.start()
				except Exception as e:
					print(e)

	def join(self, nPersistant):
		# Wait for all the threads to finish
		while (nPersistant + self.initialThreads) < threading.active_count():
			pass