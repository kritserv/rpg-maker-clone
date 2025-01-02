import pygame as pg
from math import floor, ceil
import os
from .timer import Timer

class Player(pg.sprite.Sprite):
	def __init__(self, full_path, xy):
		x, y = xy
		pg.sprite.Sprite.__init__(self)
		self.full_path = full_path

		self.levels = 0
		self.items = {}

		self.speed = 80
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

		self.direction = "bottom"
		self.animation_time = 0.09
		self.current_frame = 0

		self.rect = self.img.get_rect()

		self.pos = pg.math.Vector2([x, y])

		self.finish_pos = [self.pos[0], self.pos[1]]
		distant_to_finish_x, distant_to_finish_y = 0, 0
		self.finished_x_move = True
		self.finished_y_move = True
		self.last_dx, self.last_dy = 0, 0
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

	def calculate_val_from_key(self, key, mobile_key) -> (int, int):
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
			up = key[pg.K_UP]
			left = key[pg.K_LEFT]
			right = key[pg.K_RIGHT]
			down = key[pg.K_DOWN]
			cancel = key[pg.K_LSHIFT] or key[pg.K_RSHIFT] or key[pg.K_x]
			select = key[pg.K_ESCAPE]

		if cancel:
			self.speed = 90
			self.animation_time = 0.1
			self.is_running = True
		else:
			self.speed = 50
			self.animation_time = 0.19
			self.is_running = False

		if self.turn_around_timer.get_elapsed_time() > 1.15:
			self.turn_around_timer.pause()

		if left or right:
			if self.finished_y_move:
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
					self.last_dx = dx
					self.key_pressed = True
					self.finished_x_move = False

		elif up or down:
			if self.finished_x_move:
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
					self.last_dy = dy
					self.key_pressed = True
					self.finished_y_move = False
		else:
			self.turn_around_timer.restart()

		return dx, dy

	def make_divisible_by(self, tile_size, num) -> int:
		if num > 0:
			while num % tile_size != 0:
				num += 1
		elif num < 0:
			while num % tile_size != 0:
				num -= 1
		return num

	def expect_finish_pos(self, one_move) -> [int, int]:
		expect_pos = []
		for axis in [0, 1]:
			if axis == 1:
				last_val = self.last_dy
				pos = self.pos[1]
			else:
				last_val = self.last_dx
				pos = self.pos[0]

			if last_val > 0:
				check = ceil(pos)
			elif last_val < 0:
				check = floor(pos)
			else:
				check = 0

			if -one_move < check < one_move:
				expect_val = 0
			else:
				expect_val = self.make_divisible_by(16, check)

			expect_pos.append(expect_val)

		return expect_pos

	def calculate_distant_to_finish(self, one_move) -> (float, float):
		distant_to_finish_x = self.pos[0] - self.finish_pos[0]
		distant_to_finish_y = self.pos[1] - self.finish_pos[1]

		if distant_to_finish_x < one_move:
			distant_to_finish_x *= -1
		if distant_to_finish_y < one_move:
			distant_to_finish_y *= -1

		return distant_to_finish_x, distant_to_finish_y

	def move(self, dx, dy, dt) -> None:
		self.pos[0] += dx * self.speed * dt
		self.pos[1] += dy * self.speed * dt
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

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

	def move_to_finish_pos(self, dt, one_move, ease_out) -> None:
		distant_to_finish_x ,\
		distant_to_finish_y = self.calculate_distant_to_finish(one_move)

		if ease_out:
			if distant_to_finish_x > one_move:
				if self.direction == "left":
					if not self.pos[0] - one_move < self.finish_pos[0]:
						self.move(self.last_dx, 0, dt)
					else:
						self.move(self.last_dx*0.37, 0, dt)
				elif self.direction == "right":
					if not self.pos[0] + one_move < self.finish_pos[0]:
						self.move(self.last_dx, 0, dt)
					else:
						self.move(self.last_dx*0.37, 0, dt)

			if distant_to_finish_y > one_move:
				if self.direction == "top":
					if not self.pos[1] + one_move < self.finish_pos[1]:
						self.move(0, self.last_dy, dt)
					else:
						self.move(0, self.last_dy*0.37, dt)
				elif self.direction == "bottom":
					if not self.pos[1] - one_move < self.finish_pos[1]:
						self.move(0, self.last_dy, dt)
					else:
						self.move(0, self.last_dy*0.37, dt)

		else:
			if distant_to_finish_x > one_move:
				self.move(self.last_dx, 0, dt)
			if distant_to_finish_y > one_move:
				self.move(0, self.last_dy, dt)

		if distant_to_finish_x <= one_move:
			self.pos[0] = self.finish_pos[0]
			self.rect.x = self.pos[0]
			self.finished_x_move = True
		if distant_to_finish_y <= one_move:
			self.pos[1] = self.finish_pos[1]
			self.rect.y = self.pos[1]
			self.finished_y_move = True


	def update(self, key, dt, mobile_key={}) -> None:
		dx, dy = self.calculate_val_from_key(key, mobile_key)

		one_move = self.speed * dt

		self.finish_pos = self.expect_finish_pos(one_move)

		if self.key_pressed:
			self.move(dx, dy, dt)

		is_idle = self.finished_x_move and self.finished_y_move

		ease_out = False
		if dt > 0.018:
			ease_out = True

		if not self.key_pressed:
			self.move_to_finish_pos(
				dt,
				one_move,
				ease_out
				)

		self.animate(is_idle, dt)
