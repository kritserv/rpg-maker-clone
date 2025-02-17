import pygame as pg

class Command(pg.sprite.Sprite):
    def __init__(self, sequence, xy):
        self.sequence = sequence
        self.pos = pg.math.Vector2(xy)

    def update_for_pc(self, display, dt, current_time, key, joystick):
        if self.sequence:
            self.sequence[0].draw(display, dt, current_time)
            self.sequence[0].update_for_pc(key, joystick)


    def update_for_android(self, display, dt, current_time, mobile_key):
        if self.sequence:
            self.sequence[0].draw(display, dt, current_time)
            self.sequence[0].update_for_android(mobile_key)
