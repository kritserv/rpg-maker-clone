import pygame as pg
from .blit_text import blit_text
from .load_json import json_loader, json_saver
from datetime import datetime

class BaseMenuUI:
    def __init__(self, full_path, menu_items):
        self.full_path = full_path
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

        self.speed = 450
        self.animate_in = True

    def draw(self, display, dt):
        menu_x_finish = display.get_size()[0] - 112
        if self.menu_x < menu_x_finish:
            self.menu_x += self.speed * dt
            self.animate_in = True
        else:
            self.animate_in = False

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

    def update_for_pc(self, key, dt, current_time, *args, **kwargs):
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

        select_submenu = False
        if not self.animate_in:
            action = key[pg.K_RETURN] or key[pg.K_z]
            cancel = key[pg.K_x] or key[pg.K_ESCAPE]

            if action:
                select_submenu = self.menu[self.cursor]

            elif cancel:
                select_submenu = 'Back'

        return select_submenu

    def update_for_android(self, mobile_key, dt, current_time, *args, **kwargs):
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

        select_submenu = False
        if not self.animate_in:
            action = mobile_key["K_A"]
            cancel = mobile_key["K_B"] or mobile_key["K_ESCAPE"]

            if action:
                select_submenu = self.menu[self.cursor]

            elif cancel:
                select_submenu = 'Back'

        return select_submenu

class MenuUI(BaseMenuUI):
    def __init__(self, full_path):
        menu_items = ('Inventory', 'Skills', 'Achievement', 'Save', 'Load', 'Option', 'Exit to title')
        super().__init__(full_path, menu_items)

class MenuUISave(BaseMenuUI):
    def __init__(self, full_path, save_file_path):
        self.save_path = f"{full_path}/user_data/save.json"
        if save_file_path:
            '''
            file path for android (need to save externally so it doesn't get reset when game update)
            example path: /data/user/0/org.test.myapp/files/save.json
            '''
            self.save_path = f"{save_file_path}/save.json"

        try:
            save_slots = json_loader(self.save_path)
        except FileNotFoundError:
            json_saver(self.save_path, {
              "Slot 0": {},
              "Slot 1": {},
              "Slot 2": {},
              "Slot 3": {},
              "Slot 4": {},
              "Slot 5": {},
              "Slot 6": {}
            })
            save_slots = json_loader(self.save_path)

        menu_items = []
        for key, items in save_slots.items():
            if items.get('name', False):
                menu_items.append(items.get('name'))
            else:
                menu_items.append(key)
        super().__init__(full_path, menu_items)

    def save_game(self, select_slot, player, rpgmap):
        select_slot = f"Slot {self.cursor}"
        save_slots = json_loader(self.save_path)

        select_save_slot = save_slots.get(select_slot, False) # check if empty and ask for confirm

        save_name = f"{select_slot} {datetime.now().strftime('%Y%m%d')}"
        save_slots[select_slot] = {
            'name': save_name,
            'player_levels': player.levels,
            'player_items': player.items,
            'player_pos': [player.pos[0], player.pos[1]],
            'current_map': rpgmap.curr_map,
            'time': datetime.now().strftime('%Y:%m:%d %H:%M:%S')
            }

        json_saver(self.save_path, save_slots)
        self.menu[self.cursor] = save_name

    def update_for_pc(self, key, dt, current_time, player, rpgmap):
        select_slot = super(MenuUISave, self).update_for_pc(key, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                self.save_game(select_slot, player, rpgmap)

        return select_slot

    def update_for_android(self, mobile_key, dt, current_time, player, rpgmap):
        select_slot = super(MenuUISave, self).update_for_android(mobile_key, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                self.save_game(select_slot, player, rpgmap)

        return select_slot

class MenuUILoad(BaseMenuUI):
    def __init__(self, full_path, save_file_path):
        self.save_path = f"{full_path}/user_data/save.json"
        if save_file_path:
            '''
            file path for android (need to save externally so it doesn't get reset when game update)
            example path: /data/user/0/org.test.myapp/files/save.json
            '''

            self.save_path = f"{save_file_path}/save.json"

        try:
            save_slots = json_loader(self.save_path)
        except FileNotFoundError:
            json_saver(self.save_path, {
              "Slot 0": {},
              "Slot 1": {},
              "Slot 2": {},
              "Slot 3": {},
              "Slot 4": {},
              "Slot 5": {},
              "Slot 6": {}
            })
            save_slots = json_loader(self.save_path)

        menu_items = []
        for key, items in save_slots.items():
            if items.get('name', False):
                menu_items.append(items.get('name'))
            else:
                menu_items.append(key)
        super().__init__(full_path, menu_items)

    def load_game(self, select_slot, player, rpgmap):
        select_slot = f"Slot {self.cursor}"
        save_slots = json_loader(self.save_path)

        select_save_slot = save_slots.get(select_slot, False) # check if empty and ask for confirm

        if select_save_slot:
            player.pos = select_save_slot.get('player_pos')
            player.levels = select_save_slot.get('player_levels')
            player.items = select_save_slot.get('player_items')
            rpgmap.curr_map = select_save_slot.get('current_map')

    def update_for_pc(self, key, dt, current_time, player, rpgmap):
        select_slot = super(MenuUILoad, self).update_for_pc(key, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                self.load_game(select_slot, player, rpgmap)

        return select_slot

    def update_for_android(self, mobile_key, dt, current_time, player, rpgmap):
        select_slot = super(MenuUILoad, self).update_for_android(mobile_key, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                self.load_game(select_slot, player, rpgmap)

        return select_slot
        super().__init__(full_path, menu_items)
