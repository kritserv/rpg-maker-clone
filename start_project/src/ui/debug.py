import pygame as pg
from ..utils import Timer
from .text_blit import blit_text

class DebugUI:
    def __init__(self, g):
        self.font = g['font']['font_9']
        self.text = ""
        self.fast_text = ""
        self.update_timer = Timer()
        self.update_timer.start()
        self.game_size = g['game_size']

        self.white = g['colors']['white']
        self.bg = pg.Surface((110, 50))
        self.bg.set_alpha(200)
        self.bg.fill(g['colors']['black'])

    def draw(self, display, clock, pygame_event, player, rpgmap):
        if self.update_timer.get_elapsed_time() >= 0.5:
            self.text = 'fps: ' + "{:.2f}".format(clock.get_fps())
            self.update_timer.restart()
        self.fast_text = f"\nmap: {rpgmap.curr_map}\npos: {player.pos}\nstate: {pygame_event.game_state}"

        # if pygame_event.game_state not in (4, 5, 6):
        display.blit(self.bg, (0, 0))
        blit_text(display, self.text + self.fast_text, self.font, self.white, (5, 5))
