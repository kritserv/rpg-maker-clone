import pygame as pg

class Skill(pg.sprite.Sprite):
	def __init__(self, name, img, description, attrs):
		pg.sprite.Sprite.__init__(self)

		self.name = name
		self.img = img
		self.description = description

		self.attrs = attrs
