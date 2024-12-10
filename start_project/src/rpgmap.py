from .load_json import json_loader
from csv import reader
import pygame as pg
import os

class Tile(pg.sprite.Sprite):
	def __init__(self, img_path, pos):
		pg.sprite.Sprite.__init__(self)
		self.img = pg.image.load(img_path)
		self.rect = self.img.get_rect(topleft=pos)

class RpgMap(pg.sprite.Sprite):
	def __init__(self, full_path, start_map):
		pg.sprite.Sprite.__init__(self)
		self.tile_size = 16
		self.map_data = {}
		self.curr_map = start_map
		self.full_path = full_path

	def load_map_data(self, map_json) -> None:

		tilesets = json_loader(f"{self.full_path}game_data/data/maps/tilesets.json")

		for elem in map_json:
			name = elem["name"]
			path = f"{self.full_path}game_data/data/maps/{elem['path']}"
			tileset = elem["tileset"]

			current_tiles = []

			with open(path) as f:
				csv_load = reader(f, delimiter=",")

				for y, row in enumerate(csv_load):
					for x, tile_id in enumerate(row):
						img_path = f"{self.full_path}assets/img/tile/{tilesets[tileset][tile_id]}"
						current_tiles.append(Tile(img_path, (x*self.tile_size, y*self.tile_size)))

			self.map_data[name] = current_tiles

	def draw(self, display, camera):
		for tile in self.map_data[self.curr_map]:
			# Calculate adjusted positions
			adjusted_x = tile.rect.x - camera.offset_x + display.get_size()[0]//2
			adjusted_y = tile.rect.y - camera.offset_y
			# Draw the tile at the adjusted position
			display.blit(tile.img, (adjusted_x, adjusted_y))

	def draw_scaled_screen(self, display, camera, game_size):
		for tile in self.map_data[self.curr_map]:
			# Calculate adjusted positions
			adjusted_x = tile.rect.x - camera.offset_x + display.get_size()[0]//2 - game_size[0]
			adjusted_y = tile.rect.y - camera.offset_y - game_size[1]
			# Draw the tile at the adjusted position
			display.blit(tile.img, (adjusted_x, adjusted_y))
