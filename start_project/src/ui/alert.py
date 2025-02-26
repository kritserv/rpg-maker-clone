from .base_menu import BaseMenuUI
from .text_blit import blit_text
from .image_blit import blit_img
from ..utils import Timer
import pygame as pg

class Alert(BaseMenuUI):
    def __init__(self, g):
        menu_items = [' ']
        super().__init__(menu_items, g)
        self.menu = ''
        self.speed = 20
        self.menu_y = -100
        self.timer = Timer()
        self.timer.start()

    def draw(self, display, dt, current_time):
        slide_in = False
        if self.menu and self.timer.is_paused:
            self.timer.restart()

        if self.menu and 2 >= self.timer.get_elapsed_time() >= 0.1:
            menu_y_finish = 0
            if self.menu_y < menu_y_finish:
                self.menu_y += self.speed * dt
                self.speed += 800 * dt
                slide_in = True
            else:
                slide_in = False
                self.menu_y = menu_y_finish

            menu_x = display.get_size()[0] - 132
            menu_w = 130
            menu_h = 40
            pg.draw.rect(display, self.DARKBLUE, (menu_x, self.menu_y, menu_w, menu_h))
            blit_text(display, self.menu, self.menu_font, self.WHITE, (menu_x+4, self.menu_y + 6))
            for i in range(4):
                pg.draw.rect(display, self.GREY, (menu_x - i, self.menu_y - i, menu_w + 1, menu_h + 1), 1)

        if self.timer.get_elapsed_time() > 2:
            self.menu = ''
            self.speed = 20
            self.menu_y = -100
            self.timer.pause()

        return slide_in
