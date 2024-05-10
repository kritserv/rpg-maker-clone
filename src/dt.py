from time import time

class DeltaTime:
	def __init__(self):
		self.now = None
		self.prev = time()

	def get(self):
		self.now = time() - self.prev
		self.prev = time()