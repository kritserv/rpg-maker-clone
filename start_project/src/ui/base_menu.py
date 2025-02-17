import pygame as pg
from .text_blit import blit_text

class BaseMenuUI:
    def __init__(self, menu_items, g):
        self.menu_font = g['font']['font_9']
        self.cursor = 0
        self.cursor_blink_interval = 200

        self.play_sound = False

        self.DARKBLUE = g['colors']['darkblue']
        self.BLUE = g['colors']['blue']
        self.GREY = g['colors']['lightgrey']
        self.YELLOW = g['colors']['yellow']
        self.WHITE = g['colors']['white']

        self.menu = menu_items
        self.menu_len = len(menu_items) - 1
        self.game_size = g['game_size']

        self.menu_x = 0
        self.menu_y = self.game_size[1]

        # Cooldown settings for cursor movement
        self.cursor_cooldown_time = 150  # milliseconds
        self.last_cursor_move_time = 0   # Time of last cursor movement

        self.speed = 450

    def draw(self, display, dt, current_time):
        menu_x_finish = display.get_size()[0] - 112
        if self.menu_x > menu_x_finish:
            self.menu_x -= self.speed * dt
            slide_in = True
        else:
            slide_in = False
            self.menu_x = menu_x_finish

        menu_y = 2
        menu_w = 110
        menu_h = 90
        pg.draw.rect(display, self.DARKBLUE, (self.menu_x, menu_y, menu_w, menu_h))
        menu_text_y = 6
        blink_on = (current_time // self.cursor_blink_interval) % 2 == 0
        for i, menu_text in enumerate(self.menu):
            if i == self.cursor:
                pg.draw.rect(display, self.BLUE, (self.menu_x, menu_text_y-3, menu_w, 12))
                if blink_on:
                    blit_text(display, '> ' + menu_text, self.menu_font, self.YELLOW, (self.menu_x+12, menu_text_y))
                else:
                    blit_text(display, '  ' + menu_text, self.menu_font, self.YELLOW, (self.menu_x+12, menu_text_y))
            else:
                blit_text(display, menu_text, self.menu_font, self.WHITE, (self.menu_x+12, menu_text_y))
            menu_text_y += 12
        for i in range(4):
            pg.draw.rect(display, self.GREY, (self.menu_x - i, menu_y - i, menu_w + 1, menu_h + 1), 1)

        return slide_in

    def update_for_pc(self, key, joysticks, dt, current_time, *args, **kwargs):
        """Update menu cursor position based on key game_input and cooldown logic."""

        up, left, right, down, cancel, action = False, False, False, False, False, False

        for joystick in joysticks:
            if joystick.get_axis(1) < -0.6:
                up = True
            elif joystick.get_axis(1) > 0.6:
                down = True
            if joystick.get_button(0):
                action = True
            if joystick.get_button(1):
                action = True
            if joystick.get_button(10):
                cancel = True

        if not up:
            up = key[pg.K_UP] or key[pg.K_w]
        if not down:
            down = key[pg.K_DOWN] or key[pg.K_s]

        # Check cooldown
        if current_time - self.last_cursor_move_time > self.cursor_cooldown_time:
            if up:
                self.cursor -= 1
                if self.cursor < 0:
                    self.cursor = self.menu_len
                self.last_cursor_move_time = current_time
                if self.play_sound:
                    self.select_sfx.play()

            elif down:
                self.cursor += 1
                if self.cursor > self.menu_len:
                    self.cursor = 0
                self.last_cursor_move_time = current_time
                if self.play_sound:
                    self.select_sfx.play()

        select_submenu = False
        if not action:
            action = key[pg.K_RETURN] or key[pg.K_KP_ENTER] or key[pg.K_z] or key[pg.K_SPACE]
        if not cancel:
            cancel = key[pg.K_x] or key[pg.K_ESCAPE] or key[pg.K_KP_0]

        if action:
            select_submenu = self.menu[self.cursor]

        elif cancel:
            select_submenu = 'Back'
            if self.play_sound:
                self.select_sfx.play()

        return select_submenu

    def update_for_android(self, mobile_key, joysticks, dt, current_time, *args, **kwargs):

        up, left, right, down, cancel, action = False, False, False, False, False, False

        if not up:
            up = mobile_key["K_UP"]
        if not down:
            down = mobile_key["K_DOWN"]

        # Check cooldown
        if current_time - self.last_cursor_move_time > self.cursor_cooldown_time:
            if up:
                self.cursor -= 1
                if self.cursor < 0:
                    self.cursor = self.menu_len
                self.last_cursor_move_time = current_time
                if self.play_sound:
                    self.select_sfx.play()

            elif down:
                self.cursor += 1
                if self.cursor > self.menu_len:
                    self.cursor = 0
                self.last_cursor_move_time = current_time
                if self.play_sound:
                    self.select_sfx.play()

        select_submenu = False
        if not action:
            action = mobile_key["K_A"]
        if not cancel:
            cancel = mobile_key["K_B"] or mobile_key["K_ESCAPE"]

        if action:
            select_submenu = self.menu[self.cursor]

        elif cancel:
            select_submenu = 'Back'
            if self.play_sound:
                self.select_sfx.play()

        return select_submenu
