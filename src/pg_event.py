import pygame as pg

class PygameEvent:
	def __init__(self):
		self.running = True

	def check_type(self, event):
		keydown, keyup, quit = False, False, False
		if event.type == pg.KEYDOWN:
			keydown = True
		elif event.type == pg.KEYUP:
			keyup = True
		elif event.type == pg.QUIT:
			quit = True
		return keydown, keyup, quit

	def check_quit_game(self, event, quit, keydown):
		running = True
		if quit:
			running = False
		if keydown:
			if event.key == pg.K_q and pg.key.get_mods() & pg.KMOD_CTRL: # Ctrl + Q
				running = False
			elif event.key == pg.K_F4 and pg.key.get_mods() & pg.KMOD_ALT:  # Alt + F4
				running = False

		return running

	def check(self):
		for event in pg.event.get():
			keydown, keyup, quit = self.check_type(event)
			self.running = self.check_quit_game(event, quit, keydown)