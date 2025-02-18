import pygame as pg
from ..utils import asset_loader
from math import floor, ceil

class Player(pg.sprite.Sprite):
	def __init__(self, xy, player_img):
		pg.sprite.Sprite.__init__(self)
		self.start_position = xy

		self.levels = 0
		self.items = {}
		self.variables = {}
		self.clear_commands = []

		self.skill_dict = {}
		self.skills = []

		self.speed = 50
		self.is_running = False
		self.imgs = player_img

		self.current_img = 0
		self.img = self.imgs["bottom"][self.current_img]

		# this stackoverflow answer is very helpful in implement tile base movement and collision
		# https://stackoverflow.com/questions/74332401/how-to-make-a-collision-system-in-pygame
		self.collision = []

		self.direction = "bottom"
		self.remembered_obstacle_pos = {}
		self.animation_time = 0.09


		self.walk_buffer = 80
		self.pos = pg.math.Vector2(xy)
		self.dirvec = pg.math.Vector2(0, 0)
		self.last_pos = self.pos
		self.next_pos = self.pos
		self.focus_point = self.pos

		self.current_frame = 0
		self.last_update = pg.time.get_ticks()
		self.between_tiles = False

		self.image = pg.Surface((16, 16))
		self.image.fill((255, 0, 0))
		self.rect = self.image.get_rect()

	def start_new_game(self):
		self.pos = pg.math.Vector2(self.start_position)
		self.dirvec = pg.math.Vector2(0, 0)
		self.last_pos = self.pos
		self.next_pos = self.pos
		self.focus_point = self.pos
		self.direction = "bottom"

		self.levels = 0
		self.items = {}
		self.variables = {}
		self.clear_commands = []
		self.skills = []

		self.speed = 50
		self.is_running = False

	def calculate_val_from_key(self, key, mobile_key={}, joysticks=[], dt=0.016):
		now = pg.time.get_ticks()
		self.key_pressed = False

		if mobile_key:
			up = mobile_key["K_UP"]
			left = mobile_key["K_LEFT"]
			right = mobile_key["K_RIGHT"]
			down = mobile_key["K_DOWN"]
			cancel = mobile_key["K_B"]
			select = mobile_key["K_ESCAPE"]
		else:
			up = key[pg.K_UP] or key[pg.K_w]
			left = key[pg.K_LEFT] or key[pg.K_a]
			right = key[pg.K_RIGHT] or key[pg.K_d]
			down = key[pg.K_DOWN] or key[pg.K_s]
			cancel = key[pg.K_LSHIFT] or key[pg.K_RSHIFT] or key[pg.K_x]
			select = key[pg.K_ESCAPE] or key[pg.K_KP_0]
		for joystick in joysticks:
			up, left, right, down, cancel, select = False, False, False, False, False, False
			if joystick.get_axis(0) < -0.6:
				left = True
			elif joystick.get_axis(0) > 0.6:
				right = True
			elif joystick.get_axis(1) < -0.6:
				up = True
			elif joystick.get_axis(1) > 0.6:
				down = True
			if joystick.get_button(1):
				cancel = True
			if joystick.get_button(10):
				select = True

		if cancel:
			self.speed = 100
			self.animation_time = 0.1
			self.is_running = True
			self.walk_buffer = 50
		else:
			self.speed = 60
			self.animation_time = 0.14
			self.is_running = False
			self.walk_buffer = 80

		if now - self.last_update > self.walk_buffer:
			self.last_update = now

			new_dir_vec = pg.math.Vector2(0, 0)
			if self.dirvec.y == 0:
				if left:
					if cancel:
						self.direction = "left"
						new_dir_vec = pg.math.Vector2(-1, 0)
					else:
						if self.direction == "left":
							new_dir_vec = pg.math.Vector2(-1, 0)
						else:
							self.direction = "left"

				elif right:
					if cancel:
						self.direction = "right"
						new_dir_vec = pg.math.Vector2(1, 0)
					else:
						if self.direction == "right":
							new_dir_vec = pg.math.Vector2(1, 0)
						else:
							self.direction = "right"

			if self.dirvec.x == 0:
				if up:
					if cancel:
						self.direction = "top"
						new_dir_vec = pg.math.Vector2(0, -1)
					else:
						if self.direction == "top":
							new_dir_vec = pg.math.Vector2(0, -1)
						else:
							self.direction = "top"

				elif down:
					if cancel:
						self.direction = "bottom"
						new_dir_vec = pg.math.Vector2(0, 1)
					else:
						if self.direction == "bottom":
							new_dir_vec = pg.math.Vector2(0, 1)
						else:
							self.direction = "bottom"

			if new_dir_vec != pg.math.Vector2(0, 0):
				self.dirvec = new_dir_vec
				self.between_tiles = True
				current_index = self.rect.centerx // 16, self.rect.centery // 16
				self.last_pos = pg.math.Vector2(current_index) * 16
				self.next_pos = self.last_pos + self.dirvec * 16

		match self.direction:
			case 'top':
				focus = pg.math.Vector2(0, -1)
			case 'bottom':
				focus = pg.math.Vector2(0, 1)
			case 'left':
				focus = pg.math.Vector2(-1, 0)
			case 'right':
				focus = pg.math.Vector2(1, 0)
			case _:
				focus = pg.math.Vector2(0, 0)
		self.focus_point = self.pos + focus * 16

	def animate(self, is_idle, dt) -> None:
		if is_idle:
			self.current_img = 0

		else:
			self.current_frame += dt
			if self.current_frame >= self.animation_time:
				self.current_frame -= self.animation_time
				self.current_img = (self.current_img + 1) % len(self.imgs[self.direction])
		self.img = self.imgs[self.direction][self.current_img]
		if self.is_running:
		      self.img = self.imgs['running_'+self.direction][self.current_img]

	def update(self, key, dt, mobile_key={}, joysticks=[], collision_rects=[]) -> None:
		self.calculate_val_from_key(key, mobile_key=mobile_key, joysticks=joysticks, dt=dt)
		is_idle = True
		if self.pos != self.next_pos:
			is_idle = False

			delta = self.next_pos - self.pos
			if delta.length() > (self.dirvec * self.speed * dt).length():
				if self.remembered_obstacle_pos.get((self.pos.x, self.pos.y), '') != self.direction:
					self.pos += self.dirvec * self.speed * dt
				else:
					self.pos = self.last_pos
					self.next_pos = self.last_pos
					self.dirvec = pg.math.Vector2(0, 0)
					self.between_tiles = False
			else:
				self.pos = self.next_pos
				self.dirvec = pg.math.Vector2(0, 0)
				self.between_tiles = False

		self.rect.topleft = self.pos

		# check collision
		for rect in collision_rects:
			if self.collision.colliderect(rect):
				if (self.last_pos.x, self.last_pos.y) not in self.remembered_obstacle_pos:
					self.remembered_obstacle_pos[(self.last_pos.x, self.last_pos.y)] = self.direction
				self.pos = self.last_pos
				self.next_pos = self.last_pos
				self.dirvec = pg.math.Vector2(0, 0)
				self.between_tiles = False
				self.rect.topleft = self.pos
				break

		self.animate(is_idle, dt)
