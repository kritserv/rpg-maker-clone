import pygame as pg
from .blit_text import blit_text

class MenuUI:
    def __init__(self, full_path):
        font_path = f"{full_path}assets/fonts/PixelatedElegance.ttf"
        self.menu_font = pg.font.Font(font_path, 9)

        self.BLUE = pg.Color('darkblue')
        self.GREY = pg.Color('grey90')
        self.WHITE = pg.Color('white')

    def draw(self, display):
        menu_x = display.get_size()[0]-112
        menu_y = 2
        menu_w = 110
        menu_h = display.get_size()[1]-45
        pg.draw.rect(display, self.BLUE, (menu_x,menu_y,menu_w,menu_h))
        for i in range(4):
            pg.draw.rect(display, self.GREY, (menu_x-i,menu_y-i,menu_w+1,menu_h+1), 1)
        menu_text_x = display.get_size()[0]-100
        menu_text_y = 6
        for menu_text in ('Inventory', 'Skills', 'Achievement', 'Save', 'Load', 'Option', 'Exit to title'):
            blit_text(display, menu_text, self.menu_font, self.WHITE, (menu_text_x, menu_text_y))
            menu_text_y += 12
