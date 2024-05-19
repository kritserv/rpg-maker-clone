import pygame as pg

class PygameEvent:
	def __init__(self, game_size):
		self.game_size = game_size
		self.running = True
		self.click = False
		self.keydown, self.keyup = False, False

	def check_type(self, event) -> object:
		keydown, \
		keyup, \
		running , \
		click = False, \
			False, \
			True, \
			False
		if event.type == pg.KEYDOWN:
			keydown = True
		elif event.type == pg.KEYUP:
			keyup = True
		elif event.type == pg.QUIT:
			running = False
		elif event.type == pg.MOUSEBUTTONDOWN:
			click = True
		elif event.type == pg.MOUSEBUTTONUP:
			click = False
		else:
			if event.type == pg.VIDEORESIZE:
				new_size = pg.Surface((event.w, event.h))
				return new_size
			else:
				return None

		self.keydown, \
		self.keyup, \
		self.running, \
		self.click = keydown, \
			keyup, \
			running, \
			click

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

	def check(self) -> object:
		for event in pg.event.get():
			key = self.check_key(event)
			new_size = self.check_type(event)
			if new_size:
				return new_size
			if key:
				self.check_quit_game(event, key)

		return 0