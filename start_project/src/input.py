import pygame as pg
from .timer import Timer

class Input:
    def __init__(self, platform, game_size = [], full_path='') -> None:
        if platform == 'pc':
            self.fullscreen_toggle_timer = Timer()
            self.fullscreen_toggle_timer.start()
        elif platform == 'android':
                self.game_size = game_size
                sprite_path = f"{full_path}assets/img/sprite/"
                self.dpad_up = pg.image.load(
                    f"{sprite_path}dpad.png"
                    ).convert_alpha()
                self.dpad_up.set_alpha(155)
                self.dpad_left = pg.transform.rotate(self.dpad_up, 90)
                self.dpad_down = pg.transform.rotate(self.dpad_up, 180)
                self.dpad_right = pg.transform.rotate(self.dpad_up, 270)
                self.a = pg.image.load(
                    f"{sprite_path}a.png"
                    ).convert_alpha()
                self.b = pg.image.load(
                    f"{sprite_path}b.png"
                    ).convert_alpha()
                self.a.set_alpha(155)
                self.b.set_alpha(155)

                self.image_controls = {
                    "UP": (self.dpad_up, (40, 38)),
                    "LEFT": (self.dpad_left, (10, 66)),
                    "RIGHT": (self.dpad_right, (70, 66)),
                    "DOWN": (self.dpad_down, (40, 94)),
                    "A": (self.a, (game_size[0] - 85, 77)),
                    "B": (self.b, (game_size[0] - 50, 77)),
                }
                self.active_touches = {}


    def update_for_pc(self, pygame_event, display):
        new_size = pygame_event.check()
        if new_size:
            display = new_size
        key = pg.key.get_pressed()
        if key[pg.K_F11]:
            if self.fullscreen_toggle_timer.get_elapsed_time() >= 0.3:
                pg.display.toggle_fullscreen()
                self.fullscreen_toggle_timer.restart()
        if self.fullscreen_toggle_timer.get_elapsed_time() >= 0.5:
            self.fullscreen_toggle_timer.pause()

        return new_size, key, display

    def update_for_android(self, pygame_event):
        for event in pg.event.get():
            if event.type == pg.FINGERDOWN or event.type == pg.FINGERMOTION:
                touch_pos = (event.x * self.game_size[0], event.y * self.game_size[1])
                for direction, (image, pos) in self.image_controls.items():
                    image_rect = pg.Rect(pos[0], pos[1], image.get_width(), image.get_height())
                    if image_rect.collidepoint(touch_pos):
                        self.active_touches[event.finger_id] = direction
            elif event.type == pg.FINGERUP:
                if event.finger_id in self.active_touches:
                    del self.active_touches[event.finger_id]
            elif event.type == pg.QUIT:
                pygame_event.running = False

        # Update mobile keys
        mobile_key = {"K_UP": False, "K_LEFT": False, "K_RIGHT": False, "K_DOWN": False, "K_A": False, "K_B": False}
        for direction in self.active_touches.values():
            if direction == "UP":
                mobile_key["K_UP"] = True
            if direction == "LEFT":
                mobile_key["K_LEFT"] = True
            if direction == "RIGHT":
                mobile_key["K_RIGHT"] = True
            if direction == "DOWN":
                mobile_key["K_DOWN"] = True
            if direction == "A":
                mobile_key["K_A"] = True
            if direction == "B":
                mobile_key["K_B"] = True
        return mobile_key

    def draw_for_android(self, display):
        for direction, (image, pos) in self.image_controls.items():
            display.blit(image, pos)

    def update_for_web(self, pygame_event):
        pygame_event.check()
        return pg.key.get_pressed()
