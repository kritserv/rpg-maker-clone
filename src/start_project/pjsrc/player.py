import pygame as pg

class Player(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)

		self.speed = 220

		self.images = {
			"bottom": [],
			"top": [],
			"left": [],
			"right": []
			}
		self.load_sprites()

		self.current_image = 0
		self.image = self.images["bottom"][self.current_image]

		self.direction = "bottom"
		self.animation_time = 0.15
		self.current_frame = 0

		self.rect = self.image.get_rect()

		self.pos = pg.math.Vector2(self.rect.topleft)
		self.pos[0] = x
		self.pos[1] = y

	def load_sprites(self):
		load_spritesheet = pg.image.load("asset/img/player.png")
		sprite_width = 16
		sprite_height = 24
		directions = ["bottom", "top", "left", "right"]
		for row, direction in enumerate(directions):
			for column in range(4):
				image = pg.Surface((sprite_width, sprite_height))
				image.fill((255, 0, 255))
				image.blit(load_spritesheet, (0, 0), (column*sprite_width, row*sprite_height, sprite_width, sprite_height))
				image.set_colorkey((255, 0, 255))
				image = pg.transform.scale(image, (48, 64))
				image = image.convert_alpha()
				self.images[direction].append(image)

	def calculate_value_from_key_pressed(self, key, display):
		dx = 0
		dy = 0
		
		if key[pg.K_LEFT]:
			self.direction = "left"
			if self.rect.left > 0:
				dx = -1

		elif key[pg.K_RIGHT]:
			self.direction = "right"
			if self.rect.right < display.get_width():
				dx = 1

		elif key[pg.K_UP]:
			self.direction = "top"
			if self.rect.top > 70:
				dy = -1

		elif key[pg.K_DOWN]:
			self.direction = "bottom"
			if self.rect.bottom < display.get_height():
				dy = 1
		
		return dx, dy

	def move(self, dx, dy, dt):
		self.pos.x += dx * self.speed * dt
		self.rect.x = round(self.pos.x)
		self.pos.y += dy * self.speed * dt
		self.rect.y = round(self.pos.y)

	def animate(self, dx, dy, dt):
		if dx == 0 and dy == 0:
			self.current_image = 0
		else:
			self.current_frame += dt
			if self.current_frame >= self.animation_time:
				self.current_frame -= self.animation_time
				self.current_image = (self.current_image + 1) % len(self.images[self.direction])
		self.image = self.images[self.direction][self.current_image]

	def update(self, key, dt, display):
		dx, dy = self.calculate_value_from_key_pressed(key, display)
		self.move(dx, dy, dt)
		self.animate(dx, dy, dt)