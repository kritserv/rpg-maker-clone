import pygame as pg

class Item(pg.sprite.Sprite):
	def __init__(self, name, img, description, is_key_item, is_equipable):
		pg.sprite.Sprite.__init__(self)

		self.name = name
		self.img = img
		self.description = description

		self.is_key_item = is_key_item
		self.is_equipable = is_equipable
