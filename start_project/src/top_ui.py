import pygame as pg
from .timer import Timer
from .blit_text import blit_text

class TopUI:
    def __init__(self, full_path):
        font_path = f"{full_path}assets/fonts/PixelatedElegance.ttf"
        self.fps_font = pg.font.Font(font_path, 9)
        self.fps = 0
        self.fps_update_timer = Timer()
        self.fps_update_timer.start()

        self.BLACK = pg.Color('black')

    def draw_fps(self, display, clock):
        if self.fps_update_timer.get_elapsed_time() >= 0.5:
            self.fps = round(clock.get_fps(), 2)
            self.fps_update_timer.restart()
        blit_text(display, f'Fps:{self.fps}', self.fps_font, self.BLACK, (5, 125))
