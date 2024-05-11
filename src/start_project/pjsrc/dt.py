from time import time

class DeltaTime:
	def __init__(self):
		self.now = time()
		self.prev = time()

	def get(self):
		self.now = time() - self.prev
		self.prev = time()
		return self.now