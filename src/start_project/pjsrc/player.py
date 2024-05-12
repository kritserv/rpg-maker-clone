import pygame as pg

class Player(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)

		self.speed = 220

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
		self.animation_time = 0.15
		self.current_frame = 0

		self.rect = self.img.get_rect()

		self.pos = pg.math.Vector2(self.rect.topleft)
		self.pos[0] = x
		self.pos[1] = y

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
				img = pg.transform.scale(img, (48, 64))
				img = img.convert_alpha()
				self.imgs[direction].append(img)
				if frame == "left_leg_forward":
					self.imgs[direction].append(
						self.imgs[direction][0]
						)

	def calculate_val_from_key(self, key, display):
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
			self.current_img = 0
		else:
			self.current_frame += dt
			if self.current_frame >= self.animation_time:
				self.current_frame -= self.animation_time
				self.current_img = (self.current_img + 1) % len(self.imgs[self.direction])
		self.img = self.imgs[self.direction][self.current_img]

	def update(self, key, dt, display):
		dx, dy = self.calculate_val_from_key(key, display)
		self.move(dx, dy, dt)
		self.animate(dx, dy, dt)