import pygame as pg
from .blit_text import blit_text
from .load_json import json_loader, json_saver
from .load_asset import asset_loader
from datetime import datetime

class BaseMenuUI:
    def __init__(self, full_path, menu_items, game_size):
        self.full_path = full_path
        self.menu_font = asset_loader('font', 'PixelatedElegance')
        self.cursor = 0
        self.cursor_blink_interval = 200

        self.play_sound = False

        self.DARKBLUE = pg.Color('darkblue')
        self.BLUE = pg.Color('blue')
        self.GREY = pg.Color('grey90')
        self.YELLOW = pg.Color('yellow')
        self.WHITE = pg.Color('white')

        self.menu = menu_items
        self.menu_len = len(menu_items) - 1
        self.game_size = game_size

        self.menu_x = 0
        self.menu_y = game_size[1]

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
        """Update menu cursor position based on key input and cooldown logic."""

        up, left, right, down, cancel, action = False, False, False, False, False, False

        for joystick in joysticks:
            if joystick.get_axis(1) < -0.6:
                up = True
            elif joystick.get_axis(1) > 0.6:
                down = True
            if joystick.get_button(0):
                action = True
            if joystick.get_button(1):
                cancel = True
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
            if select_submenu and self.play_sound:
                if select_submenu not in ('Inventory', 'Skills', 'Achievement', 'Setting', 'Slot 0', 'Slot 1', 'Slot 2', 'Slot 3', 'Slot 4', 'Slot 5', 'Slot 6'):
                    self.select_sfx.play()

        elif cancel:
            select_submenu = 'Back'
            if self.play_sound:
                self.select_sfx.play()

        return select_submenu

    def update_for_android(self, mobile_key, joysticks, dt, current_time, *args, **kwargs):

        up, left, right, down, cancel, action = False, False, False, False, False, False

        for joystick in joysticks:
            if joystick.get_axis(1) < -0.6:
                up = True
            elif joystick.get_axis(1) > 0.6:
                down = True
            if joystick.get_button(0):
                action = True
            if joystick.get_button(1):
                cancel = True
            if joystick.get_button(10):
                cancel = True

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
            if select_submenu and self.play_sound:
                if select_submenu not in ('Inventory', 'Skills', 'Achievement', 'Setting', 'Slot 0', 'Slot 1', 'Slot 2', 'Slot 3', 'Slot 4', 'Slot 5', 'Slot 6'):
                    self.select_sfx.play()

        elif cancel:
            select_submenu = 'Back'
            if self.play_sound:
                self.select_sfx.play()

        return select_submenu

class MenuUI(BaseMenuUI):
    def __init__(self, full_path, game_size):
        menu_items = ('Inventory', 'Skills', 'Achievement', 'Save', 'Load', 'Setting', 'Exit to title')
        super().__init__(full_path, menu_items, game_size)
        self.open_menu_sfx = asset_loader('sfx', 'open_menu')
        self.select_sfx = asset_loader('sfx', 'select')

        self.is_open = False
        self.play_sound = True

class MenuUITitle(BaseMenuUI):
    def __init__(self, full_path, game_size):
        menu_items = ('New Game', 'Continue', 'Setting', 'Quit')
        super().__init__(full_path, menu_items, game_size)
        self.speed = 20

    def draw(self, display, dt, current_time):
        menu_y_finish = self.game_size[1] - 77
        if self.menu_y > menu_y_finish:
            self.menu_y -= self.speed * dt
            self.speed += 800 * dt
            slide_in = True
        else:
            slide_in = False

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
                    blit_text(display, '> ' + menu_text, self.menu_font, self.YELLOW, (menu_x+12, menu_text_y))
                else:
                    blit_text(display, '  ' + menu_text, self.menu_font, self.YELLOW, (menu_x+12, menu_text_y))
            else:
                blit_text(display, menu_text, self.menu_font, self.WHITE, (menu_x+12, menu_text_y))
            menu_text_y += 12
        for i in range(4):
            pg.draw.rect(display, self.GREY, (menu_x - i, self.menu_y - i, menu_w + 1, menu_h + 1), 1)

        return slide_in

class MenuUISave(BaseMenuUI):
    def __init__(self, full_path, save_file_path, game_size):
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
        super().__init__(full_path, menu_items, game_size)
        self.select_sfx = asset_loader('sfx', 'select')
        self.play_sound = True

    def save_game(self, select_slot, player, rpgmap):
        select_slot = f"Slot {self.cursor}"
        save_slots = json_loader(self.save_path)

        select_save_slot = save_slots.get(select_slot, False) # check if empty and ask for confirm

        save_name = f"{select_slot} {datetime.now().strftime('%Y%m%d')}"
        save_slots[select_slot] = {
            'name': save_name,
            'player_levels': player.levels,
            'player_items': player.items,
            'player_pos': [player.last_pos.x, player.last_pos.y],
            'player_direction': player.direction,
            'current_map': rpgmap.curr_map,
            'time': datetime.now().strftime('%Y:%m:%d %H:%M:%S')
            }

        json_saver(self.save_path, save_slots)
        self.menu[self.cursor] = save_name

    def update_for_pc(self, key, joysticks, dt, current_time, player, rpgmap):
        select_slot = super(MenuUISave, self).update_for_pc(key, joysticks, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                self.save_game(select_slot, player, rpgmap)

        return select_slot

    def update_for_android(self, mobile_key, joysticks, dt, current_time, player, rpgmap):
        select_slot = super(MenuUISave, self).update_for_android(mobile_key, joysticks, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                self.save_game(select_slot, player, rpgmap)

        return select_slot

class MenuUILoad(BaseMenuUI):
    def __init__(self, full_path, save_file_path, game_size):
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
        super().__init__(full_path, menu_items, game_size)
        self.select_sfx = asset_loader('sfx', 'select')
        self.play_sound = True

    def load_game(self, select_slot, player, rpgmap):
        select_slot = f"Slot {self.cursor}"
        save_slots = json_loader(self.save_path)

        select_save_slot = save_slots.get(select_slot, False) # check if empty and ask for confirm

        if select_save_slot:
            player.pos = pg.math.Vector2(select_save_slot.get('player_pos'))
            player.last_pos = pg.math.Vector2(select_save_slot.get('player_pos'))
            player.next_pos = pg.math.Vector2(select_save_slot.get('player_pos'))
            player.direction = select_save_slot.get('player_direction')
            player.levels = select_save_slot.get('player_levels')
            player.items = select_save_slot.get('player_items')
            rpgmap.curr_map = select_save_slot.get('current_map')
            return True
        return False

    def update_for_pc(self, key, joysticks, dt, current_time, player, rpgmap):
        select_slot = super(MenuUILoad, self).update_for_pc(key, joysticks, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                load_success = self.load_game(select_slot, player, rpgmap)
                if load_success:
                    return select_slot
                else:
                    select_slot = False

        return select_slot

    def update_for_android(self, mobile_key, joysticks, dt, current_time, player, rpgmap):
        select_slot = super(MenuUILoad, self).update_for_android(mobile_key, joysticks, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                load_success = self.load_game(select_slot, player, rpgmap)
                if load_success:
                    return select_slot
                else:
                    select_slot = False

        return select_slot
        super().__init__(full_path, menu_items)

# Sliders tutorial from coding with sphere https://github.com/m1chaelwilliams/Pygame-Tutorials
class Slider(pg.sprite.Sprite):
    def __init__(self, pos, size, initial_val) -> None:
        pg.sprite.Sprite.__init__(self)
        self.pos = pos
        self.size = size

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val

        self.container_rect = pg.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.container_color = pg.Color("black")
        self.button_rect = pg.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])
        self.button_rect_color = pg.Color("white")
        self.left_fill_rect = pg.Rect(self.slider_left_pos, self.slider_top_pos, self.button_rect.x - self.slider_left_pos, self.size[1])
        self.left_fill_rect_color = pg.Color("skyblue")

        self.save_value = self.button_rect.x - self.slider_left_pos

    def draw(self, display):
        pg.draw.rect(display, self.container_color, self.container_rect)
        pg.draw.rect(display, self.left_fill_rect_color, self.left_fill_rect)
        pg.draw.rect(display, self.button_rect_color, self.button_rect)

    def move_slider(self, left, right, dt):
        if left:
            new_x = self.button_rect.x - 200 * dt
            if new_x < self.slider_left_pos:
                new_x = self.slider_left_pos
            self.button_rect.x = new_x

        elif right:
            new_x = self.button_rect.x + 200 * dt
            if new_x > self.slider_right_pos - self.button_rect.width:
                new_x = self.slider_right_pos - self.button_rect.width
            self.button_rect.x = new_x

        x = self.button_rect.x - self.slider_left_pos
        self.save_value = x
        self.left_fill_rect.width = x

class MenuUISettings(BaseMenuUI):
    def __init__(self, full_path, settings_file_path, game_size, platform):
        self.settings_path = f"{full_path}/user_data/settings.json"
        if settings_file_path:
            self.settings_path = f"{settings_file_path}/settings.json"

        try:
            settings = json_loader(self.settings_path)
        except FileNotFoundError:
            json_saver(self.settings_path, {
                "Fullscreen": False,
                "Sound": 50,
                "Music": 50,
            })
            settings = json_loader(self.settings_path)

        menu_items = []
        for key, items in settings.items():
            menu_items.append(key)
        if platform != 'pc':
            menu_items.pop(0)
        menu_items.append('Apply')

        self.sound_slider = Slider((game_size[0]//2, game_size[1]//2), (110,30), settings['Sound']/100)
        self.sound_slider.left_fill_rect_color = pg.Color("skyblue")
        self.music_slider = Slider((game_size[0]//2, game_size[1]//2), (110,30), settings['Music']/100)
        self.music_slider.left_fill_rect_color = pg.Color("hotpink")

        super().__init__(full_path, menu_items, game_size)

    def save_settings(self, select_slot, input):
        settings = json_loader(self.settings_path)
        match select_slot:
            case 'Fullscreen':
                if input.fullscreen_toggle_timer.get_elapsed_time() >= 0.3:
                    pg.display.toggle_fullscreen()
                    input.fullscreen_toggle_timer.restart()
                    if settings['Fullscreen'] == True:
                        settings['Fullscreen'] = False
                    else:
                        settings['Fullscreen'] = True
            case 'Apply':
                settings['Sound'] = self.sound_slider.save_value
                settings['Music'] = self.music_slider.save_value
                json_saver(self.settings_path, settings)
                return 'Back'
            case _:
                pass
        json_saver(self.settings_path, settings)
        return ''


    def draw(self, display, dt, current_time):
        slide_in = super(MenuUISettings, self).draw(display, dt, current_time)
        if self.menu[self.cursor] == 'Sound':
            self.sound_slider.draw(display)
        if self.menu[self.cursor] == 'Music':
            self.music_slider.draw(display)

        return slide_in

    def update_for_pc(self, key, joysticks, dt, current_time, input):
        select_slot = super(MenuUISettings, self).update_for_pc(key, joysticks, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                select_slot = self.save_settings(select_slot, input)

        if self.menu[self.cursor] == 'Sound':
            self.sound_slider.move_slider(key[pg.K_LEFT] or key[pg.K_a], key[pg.K_RIGHT] or key[pg.K_d], dt)

        elif self.menu[self.cursor] == 'Music':
            self.music_slider.move_slider(key[pg.K_LEFT] or key[pg.K_a], key[pg.K_RIGHT] or key[pg.K_d], dt)

        return select_slot

    def update_for_android(self, mobile_key, joysticks, dt, current_time, input):
        select_slot = super(MenuUISettings, self).update_for_android(mobile_key, joysticks, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                select_slot = self.save_settings(select_slot, input)

        if self.menu[self.cursor] == 'Sound':
            self.sound_slider.move_slider(mobile_key["K_LEFT"], mobile_key["K_RIGHT"], dt)

        elif self.menu[self.cursor] == 'Music':
            self.music_slider.move_slider(mobile_key["K_LEFT"], mobile_key["K_RIGHT"], dt)

        return select_slot
