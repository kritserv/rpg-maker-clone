import pygame as pg
from pygame.key import ScancodeWrapper
from .timer import Timer
from .load_asset import asset_loader

class GameInput:
    def __init__(self, platform, game_size = [], full_path=''):
        self.fps_toggle_timer = Timer()
        self.fps_toggle_timer.start()
        self.debug_toggle_timer = Timer()
        self.debug_toggle_timer.start()
        try:
            self.joysticks = [pg.joystick.Joystick(0)]
        except pg.error:
            self.joysticks = []
        if platform == 'pc':
            self.fullscreen_toggle_timer = Timer()
            self.fullscreen_toggle_timer.start()
        elif platform == 'android':
            self.game_size = game_size
            self.dpad_up = asset_loader('sprite','dpad')
            self.dpad_up.set_alpha(155)
            self.dpad_left = pg.transform.rotate(self.dpad_up, 90)
            self.dpad_down = pg.transform.rotate(self.dpad_up, 180)
            self.dpad_right = pg.transform.rotate(self.dpad_up, 270)
            self.a = asset_loader('sprite','a')
            self.b = asset_loader('sprite','b')
            self.select = asset_loader('sprite','select')
            self.a.set_alpha(155)
            self.b.set_alpha(155)
            self.select.set_alpha(155)

            self.image_controls = {
                "UP": (self.dpad_up, (40, 38)),
                "LEFT": (self.dpad_left, (10, 66)),
                "RIGHT": (self.dpad_right, (70, 66)),
                "DOWN": (self.dpad_down, (40, 94)),
                "A": (self.a, (game_size[0] - 50, 100)),
                "B": (self.b, (game_size[0] - 85, 100)),
                "SELECT": (self.select, (game_size[0]//2-16, 100)),
            }
            self.active_touches = {}


    def update_for_pc(self, pygame_event, display):
        new_size, joystick = pygame_event.check_pc(self.joysticks)
        if new_size:
            display = new_size
        if joystick:
            self.joysticks.append(joystick)
        key = pg.key.get_pressed()
        if key[pg.K_F11]:
            if self.fullscreen_toggle_timer.get_elapsed_time() >= 0.3:
                pg.display.toggle_fullscreen()
                self.fullscreen_toggle_timer.restart()
        if self.fullscreen_toggle_timer.get_elapsed_time() >= 0.5:
            self.fullscreen_toggle_timer.pause()

        return new_size, key, display

    def update_for_android(self, pygame_event):
        mobile_key, _ = pygame_event.check_android(self.active_touches, self.image_controls)
        return mobile_key

    def draw_for_android(self, display):
        for direction, (image, pos) in self.image_controls.items():
            display.blit(image, pos)

    def update_for_web(self, pygame_event):
        _, joystick = pygame_event.check_pc(self.joysticks)
        if joystick:
            self.joysticks.append(joystick)
        return pg.key.get_pressed()
