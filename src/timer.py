from time import time

class Timer:
	def __init__(self):
		self.start_time, self.elapsed_time = 0, 0
		self.is_paused = True

	def start_or_resume(self) -> None:
		if self.is_paused:
			self.start_time = time()
			self.is_paused = False

	def start(self) -> None:
		self.start_or_resume()

	def resume(self) -> None:
		self.start_or_resume()

	def pause(self) -> None:
		if not self.is_paused:
			self.elapsed_time += time() - self.start_time
			self.is_paused = True

	def reset(self) -> None:
		self.start_time = 0
		self.elapsed_time = 0
		self.is_paused = True

	def restart(self) -> None:
		self.reset()
		self.start_or_resume()

	def toggle_pause(self) -> None:
		if self.is_paused:
			self.start_or_resume()
		else:
			self.pause()

	def now(self) -> float:
		if self.is_paused:
			return round(self.elapsed_time, 3)
		else:
			return round(self.elapsed_time + time() - self.start_time, 3)