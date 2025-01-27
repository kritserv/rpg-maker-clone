import pygame as pg
from math import floor

class Camera:
	def __init__(self, display_width, display_height, game_size_width, game_size_height):
		self.display_width = display_width
		self.display_height = display_height
		self.offset_x = 0
		self.offset_y = 0

		self.extra_offset_x = -(display_width/2-8)

		multiply = display_height/game_size_height
		if multiply % 2 == 0:
			self.extra_offset_y = -floor(game_size_height+5+game_size_height/2*(multiply-1))-1
		else:
			self.extra_offset_y = -floor(game_size_height+5+game_size_height/2*(multiply-1))

	def update(self, player):
		self.offset_x = self.extra_offset_x + player.rect.centerx + self.display_width // 2
		self.offset_y = self.extra_offset_y + player.rect.centery + self.display_height // 2
