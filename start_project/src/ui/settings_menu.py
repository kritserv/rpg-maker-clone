from .base_menu import BaseMenuUI
from ..utils import json_loader, json_saver
from .text_blit import blit_text
import pygame as pg

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
        # Get the display dimensions
        display_width = display.get_width()
        display_height = display.get_height()

        # Calculate center position
        center_x = display_width // 2
        center_y = display_height // 2

        # Update slider positions relative to center
        self.slider_left_pos = center_x - (self.size[0] // 2) - 60
        self.slider_right_pos = center_x + (self.size[0] // 2) - 60
        self.slider_top_pos = center_y - (self.size[1] // 2)

        # Update rectangles with new positions
        self.container_rect = pg.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect.x = self.slider_left_pos + self.save_value
        self.button_rect.y = self.slider_top_pos
        self.left_fill_rect = pg.Rect(self.slider_left_pos, self.slider_top_pos,
                                    self.button_rect.x - self.slider_left_pos, self.size[1])

        # Draw the components
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
    def __init__(self, settings_file_path, g):
        game_size = g['game_size']
        self.platform = g['game_mode']
        self.settings_font = g['font']['font_18']
        self.screen_center_y = game_size[1]//2-18
        self.screen_center_x = game_size[0]//2-20
        full_path = g['full_path']
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
                "Fps": 0,
                "Debug": False
            })
            settings = json_loader(self.settings_path)

        menu_items = []
        for key, items in settings.items():
            menu_items.append(key)
        if self.platform != 'pc':
            menu_items.pop(0)
        menu_items.append('Apply')

        self.sound_controller = None
        self.sound_slider = Slider((game_size[0]//2, game_size[1]//2), (110,30), settings.get('Sound', 50)/100)
        self.sound_slider.left_fill_rect_color = g['colors']['lightblue']
        self.music_slider = Slider((game_size[0]//2, game_size[1]//2), (110,30), settings.get('Music', 50)/100)
        self.music_slider.left_fill_rect_color = g['colors']['pink']

        self.cap_fps = settings.get('Fps', 0)
        self.debug = settings.get('Debug', False)

        super().__init__(menu_items, g)

    def save_settings(self, select_slot, game_input):
        settings = json_loader(self.settings_path)
        match select_slot:
            case 'Fullscreen':
                if game_input.fullscreen_toggle_timer.get_elapsed_time() >= 0.3:
                    pg.display.toggle_fullscreen()
                    game_input.fullscreen_toggle_timer.restart()
                    if settings['Fullscreen'] == True:
                        settings['Fullscreen'] = False
                    else:
                        settings['Fullscreen'] = True
            case 'Fps':
                FPS_VALUES = [0, 30, 60, 90, 120, 240, 480]
                if game_input.fps_toggle_timer.get_elapsed_time() >= 0.11:
                    game_input.fps_toggle_timer.restart()
                    current_index = FPS_VALUES.index(self.cap_fps)
                    new_index = (current_index + 1) % len(FPS_VALUES)
                    self.cap_fps = FPS_VALUES[new_index]
            case 'Debug':
                if game_input.debug_toggle_timer.get_elapsed_time() >= 0.3:
                    game_input.debug_toggle_timer.restart()
                    if self.debug == True:
                        self.debug = False
                    else:
                        self.debug = True
            case 'Apply':
                settings['Sound'] = self.sound_slider.save_value
                settings['Music'] = self.music_slider.save_value
                settings['Fps'] = self.cap_fps
                settings['Debug'] = self.debug
                json_saver(self.settings_path, settings)
                return 'Back'
            case _:
                pass
        json_saver(self.settings_path, settings)
        return ''


    def draw(self, display, dt, current_time):
        slide_in = super(MenuUISettings, self).draw(display, dt, current_time)
        match self.menu[self.cursor]:
            case 'Sound':
                self.sound_slider.draw(display)
            case 'Music':
                self.music_slider.draw(display)
            case 'Fps':
                text = f"{self.cap_fps}"
                if self.cap_fps == 0:
                    text = '8\n\n\n\n\n\n'
                    blit_text(display, text, self.settings_font, self.WHITE, (0, 0), 90, True)
                else:
                    blit_text(display, f'{text}              ', self.settings_font, self.WHITE, (0, 0), 0, True)
                if self.platform == 'web':
                    blit_text(display, '\n\n\n\n\n\n:(\n\nPlaying a game in a browser\nis limited to a maximum of 60 FPS.', self.menu_font, self.WHITE, (0, 0), 0, True)
            case 'Debug':
                text = "On"
                if self.debug == False:
                    text = 'Off'
                blit_text(display, f'{text}              ', self.settings_font, self.WHITE, (self.screen_center_x, self.screen_center_y), 0, True)

        return slide_in

    def update_for_pc(self, key, joysticks, dt, current_time, game_input):
        select_slot = super(MenuUISettings, self).update_for_pc(key, joysticks, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                select_slot = self.save_settings(select_slot, game_input)

        joystick_left, joystick_right = False, False
        for joystick in joysticks:
            if joystick.get_axis(0) < -0.6:
                joystick_left = True
            elif joystick.get_axis(0) > 0.6:
                joystick_right = True

        left, right = False, False
        if key[pg.K_LEFT] or key[pg.K_a] or joystick_left:
            left = True
        if key[pg.K_RIGHT] or key[pg.K_d] or joystick_right:
            right = True

        match self.menu[self.cursor]:
            case 'Sound':
                self.sound_slider.move_slider(left, right, dt)

            case 'Music':
                self.music_slider.move_slider(left, right, dt)

            case 'Fps':
                FPS_VALUES = [0, 30, 60, 90, 120, 240, 480]

                if game_input.fps_toggle_timer.get_elapsed_time() >= 0.11:
                    game_input.fps_toggle_timer.restart()
                    current_index = FPS_VALUES.index(self.cap_fps)
                    if left:
                        new_index = (current_index - 1) % len(FPS_VALUES)
                    elif right:
                        new_index = (current_index + 1) % len(FPS_VALUES)
                    else:
                        new_index = current_index
                    self.cap_fps = FPS_VALUES[new_index]

            case 'Debug':
                DEBUG_VALUES = [True, False]

                if game_input.fps_toggle_timer.get_elapsed_time() >= 0.11:
                    game_input.fps_toggle_timer.restart()
                    current_index = DEBUG_VALUES.index(self.debug)
                    if left:
                        new_index = (current_index - 1) % len(DEBUG_VALUES)
                    elif right:
                        new_index = (current_index + 1) % len(DEBUG_VALUES)
                    else:
                        new_index = current_index
                    self.debug = DEBUG_VALUES[new_index]

        return select_slot

    def update_for_android(self, mobile_key, joysticks, dt, current_time, game_input):
        select_slot = super(MenuUISettings, self).update_for_android(mobile_key, joysticks, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                select_slot = self.save_settings(select_slot, game_input)

        left, right = False, False
        if mobile_key["K_LEFT"]:
            left = True
        if mobile_key["K_RIGHT"]:
            right = True

        match self.menu[self.cursor]:
            case 'Sound':
                self.sound_slider.move_slider(left, right, dt)

            case 'Music':
                self.music_slider.move_slider(left, right, dt)

            case 'Fps':
                FPS_VALUES = [0, 30, 60, 90, 120, 240, 480]

                if game_input.fps_toggle_timer.get_elapsed_time() >= 0.11:
                    game_input.fps_toggle_timer.restart()
                    current_index = FPS_VALUES.index(self.cap_fps)
                    if left:
                        new_index = (current_index - 1) % len(FPS_VALUES)
                    elif right:
                        new_index = (current_index + 1) % len(FPS_VALUES)
                    else:
                        new_index = current_index
                    self.cap_fps = FPS_VALUES[new_index]

            case 'Debug':
                DEBUG_VALUES = [True, False]

                if game_input.fps_toggle_timer.get_elapsed_time() >= 0.11:
                    game_input.fps_toggle_timer.restart()
                    current_index = DEBUG_VALUES.index(self.debug)
                    if left:
                        new_index = (current_index - 1) % len(DEBUG_VALUES)
                    elif right:
                        new_index = (current_index + 1) % len(DEBUG_VALUES)
                    else:
                        new_index = current_index
                    self.debug = DEBUG_VALUES[new_index]

        return select_slot
