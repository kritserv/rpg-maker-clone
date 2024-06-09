from .load_json import json_loader
from csv import reader
import pygame as pg

class Tile(pg.sprite.Sprite):
	def __init__(self, img_path, pos, zoom):
		pg.sprite.Sprite.__init__(self)
		self.img = pg.image.load(img_path)
		self.img = pg.transform.scale(
			self.img, 
			(self.img.get_width() * zoom, 
				self.img.get_height() * zoom
				)
			)
		self.rect = self.img.get_rect(topleft=pos)
		menu_offset = (280, 64)
		self.rect.x += menu_offset[0]
		self.rect.y += menu_offset[1]

class RpgMap(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.zoom = 2.25
		self.tile_size = 16 * self.zoom
		self.map_data = {}
		self.curr_map = "map001"

	def load_map_data(self, map_json, project_name) -> None:

		tilesets = json_loader(f"projects/{project_name}/game_data/data/maps/tilesets.json")

		for elem in map_json:
			name = elem["name"]
			path = f"projects/{project_name}/game_data/data/maps/"+elem["path"]
			tileset = elem["tileset"]

			current_tiles = []

			with open(path) as f:
				csv_load = reader(f, delimiter=",")

				for y, row in enumerate(csv_load):
					for x, tile_id in enumerate(row):
						img_path = f"projects/{project_name}/assets/img/tile/" + tilesets[tileset][tile_id]
						current_tiles.append(Tile(img_path, (x*self.tile_size, y*self.tile_size), self.zoom))

			self.map_data[name] = current_tiles

	def draw(self, display) -> None:
		for tile in self.map_data[self.curr_map]:
			display.blit(tile.img, tile.rect)