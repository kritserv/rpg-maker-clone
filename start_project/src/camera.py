import pygame as pg

class Camera:
	def __init__(self, display_width, display_height, game_size_width):
		self.display_width = display_width
		self.display_height = display_height
		self.offset_x = 0
		self.offset_y = 0
		self.extra_offset = -(game_size_width+game_size_width/2)+8

	def update(self, player):
		self.offset_x = self.extra_offset + player.rect.centerx + self.display_width // 2
		self.offset_y = -279 + player.rect.centery + self.display_height // 2
