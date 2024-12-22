import pygame as pg
from .timer import Timer

class Input:
    def __init__(self, platform, game_size = []) -> None:
        if platform == 'pc':
            self.fullscreen_toggle_timer = Timer()
            self.fullscreen_toggle_timer.start()
        elif platform == 'android':
            self.game_size = game_size
            rect1 = (pg.Rect(40, 30, 30, 30), "UP")
            rect2 = (pg.Rect(5, 65, 30, 30), "LEFT")
            rect3 = (pg.Rect(75, 65, 30, 30), "RIGHT")
            rect4 = (pg.Rect(40, 100, 30, 30), "DOWN")
            rect5 = (pg.Rect(game_size[0] - 90, 77, 30, 30), "A")
            rect6 = (pg.Rect(game_size[0] - 50, 77, 30, 30), "B")
            self.all_rect = [rect1, rect2, rect3, rect4, rect5, rect6]
            self.active_touches = {}  # Store touch points and their corresponding actions

    def update_for_pc(self, pygame_event, display):
        new_size = pygame_event.check()
        if new_size:
            display = new_size
        key = pg.key.get_pressed()
        if key[pg.K_f] or key[pg.K_F11]:
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
                for rect, direction in self.all_rect:
                    if rect.collidepoint(touch_pos):
                        self.active_touches[event.finger_id] = direction
            elif event.type == pg.FINGERUP:
                if event.finger_id in self.active_touches:
                    del self.active_touches[event.finger_id]
            elif event.type == pg.QUIT:
                pygame_event.running = False

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

    def draw_for_android(self, display, color1, color2):
        for rect, direction in self.all_rect:
            if direction in self.active_touches.values():
                pg.draw.rect(display, color1, rect, border_radius=5)
            else:
                pg.draw.rect(display, color2, rect, border_radius=5)

    def update_for_web(self, pygame_event):
        pygame_event.check()
        return pg.key.get_pressed()
