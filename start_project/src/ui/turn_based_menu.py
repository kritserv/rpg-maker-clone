from .base_menu import BaseMenuUI
from .text_blit import blit_text
from .image_blit import blit_img
import pygame as pg
from .conversation import Conversation

class MenuUITurnbased(BaseMenuUI):
    def __init__(self, g):
        menu_items = ('Skill', 'Item', 'Skip', 'Run')
        super().__init__(menu_items, g)
        self.speed = 20
        self.play_sound = True
        self.state = 'exit'
        self.infomation = Conversation(self.menu_font, [' '])
        self.current_enemy = ''

    def draw(self, display, dt, current_time):
        menu_y_finish = self.game_size[1]-55
        if self.menu_y > menu_y_finish:
            self.menu_y -= self.speed * dt
            self.speed += 800 * dt
            slide_in = True
        else:
            slide_in = False
            self.menu_y = menu_y_finish

        menu_x = display.get_width()-150
        menu_w = 110
        menu_h = 55
        pg.draw.rect(display, self.DARKBLUE, (menu_x, self.menu_y, menu_w, menu_h))
        menu_text_y = self.menu_y + 6
        blink_on = (current_time // self.cursor_blink_interval) % 2 == 0
        for i, menu_text in enumerate(self.menu):
            if i == self.cursor:
                pg.draw.rect(display, self.BLUE, (menu_x, menu_text_y-3, menu_w, 12))
                if blink_on:
                    blit_text(display, '→ ' + menu_text, self.menu_font, self.YELLOW, (menu_x+12, menu_text_y))
                else:
                    blit_text(display, '    ' + menu_text, self.menu_font, self.YELLOW, (menu_x+12, menu_text_y))
            else:
                blit_text(display, menu_text, self.menu_font, self.WHITE, (menu_x+12, menu_text_y))
            menu_text_y += 12
        for i in range(4):
            pg.draw.rect(display, self.GREY, (menu_x - i, self.menu_y - i, menu_w + 1, menu_h + 1), 1)

        return slide_in

    def draw2(self, display, dt, current_time, player, enemy):
        display.fill('black')

        if player.hp < 0:
            player.hp = 0
        if enemy.hp < 0:
            enemy.hp = 0

        if enemy.hp > 0:
            blit_img(display, enemy.img, enemy.img.get_rect(center=(display.get_width()//2, display.get_height()//4)))

        player_hp = player.hp/player.max_hp
        if 0.4 > player_hp >= 0:
            rect_col = 'red'
            font_col = 'darkred'
        elif 0.7 > player_hp >= 0.4:
            rect_col = 'yellow'
            font_col = 'orange'
        else:
            rect_col = 'green'
            font_col = 'darkgreen'

        blit_text(display, f'player: {player.hp} / {player.max_hp}', self.menu_font, pg.Color(font_col), (5,70))
        pg.draw.rect(display, pg.Color('grey20'), (5, 80, 100, 6))
        pg.draw.rect(display, pg.Color(rect_col), (5, 80, int(player.hp/player.max_hp*100), 6))

        enemy_hp = enemy.hp/enemy.max_hp
        if 0.4 > enemy_hp >= 0:
            rect_col = 'red'
            font_col = 'darkred'
        elif 0.7 > enemy_hp >= 0.4:
            rect_col = 'yellow'
            font_col = 'orange'
        else:
            rect_col = 'green'
            font_col = 'darkgreen'

        blit_text(display, f'{enemy.name}: {enemy.hp} / {enemy.max_hp}', self.menu_font, font_col, (display.get_width()-135,5))
        pg.draw.rect(display, pg.Color('grey20'), (display.get_width()-135, 15, 100, 6))
        pg.draw.rect(display, rect_col, (display.get_width()-135, 15, int(enemy.hp/enemy.max_hp*100), 6))
