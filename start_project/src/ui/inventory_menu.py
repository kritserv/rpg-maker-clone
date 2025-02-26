from .base_menu import BaseMenuUI
from .text_blit import blit_text
from .image_blit import blit_img
import pygame as pg

class MenuUIInventory(BaseMenuUI):
    def __init__(self, saves_file_path, g):
        menu_items = (
            ' ',
        )
        super().__init__(menu_items, g)
        self.speed = 20
        self.play_sound = True

    def draw(self, display, dt, current_time, player_items, item_dict):
        menu_y_finish = 5
        if self.cursor >= 10:
            menu_y_finish = self.cursor * -8
        else:
            menu_y_finish = 5

        if self.menu_y > menu_y_finish:
            self.menu_y -= self.speed * dt
            self.speed += 800 * dt
            slide_in = True
        else:
            slide_in = False
            self.menu_y = menu_y_finish

        menu_x = 2
        menu_w = 120
        if len(self.menu) <= 10:
            menu_h = 127
        else:
            menu_h = len(self.menu)*13

        pg.draw.rect(display, self.DARKBLUE, (menu_x, self.menu_y, menu_w, menu_h))
        menu_text_y = self.menu_y + 6

        select_item = item_dict.get(self.menu[self.cursor])
        select_item_quant = 0
        select_item_is_equip = False
        if select_item and player_items.get(select_item.name):
            select_item_quant = player_items[select_item.name]['quant']
            select_item_is_equip = player_items[select_item.name]['is_equip']

        add_text = ''
        if select_item_quant:
            add_text = f' : {select_item_quant}'

        blink_on = (current_time // self.cursor_blink_interval) % 2 == 0
        for i, menu_text in enumerate(self.menu):
            if i == self.cursor:
                pg.draw.rect(display, self.BLUE, (menu_x, menu_text_y-3, menu_w, 12))
                if blink_on:
                    blit_text(display, f'> {menu_text}{add_text}', self.menu_font, self.YELLOW, (menu_x+12, menu_text_y))
                else:
                    blit_text(display, f'  {menu_text}{add_text}', self.menu_font, self.YELLOW, (menu_x+12, menu_text_y))

            else:
                blit_text(display, menu_text, self.menu_font, self.WHITE, (menu_x+12, menu_text_y))

            menu_text_y += 12
        for i in range(4):
            pg.draw.rect(display, self.GREY, (menu_x - i, self.menu_y - i, menu_w + 1, menu_h + 1), 1)

        if select_item:
            width = display.get_width()
            height = display.get_height()
            blit_img(display, select_item.img, (menu_w + width//20, height//6))
            blit_text(display, select_item.description, self.menu_font, self.WHITE, (menu_w + width//20, height//2*1.3))
            if select_item.is_equipable:
                if select_item_is_equip:
                    blit_text(display, 'is equip', self.menu_font, self.WHITE, (menu_w + width//20, height//10))
                else:
                    blit_text(display, 'is unequip', self.menu_font, self.WHITE, (menu_w + width//20, height//10))

        return slide_in
