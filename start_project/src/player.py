from sys import _current_frames
import pygame as pg
from math import floor, ceil
import os
from .timer import Timer

class Player(pg.sprite.Sprite):
	def __init__(self, full_path, xy):
		pg.sprite.Sprite.__init__(self)
		self.full_path = full_path

		self.levels = 0
		self.items = {}

		self.speed = 50
		self.is_running = False

		self.imgs = {
			"bottom": [],
			"top": [],
			"left": [],
			"right": [],
			"running_bottom": [],
			"running_top": [],
			"running_left": [],
			"running_right": [],
			}
		self.load_sprites()

		self.current_img = 0
		self.img = self.imgs["bottom"][self.current_img]
		self.collision_border_right = []
		self.collision_border_left = []
		self.collision_border_top = []
		self.collision_border_bottom = []

		self.direction = "bottom"
		self.remembered_obstacle_pos = {}
		self.animation_time = 0.09


		self.walk_buffer = 50
		self.pos = pg.math.Vector2(xy)
		self.dirvec = pg.math.Vector2(0, 0)
		self.last_pos = self.pos
		self.next_pos = self.pos

		self.current_frame = 0
		self.last_update = pg.time.get_ticks()
		self.between_tiles = False

		self.image = pg.Surface((16, 16))
		self.image.fill((255, 0, 0))
		self.rect = self.image.get_rect()

		self.turn_around_timer = Timer()
		self.turn_around_timer.start()

	def load_sprites(self) -> None:
		load_spritesheet = pg.image.load(
			f"{self.full_path}assets/img/sprite/player.png"
			)
		sprite_width = 16
		sprite_height = 24
		directions = [
		    "bottom",
			"top",
			"left",
			"right",
			"running_bottom",
			"running_top",
			"running_left",
			"running_right"
			]
		frames = [
			"stand_still",
			"left_leg_forward",
			"right_leg_forward"
			]
		for row, direction in enumerate(directions):
			for i, frame in enumerate(frames):
				img = pg.Surface(
					(sprite_width, sprite_height)
					)
				img.fill((255, 0, 255))
				img.blit(
					load_spritesheet,
					(0, 0),
					(
						i*sprite_width,
						row*sprite_height,
						sprite_width,
						sprite_height
					)
				)
				img.set_colorkey((255, 0, 255))
				img = img.convert_alpha()
				self.imgs[direction].append(img)
				if frame == "left_leg_forward":
					self.imgs[direction].append(
						self.imgs[direction][0]
						)

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
			cancel = key[pg.K_LSHIFT] or key[pg.K_RSHIFT] or key[pg.K_x] or key[pg.K_KP_0]
			select = key[pg.K_ESCAPE]
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
			self.speed = 130
			self.animation_time = 0.1
			self.is_running = True
		else:
			self.speed = 80
			self.animation_time = 0.19
			self.is_running = False

		if self.turn_around_timer.get_elapsed_time() > 1.15:
			self.turn_around_timer.pause()

		if now - self.last_update > self.walk_buffer:
			self.last_update = now

			new_dir_vec = pg.math.Vector2(0, 0)
			if self.dirvec.y == 0:
				if left:
					if cancel:
						self.direction = "left"
						new_dir_vec = pg.math.Vector2(-1, 0)
					else:
						if self.direction == "left" and self.turn_around_timer.get_elapsed_time() <= 0.9:
							new_dir_vec = pg.math.Vector2(-1, 0)
						else:
							self.direction = "left"
							self.turn_around_timer.elapsed_time = 0.9

				elif right:
					if cancel:
						self.direction = "right"
						new_dir_vec = pg.math.Vector2(1, 0)
					else:
						if self.direction == "right" and self.turn_around_timer.get_elapsed_time() <= 0.9:
							new_dir_vec = pg.math.Vector2(1, 0)
						else:
							self.direction = "right"
							self.turn_around_timer.elapsed_time = 0.9

			if self.dirvec.x == 0:
				if up:
					if cancel:
						self.direction = "top"
						new_dir_vec = pg.math.Vector2(0, -1)
					else:
						if self.direction == "top" and self.turn_around_timer.get_elapsed_time() <= 0.9:
							new_dir_vec = pg.math.Vector2(0, -1)
						else:
							self.direction = "top"
							self.turn_around_timer.elapsed_time = 0.9

				elif down:
					if cancel:
						self.direction = "bottom"
						new_dir_vec = pg.math.Vector2(0, 1)
					else:
						if self.direction == "bottom" and self.turn_around_timer.get_elapsed_time() <= 0.9:
							new_dir_vec = pg.math.Vector2(0, 1)
						else:
							self.direction = "bottom"
							self.turn_around_timer.elapsed_time = 0.9
			else:
				self.turn_around_timer.restart()

			if new_dir_vec != pg.math.Vector2(0, 0):
				self.dirvec = new_dir_vec
				self.between_tiles = True
				current_index = self.rect.centerx // 16, self.rect.centery // 16
				self.last_pos = pg.math.Vector2(current_index) * 16
				self.next_pos = self.last_pos + self.dirvec * 16

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
		self.rect = self.image.get_rect()
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
					self.rect.topleft = self.pos
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
