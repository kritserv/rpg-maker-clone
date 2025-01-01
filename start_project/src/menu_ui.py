import pygame as pg
from .blit_text import blit_text

class MenuUI:
    def __init__(self, full_path):
        font_path = f"{full_path}assets/fonts/PixelatedElegance.ttf"
        self.menu_font = pg.font.Font(font_path, 9)
        self.cursor = 0

        self.DARKBLUE = pg.Color('darkblue')
        self.BLUE = pg.Color('BLUE')
        self.GREY = pg.Color('grey90')
        self.YELLOW = pg.Color('yellow')
        self.WHITE = pg.Color('white')

        self.menu = ('Inventory', 'Skills', 'Achievement', 'Save', 'Load', 'Option', 'Exit to title')
        self.menu_len = len(self.menu) - 1

        # Cooldown settings for cursor movement
        self.cursor_cooldown_time = 150  # milliseconds
        self.last_cursor_move_time = 0   # Time of last cursor movement

    def draw(self, display):
        menu_x = display.get_size()[0] - 112
        menu_y = 2
        menu_w = 110
        menu_h = display.get_size()[1] - 49
        pg.draw.rect(display, self.DARKBLUE, (menu_x, menu_y, menu_w, menu_h))
        menu_text_x = display.get_size()[0] - 100
        menu_text_y = 6
        for i, menu_text in enumerate(self.menu):
            if i == self.cursor:
                pg.draw.rect(display, self.BLUE, (menu_x, menu_text_y-3, menu_w, 12))
                blit_text(display, '>' + menu_text, self.menu_font, self.YELLOW, (menu_text_x, menu_text_y))
            else:
                blit_text(display, menu_text, self.menu_font, self.WHITE, (menu_text_x, menu_text_y))
            menu_text_y += 12
        for i in range(4):
            pg.draw.rect(display, self.GREY, (menu_x - i, menu_y - i, menu_w + 1, menu_h + 1), 1)

    def update_for_pc(self, key, dt, current_time):
        """Update menu cursor position based on key input and cooldown logic."""
        up = key[pg.K_UP]
        down = key[pg.K_DOWN]

        # Check cooldown
        if current_time - self.last_cursor_move_time > self.cursor_cooldown_time:
            if up:
                self.cursor -= 1
                if self.cursor < 0:
                    self.cursor = self.menu_len
                self.last_cursor_move_time = current_time

            elif down:
                self.cursor += 1
                if self.cursor > self.menu_len:
                    self.cursor = 0
                self.last_cursor_move_time = current_time

    def update_for_android(self, mobile_key, dt, current_time):
        up = mobile_key["K_UP"]
        down = mobile_key["K_DOWN"]

        # Check cooldown
        if current_time - self.last_cursor_move_time > self.cursor_cooldown_time:
            if up:
                self.cursor -= 1
                if self.cursor < 0:
                    self.cursor = self.menu_len
                self.last_cursor_move_time = current_time

            elif down:
                self.cursor += 1
                if self.cursor > self.menu_len:
                    self.cursor = 0
                self.last_cursor_move_time = current_time
