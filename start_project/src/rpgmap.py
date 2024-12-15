from .load_json import json_loader
from csv import reader
import pygame as pg
import os

class Tile(pg.sprite.Sprite):
    """Represents a single tile in the game."""
    def __init__(self, img_path, pos):
        super().__init__()
        self.img = pg.image.load(img_path).convert_alpha()
        self.rect = self.img.get_rect(topleft=pos)


class RpgMap(pg.sprite.Sprite):
    """Handles loading and rendering of RPG map layers."""
    def __init__(self, full_path, start_map, game_size):
        super().__init__()
        self.tile_size = 16  # Standard tile size
        self.map_data = {}   # Stores map layers for each map
        self.curr_map = start_map
        self.full_path = full_path

        self.game_size = game_size
        self.view_height = game_size[1]//2+self.tile_size
        self.view_width = game_size[0]//2+self.tile_size

    def load_map_data(self, map_json) -> None:
        """
        Load all maps and their layers into memory from the given JSON.
        Each map will have multiple layers stored in a dictionary.
        """
        tilesets = json_loader(f"{self.full_path}game_data/data/maps/tilesets.json")

        for map_entry in map_json:
            map_name = map_entry["name"]
            tileset = map_entry["tileset"]

            # Prepare layers for the current map
            map_layers = {}

            for layer_index in range(1, 3):  # Adjust range as needed for more layers
                layer_name = f"layer{layer_index}"
                csv_path = f"{self.full_path}game_data/data/maps/{map_name}{layer_name}.csv"

                if os.path.exists(csv_path):
                    map_layers[layer_name] = self._load_layer(csv_path, tilesets[tileset])

            # Store the map's layers
            self.map_data[map_name] = map_layers

    def _load_layer(self, csv_path, tileset) -> list:
        """
        Load a single layer of tiles from a CSV file.
        """
        layer_tiles = []
        with open(csv_path) as f:
            csv_reader = reader(f, delimiter=",")
            for y, row in enumerate(csv_reader):
                for x, tile_id in enumerate(row):
                    if tile_id.strip():  # Ignore empty tiles
                        img_path = f"{self.full_path}assets/img/tile/{tileset[tile_id]}"
                        layer_tiles.append(Tile(img_path, (x * self.tile_size, y * self.tile_size)))
        return layer_tiles

    def draw(self, display, camera, player_rect, layers=None):
        """
        Draw specified layers of the current map onto the display.
        If no layers are specified, all layers will be drawn.
        """
        layers_to_draw = layers or self.map_data[self.curr_map].keys()
        bottom_edge = player_rect.y - self.view_height
        top_edge = player_rect.y + self.view_height
        left_edge = player_rect.x + self.view_width
        right_edge = player_rect.x - self.view_width
        for layer_name in layers_to_draw:
            for tile in self.map_data[self.curr_map].get(layer_name, []):
                if bottom_edge < tile.rect.y < top_edge and right_edge < tile.rect.x < left_edge:
                    adjusted_x = tile.rect.x - camera.offset_x + display.get_size()[0] // 2
                    adjusted_y = tile.rect.y - camera.offset_y
                    display.blit(tile.img, (adjusted_x, adjusted_y))

    def draw_scaled_screen(self, display, camera, player_rect, layers=None):
        """
        Draw specified layers of the current map onto a scaled display.
        If no layers are specified, all layers will be drawn.
        """
        layers_to_draw = layers or self.map_data[self.curr_map].keys()
        bottom_edge = player_rect.y - self.view_height
        top_edge = player_rect.y + self.view_height
        left_edge = player_rect.x + self.view_width
        right_edge = player_rect.x - self.view_width

        for layer_name in layers_to_draw:
            for tile in self.map_data[self.curr_map].get(layer_name, []):
                if bottom_edge < tile.rect.y < top_edge and right_edge < tile.rect.x < left_edge:
                    adjusted_x = tile.rect.x - camera.offset_x + display.get_size()[0] // 2 - self.game_size[0]
                    adjusted_y = tile.rect.y - camera.offset_y - self.game_size[1]
                    display.blit(tile.img, (adjusted_x, adjusted_y))
