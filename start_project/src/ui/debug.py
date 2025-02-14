import pygame as pg
from ..utils import Timer
from .text_blit import blit_text
from psutil import cpu_percent, virtual_memory

class DebugUI:
    def __init__(self, g):
        self.fps_font = g['font']['font_9']
        self.fps = 0
        self.cpu = 0
        self.ram = 0
        self.fps_update_timer = Timer()
        self.fps_update_timer.start()
        self.game_size = g['game_size']

    def draw_fps(self, display, clock):
        if self.fps_update_timer.get_elapsed_time() >= 0.5:
            self.fps = "{:.2f}".format(clock.get_fps())
            self.cpu = "{:.2f}".format(cpu_percent())
            self.ram = "{:.2f}".format(virtual_memory().percent)
            self.fps_update_timer.restart()

        blit_text(display, f'ram:{self.ram}%', self.fps_font, pg.Color('black'), (5, self.game_size[1]-32))
        blit_text(display, f'cpu :{self.cpu}%', self.fps_font, pg.Color('black'), (5, self.game_size[1]-22))
        blit_text(display, f'fps :{self.fps}', self.fps_font, pg.Color('black'), (5, self.game_size[1]-12))
