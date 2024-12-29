import pygame as pg
from dataclasses import dataclass

@dataclass(slots=True, kw_only=True)
class PygameEvent:
	game_size: list
	keydown: bool = False
	keyup: bool = False
	running: bool = True

	def check_type(self, event):
		keydown, keyup, running = False, True, True
		if event.type == pg.KEYDOWN:
			keydown = True
		elif event.type == pg.KEYUP:
			keyup = True
		elif event.type == pg.QUIT:
			running = False
		else:
			if event.type == pg.VIDEORESIZE:
				new_size = self.get_size_and_maintain_aspect_ratio(event)
				new_display = pg.Surface(new_size)
				return new_display
			else:
				return None
		self.keydown, \
		self.keyup, \
		self.running = keydown, \
			keyup, \
			running

	def get_size_and_maintain_aspect_ratio(self, event) -> tuple:
	    # Scale On Width (still bug with drawing rpgmap)
		# ratio = event.w / self.game_size[0]
		# new_height = int(event.h / ratio)
		# return (self.game_size[0], new_height)

		# Scale On Height
		ratio = event.h / self.game_size[1]
		new_width = int(event.w / ratio)
		return (new_width, self.game_size[1])

	def check_quit_game(self, event, key) -> None:
		running = True
		if self.keydown:
			if key == pg.K_q and pg.key.get_mods() & pg.KMOD_CTRL: # Ctrl + Q
				running = False
			elif key == pg.K_F4 and pg.key.get_mods() & pg.KMOD_ALT:  # Alt + F4
				running = False
		self.running = running

	def check_key(self, event) -> bool:
		try:
			key = event.key
			return key
		except AttributeError:
			return False

	def check(self):
		for event in pg.event.get():
			key = self.check_key(event)
			new_size = self.check_type(event)
			if new_size:
				return new_size
				break
			if key:
				self.check_quit_game(event, key)
		return 0
