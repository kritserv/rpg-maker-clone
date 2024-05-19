from time import time

class DeltaTime:
	def __init__(self):
		self.prev = time()

	def get(self) -> float:
		now = time()
		delta = now - self.prev
		self.prev = now
		return delta
