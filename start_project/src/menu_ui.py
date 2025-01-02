import pygame as pg
from .blit_text import blit_text

class BaseMenuUI:
    def __init__(self, full_path, menu_items):
        font_path = f"{full_path}assets/fonts/PixelatedElegance.ttf"
        self.menu_font = pg.font.Font(font_path, 9)
        self.cursor = 0

        self.DARKBLUE = pg.Color('darkblue')
        self.BLUE = pg.Color('blue')
        self.GREY = pg.Color('grey90')
        self.YELLOW = pg.Color('yellow')
        self.WHITE = pg.Color('white')

        self.menu = menu_items
        self.menu_len = len(menu_items) - 1

        self.menu_x = 0

        # Cooldown settings for cursor movement
        self.cursor_cooldown_time = 150  # milliseconds
        self.last_cursor_move_time = 0   # Time of last cursor movement

        self.speed = 900
        self.animate_in = False

    def draw(self, display, dt):
        menu_x_finish = display.get_size()[0] - 112
        if self.menu_x < menu_x_finish:
            self.menu_x += self.speed * dt
            self.speed -= 1400*dt
            self.animate_in = True
        else:
            self.animate_in = False
            self.speed = 900

        menu_y = 2
        menu_w = 110
        menu_h = display.get_size()[1] - 49
        pg.draw.rect(display, self.DARKBLUE, (self.menu_x, menu_y, menu_w, menu_h))
        menu_text_y = 6
        for i, menu_text in enumerate(self.menu):
            if i == self.cursor:
                pg.draw.rect(display, self.BLUE, (self.menu_x, menu_text_y-3, menu_w, 12))
                blit_text(display, '>' + menu_text, self.menu_font, self.YELLOW, (self.menu_x+12, menu_text_y))
            else:
                blit_text(display, menu_text, self.menu_font, self.WHITE, (self.menu_x+12, menu_text_y))
            menu_text_y += 12
        for i in range(4):
            pg.draw.rect(display, self.GREY, (self.menu_x - i, menu_y - i, menu_w + 1, menu_h + 1), 1)

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
        return False

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

class MenuUI(BaseMenuUI):
    def __init__(self, full_path):
        menu_items = ('Inventory', 'Skills', 'Achievement', 'Save', 'Load', 'Option', 'Exit to title')
        super().__init__(full_path, menu_items)

    def update_for_pc(self, key, dt, current_time):
        select_submenu = False
        if not self.animate_in:
            super().update_for_pc(key, dt, current_time)
            action = key[pg.K_RETURN]

            if action:
                self.last_action_time = current_time
                if self.cursor == 3:  # Save option selected
                    select_submenu = 'save'
                elif self.cursor == 4:  # Load option selected
                    select_submenu = 'load'

        return select_submenu

    def update_for_android(self, mobile_key, dt, current_time):
        select_submenu = False
        if not self.animate_in:
            super().update_for_android(mobile_key, dt, current_time)
            action = mobile_key["K_A"]

            if action:
                self.last_action_time = current_time
                if self.cursor == 3:  # Save option selected
                    select_submenu = 'save'
                elif self.cursor == 4:  # Load option selected
                    select_submenu = 'load'

        return select_submenu

class MenuUISave(BaseMenuUI):
    def __init__(self, full_path, player, map):
        menu_items = ('Slot 0', 'Slot 1', 'Slot 2', 'Slot 3', 'Slot 4', 'Slot 5', 'Slot 6')
        super().__init__(full_path, menu_items)
