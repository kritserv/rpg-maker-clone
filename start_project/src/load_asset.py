import pygame as pg
import os
from .load_json import json_loader
from csv import reader
full_path = f"{os.path.abspath('.')}/"

noimage = pg.image.fromstring(b'\x00\x00\x00\xff\xa0\xf3\xff\xa0\xf3\x00\x00\x00', (2, 2), 'RGB')
class NoSound:
    def play(self):
        pass

def load_player_sprite():
	load_spritesheet = asset_loader('sprite', 'player')
	sprite_width = 16
	sprite_height = 24
	imgs = {
		"bottom": [],
		"top": [],
		"left": [],
		"right": [],
		"running_bottom": [],
		"running_top": [],
		"running_left": [],
		"running_right": [],
		}
	directions = [
	    "bottom",
		"top",
		"left",
		"right",
		"running_bottom",
		"running_top",
		"running_left",
		"running_right"
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
			img = img.convert_alpha()
			imgs[direction].append(img)
			if frame == "left_leg_forward":
				imgs[direction].append(
					imgs[direction][0]
					)
	return imgs

class Tile(pg.sprite.Sprite):
    """Represents a single tile in the game."""
    def __init__(self, img, pos):
        super().__init__()
        self.img = img
        self.rect = self.img.get_rect(topleft=pos)

def _load_layer(csv_path, tileset, all_tile_imgs) -> list:
    """
    Load a single layer of tiles from a CSV file.
    """
    tile_size = 16
    layer_tiles = []
    with open(csv_path) as f:
        csv_reader = reader(f, delimiter=",")
        for y, row in enumerate(csv_reader):
            for x, tile_id in enumerate(row):
                if tile_id.strip():  # Ignore empty tiles
                    img_name = tileset[tile_id]
                    layer_tiles.append(Tile(all_tile_imgs[img_name], (x * tile_size, y * tile_size)))
    return layer_tiles

def load_map_data(map_json, all_tile_imgs):
    """
    Load all maps and their layers into memory from the given JSON.
    Each map will have multiple layers stored in a dictionary.
    """
    map_data = {}
    tilesets = json_loader(f"{full_path}game_data/data/maps/tilesets.json")

    for map_entry in map_json:
        map_name = map_entry["name"]
        tileset = map_entry["tileset"]

        # Prepare layers for the current map
        map_layers = {}

        for layer_index in range(1, 5):  # Adjust range as needed for more layers
            layer_name = f"layer{layer_index}"
            csv_path = f"{full_path}game_data/data/maps/{map_name}{layer_name}.csv"

            if os.path.exists(csv_path):
                map_layers[layer_name] = _load_layer(csv_path, tilesets[tileset], all_tile_imgs)

        # Store the map's layers
        map_data[map_name] = map_layers
    return map_data

def asset_loader(asset_type: str, asset: str) -> pg.mixer.Sound | NoSound | pg.Surface | pg.font.Font:
    match asset_type:
        case 'sfx':
            try:
                return pg.mixer.Sound(f"{full_path}assets/sfx/{asset}.ogg")
            except OSError as e:
                print(e)
                return NoSound()
        case 'sprite':
            try:
                return pg.image.load(f"{full_path}assets/img/sprite/{asset}.png").convert_alpha()
            except OSError as e:
                print(e)
                match asset:
                    case 'player':
                        return pg.transform.scale(noimage, (48, 192))
                    case _:
                        return pg.transform.scale(noimage, (24, 24))
        case 'tile':
            try:
                return pg.image.load(f"{full_path}assets/img/tile/{asset}.png").convert_alpha()
            except OSError as e:
                print(e)
                return pg.transform.scale(noimage, (16, 16))
        case 'img':
            try:
                return pg.image.load(f"{full_path}assets/{asset}.png").convert_alpha()
            except OSError as e:
                print(e)
                return noimage
        case 'font':
            try:
                return pg.font.Font(f"{full_path}assets/font/{asset}.ttf", 9)
            except OSError as e:
                print(e)
                return pg.font.SysFont('', size=14)
        case _:
            raise Exception(f"Unknown asset type: {asset_type}")
