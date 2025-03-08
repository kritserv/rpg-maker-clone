from .base_menu import BaseMenuUI
from .text_blit import blit_text
from .image_blit import blit_img
import pygame as pg

class MenuUITitle(BaseMenuUI):
    def __init__(self, g):
        menu_items = ('New Game', 'Continue', 'Setting', 'Quit')
        super().__init__(menu_items, g)
        self.speed = 20

    def draw(self, display, dt, current_time):
        blit_img(display, self.bg, (0,0), True)
        menu_y_finish = self.game_size[1] - 77
        if self.menu_y > menu_y_finish:
            self.menu_y -= self.speed * dt
            self.speed += 800 * dt
            slide_in = True
        else:
            slide_in = False
            self.menu_y = menu_y_finish

        menu_x = 2
        menu_w = 110
        menu_h = 55
        pg.draw.rect(display, self.DARKBLUE, (menu_x, self.menu_y, menu_w, menu_h))
        menu_text_y = self.menu_y + 6
        blink_on = (current_time // self.cursor_blink_interval) % 2 == 0
        for i, menu_text in enumerate(self.menu):
            if i == self.cursor:
                pg.draw.rect(display, self.BLUE, (menu_x, menu_text_y-3, menu_w, 12))
                if blink_on:
                    blit_text(display, '→ ' + menu_text, self.menu_font, self.YELLOW, (menu_x+12, menu_text_y))
                else:
                    blit_text(display, '    ' + menu_text, self.menu_font, self.YELLOW, (menu_x+12, menu_text_y))
            else:
                blit_text(display, menu_text, self.menu_font, self.WHITE, (menu_x+12, menu_text_y))
            menu_text_y += 12
        for i in range(4):
            pg.draw.rect(display, self.GREY, (menu_x - i, self.menu_y - i, menu_w + 1, menu_h + 1), 1)

        return slide_in
