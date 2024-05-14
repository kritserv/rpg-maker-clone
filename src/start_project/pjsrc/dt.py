from time import time

class DeltaTime:
	def __init__(self):
		self.prev = time()

	def get(self):
		now = time()
		delta = now - self.prev
		self.prev = now
		return delta
