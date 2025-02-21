from ..utils import json_loader, asset_loader
import pygame as pg

class RpgMap(pg.sprite.Sprite):
    """Handles loading and rendering of RPG map layers."""
    def __init__(self, start_map, g, map_data):
        super().__init__()
        self.tile_size = 16  # Standard tile size
        self.map_data = map_data   # Stores map layers for each map
        self.start_map = start_map
        self.curr_map = start_map

        self.game_size = g['game_size']
        self.view_height = self.game_size[1]//2+self.tile_size
        self.view_width = self.game_size[0]//2+self.tile_size

    def start_new_game(self):
        self.curr_map = self.start_map

    def resize_view(self, new_size):
        """
        Update View size when resize windows
        """
        if new_size != 0:
            self.game_size = new_size.get_size()
            self.view_height = self.game_size[1]//2+self.tile_size
            self.view_width = self.game_size[0]//2+self.tile_size

    def draw(self, display, camera, player_rect, layers=None, get_collision=False):
        """
        Draw specified layers of the current map onto the display.
        If no layers are specified, all layers will be drawn.
        """
        draw_count = 0
        collision_rects = []

        layers_to_draw = layers or self.map_data[self.curr_map].keys()
        bottom_edge = player_rect.y - self.view_height
        top_edge = player_rect.y + self.view_height
        left_edge = player_rect.x + self.view_width
        right_edge = player_rect.x - self.view_width
        for layer_name in layers_to_draw:
            for tile in self.map_data[self.curr_map].get(layer_name, []):
                if bottom_edge < tile.rect.y < top_edge and right_edge < tile.rect.x < left_edge:
                    if get_collision:
                        adjusted_x = tile.rect.x - camera.offset_x + display.get_size()[0] // 2
                        adjusted_y = tile.rect.y - camera.offset_y
                        # display.blit(tile.img, (adjusted_x, adjusted_y)) # show collision
                        collision_rects.append(pg.Rect(adjusted_x, adjusted_y, self.tile_size, self.tile_size))
                    else:
                        adjusted_x = tile.rect.x - camera.offset_x + display.get_size()[0] // 2
                        adjusted_y = tile.rect.y - camera.offset_y
                        display.blit(tile.img, (adjusted_x, adjusted_y))
                        draw_count += 1
        if get_collision:
            return collision_rects
        else:
            return draw_count
