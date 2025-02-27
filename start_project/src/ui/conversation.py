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
        self.delay = 10

        for i in range(len(self.dialogs)):
            self.dialogs[i] += ' ' * self.delay

        self.index = 0

        self.BLUE = pg.Color('darkblue')
        self.WHITE = pg.Color('white')
        self.GREY = pg.Color('grey90')

    def draw(self, display, dt, current_time):
        if not self.finish:
            height = display.get_height()
            height_div_3 = height//2.5
            width = display.get_width()

            pg.draw.rect(display, self.BLUE, [20, height-height_div_3, width-40, height_div_3])
            for i in range(4):
                pg.draw.rect(display, self.GREY, (20 - i, height-height_div_3 - i, width-40 + 1, height_div_3 + 1), 1)

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
                    blit_text(display, '->', self.font, self.WHITE, (width//2-8, height-height_div_3+45))
            blit_text(display, show_text, self.font, self.WHITE, (width//5, height-height_div_3+5))

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

    def update_for_pc(self, dt, key, joysticks, player, rpgmap, pygame_event, menu_ui_turn_based, command_list):
        # use any key to progress conversation
        action = key[pg.K_RETURN] or key[pg.K_KP_ENTER] or key[pg.K_z] or key[pg.K_SPACE] or key[pg.K_x] or key[pg.K_ESCAPE] or key[pg.K_KP_0]
        for joystick in joysticks:
            action = joystick.get_button(0)
            if not action:
                action = joystick.get_button(1)
        self.update(action, player)

    def update_for_android(self, dt, mobile_key, player, rpgmap, pygame_event, menu_ui_turn_based, command_list):
        # use any key to progress conversation
        action = mobile_key["K_A"] or mobile_key["K_B"]
        self.update(action, player)
