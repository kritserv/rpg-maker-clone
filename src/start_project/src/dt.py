from time import time
from dataclasses import dataclass

@dataclass(slots=True)
class DeltaTime:
	prev: float = time()

	def get(self) -> float:
		now = time()
		delta = now - self.prev
		self.prev = now
		return delta
