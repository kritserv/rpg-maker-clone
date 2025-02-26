import pygame as pg

class Skill(pg.sprite.Sprite):
	def __init__(self, name, img, description, effect):
		pg.sprite.Sprite.__init__(self)

		self.name = name
		self.img = img
		self.description = description

		self.skill_effect = effect
