import pygame as pg

class Item(pg.sprite.Sprite):
	def __init__(self, name, img, defense, attack, critical, speed, is_key_item):
		pg.sprite.Sprite.__init__(self)

		self.name = name
		self.img = img

		self.attrs = {
    		'defense': defense,
    		'attack': attack,
    		'critical': critical,
    		'speed': speed
		}

		self.is_key_item = is_key_item
