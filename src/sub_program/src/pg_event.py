import pygame as pg

class PygameEvent:
	def __init__(self):
		self.running = True
		self.click = False
		self.keydown, self.keyup = False, False
		self.need_input = True
		self.user_input = ""

	def check_type(self, event) -> object or None:
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

	def check_unicode(self, key, event) -> None:
		if self.need_input and key:
			if self.keydown:
				if key == pg.K_BACKSPACE:
					self.user_input = self.user_input[:-1]
					pg.time.set_timer(pg.USEREVENT, 75)
				else:
					self.user_input += event.unicode

			elif self.keyup:
				if key == pg.K_BACKSPACE:
					pg.time.set_timer(pg.USEREVENT, 0)

	def check_key(self, event) -> int or bool:
		try:
			key = event.key
			return key
		except AttributeError:
			return False

	def check(self) -> object or int:
		for event in pg.event.get():
			key = self.check_key(event)
			new_size = self.check_type(event)
			self.check_unicode(key, event)

			if event.type == pg.USEREVENT:
				self.user_input = self.user_input[:-1]

			if new_size:
				return new_size
			if key:
				self.check_quit_game(event, key)

		return 0