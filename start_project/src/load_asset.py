import pygame as pg
import os
full_path = f"{os.path.abspath('.')}/"

class NoSound:
    def play(self):
        pass

noimage = pg.image.fromstring(b'\x00\x00\x00\xff\xa0\xf3\xff\xa0\xf3\x00\x00\x00', (2, 2), 'RGB')
def asset_loader(asset_type: str, asset: str) -> pg.mixer.Sound | NoSound | pg.Surface | pg.font.Font:
    match asset_type:
        case 'sfx':
            try:
                return pg.mixer.Sound(f"{full_path}assets/sfx/{asset}.ogg")
            except OSError as e:
                print(e)
                return NoSound()
        case 'sprite':
            try:
                return pg.image.load(f"{full_path}assets/img/sprite/{asset}.png").convert_alpha()
            except OSError as e:
                print(e)
                match asset:
                    case 'player':
                        return pg.transform.scale(noimage, (48, 192))
                    case _:
                        return pg.transform.scale(noimage, (24, 24))
        case 'tile':
            try:
                return pg.image.load(f"{full_path}assets/img/tile/{asset}.png").convert_alpha()
            except OSError as e:
                print(e)
                return pg.transform.scale(noimage, (16, 16))
        case 'img':
            try:
                return pg.image.load(f"{full_path}assets/{asset}.png").convert_alpha()
            except OSError as e:
                print(e)
                return noimage
        case 'font':
            try:
                return pg.font.Font(f"{full_path}assets/font/{asset}.ttf", 9)
            except OSError as e:
                print(e)
                return pg.font.SysFont('', size=14)
        case _:
            raise Exception(f"Unknown asset type: {asset_type}")
