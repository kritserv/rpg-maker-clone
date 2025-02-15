import pygame as pg
from ..utils import Timer
from .text_blit import blit_text

class DebugUI:
    def __init__(self, g):
        self.fps_font = g['font']['font_9']
        self.fps = 0
        self.fps_update_timer = Timer()
        self.fps_update_timer.start()
        self.game_size = g['game_size']

    def draw_fps(self, display, clock):
        if self.fps_update_timer.get_elapsed_time() >= 0.5:
            self.fps = "{:.2f}".format(clock.get_fps())
            self.fps_update_timer.restart()

        blit_text(display, f'fps :{self.fps}', self.fps_font, pg.Color('black'), (5, self.game_size[1]-12))
