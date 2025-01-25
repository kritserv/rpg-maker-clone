import pygame as pg
import os
full_path = f"{os.path.abspath('.')}/"

def asset_loader(asset_type, asset):
    match asset_type:
        case 'sfx':
            return pg.mixer.Sound(f"{full_path}assets/sfx/{asset}.ogg")
        case 'sprite':
            return pg.image.load(f"{full_path}assets/img/sprite/{asset}.png").convert_alpha()
        case 'tile':
            return pg.image.load(f"{full_path}assets/img/tile/{asset}.png").convert_alpha()
        case 'img':
            return pg.image.load(f"{full_path}assets/{asset}.png").convert_alpha()
        case 'font':
            return pg.font.Font(f"{full_path}assets/font/{asset}.ttf", 9)
        case _:
            raise Exception(f"Unknown asset type: {asset_type}")
