import pygame as pg
from ..ui import blit_text

class Conversation:
    def __init__(self, font, dialogs):
        self.font = font
        self.blink_interval = 200

        self.dialogs = dialogs
        self.active_dialog = 0
        self.message_done = False
        self.finish = False
        self.speed = 20

        self.index = 0

        self.BLACK = pg.Color('black')
        self.WHITE = pg.Color('white')

    def draw(self, display, dt, current_time):
        if not self.finish:
            height = display.get_height()
            height_div_3 = height//2.5
            width = display.get_width()
            pg.draw.rect(display, self.BLACK, [20, height-height_div_3, width-40, height_div_3])

            dialog = self.dialogs[self.active_dialog]

            if not self.message_done:
                speed = self.speed * dt
                if speed == 0:
                    speed = 0.01

                if self.index >= len(dialog):
                    self.message_done = True

                self.index += speed

            show_text = dialog[0:int(self.index)]
            if self.message_done:
                blink_on = (current_time // self.blink_interval) % 2 == 0
                if blink_on:
                    blit_text(display, '->', self.font, self.WHITE, (width-40, height-height_div_3+35))
            blit_text(display, show_text, self.font, self.WHITE, (25, height-height_div_3+5))

    def update(self, action, player):
        if action:
            if self.message_done:
                self.active_dialog += 1

                if self.active_dialog >= len(self.dialogs):
                    self.finish = True
                    self.active_dialog = 0

                self.message_done = False
                self.index = 0
            else:
                self.speed = 40
        else:
            self.speed = 20

    def update_for_pc(self, key, joysticks, player, item_dict):
        action = key[pg.K_RETURN] or key[pg.K_KP_ENTER] or key[pg.K_z] or key[pg.K_SPACE]
        for joystick in joysticks:
            action = joystick.get_button(1)
        self.update(action, player)

    def update_for_android(self, mobile_key, player, item_dict):
        action = mobile_key["K_A"]
        self.update(action, player)
