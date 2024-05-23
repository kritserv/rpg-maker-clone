import pygame as pg

class PygameEvent:
	def __init__(self, game_size, scale_method):
		self.game_size = game_size
		self.running = True
		self.click = False
		self.keydown, self.keyup = False, False
		self.up, self.down, self.left, self.right = False, False, False, False
		self.interact, self.cancel = False, False
		if scale_method == "by windows width":
			self.scale_on_x_axis = True
		else:
			self.scale_on_x_axis = False

	def check_type(self, event) -> object or None:
		keydown, \
		keyup, \
		running, \
		click =	False, \
			True, \
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
				new_size = self.get_size_and_maintain_aspect_ratio(event)
				new_display = pg.Surface(new_size)
				return new_display
			else:
				return None
		self.keydown, \
		self.keyup, \
		self.running, \
		self.click = keydown, \
			keyup, \
			running, \
			click

	def get_size_and_maintain_aspect_ratio(self, event) -> tuple:
		if self.scale_on_x_axis:
			ratio = event.w / self.game_size[0]
			new_height = int(event.h / ratio)
			return (self.game_size[0], new_height)
		else:
			ratio = event.h / self.game_size[1]
			new_width = int(event.w / ratio)
			return (new_width, self.game_size[1])

	def check_arrow_key(self, event, key) -> None:
		up, down, left, right = False, False, False, False
		if self.keydown:
			if key == pg.K_UP:
				up = True
			elif key == pg.K_DOWN:
				down = True
			elif key == pg.K_LEFT:
				left = True
			elif key == pg.K_RIGHT:
				right = True
		elif self.keyup:
			if key == pg.K_UP or key == pg.K_DOWN or key == pg.K_LEFT or key == pg.K_RIGHT:
				up, down, left, right = False, False, False, False
		self.up, self.down, self.left, self.right = up, down, left, right

	def check_interact(self, event, key) -> None:
		interact = False
		if self.keydown:
			if key == pg.K_RETURN:
				interact = True
		elif self.keyup:
			if key == pg.K_z or key == pg.K_SPACE:
				interact = True
		self.interact = interact

	def check_cancel(self, event, key) -> None:
		cancel = False
		if self.keydown:
			if key == pg.K_ESCAPE:
				cancel = True
		elif self.keyup:
			if key == pg.K_x or key == pg.K_KP0:
				cancel = True
		self.cancel = cancel

	def check_quit_game(self, event, key) -> None:
		running = True
		if self.keydown:
			if key == pg.K_q and pg.key.get_mods() & pg.KMOD_CTRL: # Ctrl + Q
				running = False
			elif key == pg.K_F4 and pg.key.get_mods() & pg.KMOD_ALT:  # Alt + F4
				running = False
		self.running = running

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
			if new_size:
				return new_size
				break
			if key:
				self.check_quit_game(event, key)
				self.check_arrow_key(event, key)
				self.check_interact(event, key)
				self.check_cancel(event, key)
		return 0