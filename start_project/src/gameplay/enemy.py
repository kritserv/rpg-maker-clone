import pygame as pg
from math import floor, ceil
from ..utils import asset_loader

class Enemy(pg.sprite.Sprite):
	def __init__(self, name, hp, enemy_img, moves, defeat_reward):
		pg.sprite.Sprite.__init__(self)

		self.name = name
		self.start_hp = hp
		self.max_hp = self.start_hp
		self.hp = self.start_hp

		self.img = asset_loader('sprite', enemy_img)

		self.image = pg.Surface((16, 16))
		self.image.fill((255, 0, 0))
		self.rect = self.image.get_rect()

		self.moves = moves
		self.defeat_reward = defeat_reward
		self.battle_info = []

	def start_new_game(self):
		self.max_hp = self.start_hp
		self.hp = self.start_hp
