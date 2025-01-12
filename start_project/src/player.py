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
		self.animation_time = 0.09
		self.current_frame = 0

		self.rect = self.img.get_rect()

		self.pos = pg.math.Vector2(xy)

		self.last_dir = pg.math.Vector2(0, 0)
		self.key_pressed = False

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
		dx = 0
		dy = 0
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
			self.speed = 90
			if dt > 0.33:
				self.speed = 70
			self.animation_time = 0.1
			self.is_running = True
		else:
			self.speed = 60
			if dt > 0.33:
				self.speed = 45
			self.animation_time = 0.19
			self.is_running = False

		if self.turn_around_timer.get_elapsed_time() > 1.15:
			self.turn_around_timer.pause()

		if left or right:
			if left:
				if cancel:
					dx = -1
					self.direction = "left"
				else:
					if self.direction == "left" and self.turn_around_timer.get_elapsed_time() <= 0.9:
						dx = -1
					else:
						self.direction = "left"
						self.turn_around_timer.elapsed_time = 0.9

			elif right:
				if cancel:
					dx = 1
					self.direction = "right"
				else:
					if self.direction == "right" and self.turn_around_timer.get_elapsed_time() <= 0.9:
						dx = 1
					else:
						self.direction = "right"
						self.turn_around_timer.elapsed_time = 0.9

			if left and right:
				self.direction = "bottom"
				dx = 0

			if dx != 0:
				self.last_dir.x = dx
				self.key_pressed = True

		elif up or down:
			if up:
				if cancel:
					dy = -1
					self.direction = "top"
				else:
					if self.direction == "top" and self.turn_around_timer.get_elapsed_time() <= 0.9:
						dy = -1
					else:
						self.direction = "top"
						self.turn_around_timer.elapsed_time = 0.9

			elif down:
				if cancel:
					dy = 1
					self.direction = "bottom"
				else:
					if self.direction == "bottom" and self.turn_around_timer.get_elapsed_time() <= 0.9:
						dy = 1
					else:
						self.direction = "bottom"
						self.turn_around_timer.elapsed_time = 0.9

			if up and down:
				self.direction = "bottom"
				dy = 0

			if dy != 0:
				self.last_dir.y = dy
				self.key_pressed = True
		else:
			self.turn_around_timer.restart()

		return dx, dy

	def move(self, dx, dy, dt, collision_rects) -> None:
		direction = pg.math.Vector2(dx, dy)
		next_move = self.pos + (direction * self.speed * dt)
		self.pos = next_move
		self.rect.topleft = self.pos

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

	def check_obstacles(self, collision_rects):
		next_move = []
		if self.direction == "top":
			next_move = self.collision_border_top

		elif self.direction == "bottom":
			next_move = self.collision_border_bottom

		elif self.direction == "left":
			next_move = self.collision_border_left

		elif self.direction == "right":
			next_move = self.collision_border_right

		can_move = True
		for collision_rect in collision_rects:
			if next_move:
				if pg.Rect.colliderect(collision_rect, next_move):
					can_move = False
					return can_move
		return can_move

	def update(self, key, dt, mobile_key={}, joysticks=[], collision_rects=[]) -> None:
		dx, dy = self.calculate_val_from_key(key, mobile_key=mobile_key, joysticks=joysticks, dt=dt)
		can_move = self.check_obstacles(collision_rects)
		if self.key_pressed:
			is_idle = False
			if can_move:
				self.move(dx, dy, dt, collision_rects)
		else:
			is_idle = True
			self.rect.topleft = self.pos

		self.animate(is_idle, dt)
