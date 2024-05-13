import pygame as pg
from math import floor, ceil

class Player(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)

		self.speed = 90

		self.imgs = {
			"bottom": [],
			"top": [],
			"left": [],
			"right": []
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
		self.diff_x, self.diff_y = 0, 0
		self.finished_x_move = True
		self.finished_y_move = True
		self.last_dx, self.last_dy = 0, 0
		self.key_pressed = False

	def load_sprites(self):
		load_spritesheet = pg.image.load(
			"assets/img/player.png"
			)
		sprite_width = 16
		sprite_height = 24
		directions = [
			"bottom", 
			"top", 
			"left", 
			"right"
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

	def calculate_val_from_key(self, key):
		dx = 0
		dy = 0
		self.key_pressed = False
		
		if key[pg.K_LEFT] or key[pg.K_RIGHT]:
			if self.finished_y_move:
				if key[pg.K_LEFT]:
					self.direction = "left"
					dx = -1

				elif key[pg.K_RIGHT]:
					self.direction = "right"
					dx = 1

				if dx != 0:
					self.last_dx = dx
					self.key_pressed = True
					self.finished_x_move = False

		elif key[pg.K_UP] or key[pg.K_DOWN]:
			if self.finished_x_move:
				if key[pg.K_UP]:
					self.direction = "top"
					dy = -1

				elif key[pg.K_DOWN]:
					self.direction = "bottom"
					dy = 1

				if dy != 0:
					self.last_dy = dy
					self.key_pressed = True
					self.finished_y_move = False
		
		return dx, dy

	def make_divisible_by_16(self, num):
		if num > 0:
			while num % 16 != 0:
				num += 1
		elif num < 0:
			while num % 16 != 0:
				num -= 1
		return num

	def expect_finish_x_pos(self, one_move):

		if self.last_dx < 0:
			check = floor(self.pos[0])
		elif self.last_dx > 0:
			check = ceil(self.pos[0])
		else:
			check = 0

		if -one_move < check < one_move:
			expect_x = 0
		else:
			expect_x = self.make_divisible_by_16(check)

		return expect_x

	def expect_finish_y_pos(self, one_move, tile_size=16):

		if self.last_dy < 0:
			check = floor(self.pos[1])
		elif self.last_dy > 0:
			check = ceil(self.pos[1])
		else:
			check = 0

		if -one_move < check < one_move:
			expect_y = 0
		else:
			expect_y = self.make_divisible_by_16(check)

		return expect_y

	def move(self, dx, dy, dt):
		self.pos[0] += dx * self.speed * dt
		self.pos[1] += dy * self.speed * dt
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

	def animate(self, idle, dt):

		if idle:
			self.current_img = 0

		else:
			self.current_frame += dt
			if self.current_frame >= self.animation_time:
				self.current_frame -= self.animation_time
				self.current_img = (self.current_img + 1) % len(self.imgs[self.direction])
		self.img = self.imgs[self.direction][self.current_img]

	def update(self, key, dt):
		dx, dy = self.calculate_val_from_key(key)

		if self.key_pressed:
			self.move(dx, dy, dt)

		idle = not dx and not dy

		one_move = self.speed * dt
		if one_move == 0.0:
			one_move = 0.01

		if not self.key_pressed:
			self.finish_pos[0]= self.expect_finish_x_pos(one_move)
			self.finish_pos[1] =  self.expect_finish_y_pos(one_move)

			if self.finish_pos[0]<= self.pos[0]:
				self.diff_x = self.pos[0]- self.finish_pos[0]
			else:
				self.diff_x = self.finish_pos[0]- self.pos[0]

			if self.finish_pos[1] <= self.pos[1]:
				self.diff_y = self.pos[1] - self.finish_pos[1]
			else:
				self.diff_y = self.finish_pos[1] - self.pos[1]

			if self.diff_x > one_move:
				self.move(self.last_dx, 0, dt)
			elif self.diff_x <= one_move:
				self.pos[0]= self.finish_pos[0]
				self.finished_x_move = True

			if self.diff_y > one_move:
				self.move(0, self.last_dy, dt)
			elif self.diff_y <= one_move:
				self.pos[1] = self.finish_pos[1]
				self.finished_y_move = True

		self.animate(idle, dt)
