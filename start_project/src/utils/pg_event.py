import pygame as pg
from dataclasses import dataclass

@dataclass(slots=True, kw_only=True)
class PygameEvent:
	game_size: list
	keydown: bool = False
	keyup: bool = False
	running: bool = True
	game_state: int = -2
	is_save_state: bool = False
	is_load_state: bool = False

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
				event.w = max(event.w, self.game_size[0])
				event.h = max(event.h, self.game_size[1])
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

	def check_joystick(self, event):
		if event.type == pg.JOYDEVICEADDED:
			joy = pg.joystick.Joystick(event.device_index)
			return joy
		return False

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

	def check_game_state(self, key, joysticks) -> None:
		if self.keydown:
			if key == pg.K_ESCAPE or key == pg.K_KP0:  # Esc, Keypad 0
				if self.game_state == 0:
					self.game_state = 1
				elif self.game_state == 1:
					self.game_state = 0
		for joystick in joysticks:
			if joystick.get_button(10):
				if self.game_state == 0:
					self.game_state = 1
				elif self.game_state == 1:
					self.game_state = 0

	def check_key(self, event) -> bool:
		try:
			key = event.key
			return key
		except AttributeError:
			return False

	def check_pc(self, joysticks):
		for event in pg.event.get():
			key = self.check_key(event)
			new_size = self.check_type(event)
			joy = self.check_joystick(event)
			if new_size:
				return (new_size, joy)
			if key:
				self.check_quit_game(event, key)
				self.check_game_state(key, joysticks)
		return (False, False)

	def check_android(self, active_touches, image_controls):
		joy = False
		for event in pg.event.get():
			joy = self.check_joystick(event)
			if event.type == pg.FINGERDOWN or event.type == pg.FINGERMOTION:
				touch_pos = (event.x * self.game_size[0], event.y * self.game_size[1])
				for direction, (image, pos) in image_controls.items():
					image_rect = pg.Rect(pos[0], pos[1], image.get_width(), image.get_height())
					if image_rect.collidepoint(touch_pos):
						active_touches[event.finger_id] = direction
			elif event.type == pg.FINGERUP:
				if event.finger_id in active_touches:
					# Handle the SELECT action on touch release
					if active_touches[event.finger_id] == "SELECT":
						if self.game_state == 0:
							self.game_state = 1
						elif self.game_state == 1:
							self.game_state = 0
					del active_touches[event.finger_id]
			elif event.type == pg.QUIT:
				self.running = False

		mobile_key = {"K_UP": False, "K_LEFT": False, "K_RIGHT": False, "K_DOWN": False,
					"K_A": False, "K_B": False, "K_ESCAPE": False}
		for direction in active_touches.values():
			if direction == "UP":
				mobile_key["K_UP"] = True
			if direction == "LEFT":
				mobile_key["K_LEFT"] = True
			if direction == "RIGHT":
				mobile_key["K_RIGHT"] = True
			if direction == "DOWN":
				mobile_key["K_DOWN"] = True
			if direction == "A":
				mobile_key["K_A"] = True
			if direction == "B":
				mobile_key["K_B"] = True

		return (mobile_key, joy)
