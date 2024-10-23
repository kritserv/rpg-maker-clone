web = True

import pygame as pg
from time import time

import asyncio
if not web:
    import moderngl
    from src import OpenGLStuff

pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

from sys import exit

game_size = (240, 137)

native_res_multiplier = 3
screen = pg.display.set_mode(
    (game_size[0]*native_res_multiplier, game_size[1]*native_res_multiplier),
    pg.RESIZABLE | (pg.OPENGL | pg.DOUBLEBUF if not web else 0)
)

from src import json_loader, Player, RpgMap, DeltaTime, PygameEvent, blit_text

pg.display.set_icon(pg.image.load("assets/icon.png").convert_alpha())

async def main():
    display = pg.Surface((game_size))

    if not web:
        opengl = OpenGLStuff()

    db = json_loader("game_data/db.json")
    pg.display.set_caption(db["main"]["main_title"])

    settings = json_loader("user_data/settings.json")
    scale_method = settings["scale_method"]

    player = Player(0, 64)
    rpgmap = RpgMap()
    rpgmap.load_map_data(db["maps"])

    clock = pg.time.Clock()
    grey = pg.Color("grey20")

    delta_time = DeltaTime()
    scale_on_x_axis = scale_method == "by windows width"
    pygame_event = PygameEvent(game_size=game_size, scale_on_x_axis=scale_on_x_axis)

    while pygame_event.running:
        dt = delta_time.get()
        clock.tick()

        # Input
        new_size = pygame_event.check()
        if new_size:
            display = new_size
        key = pg.key.get_pressed()

        # Logic
        player.update(key, dt)

        # Graphic
        display.fill(grey)
        rpgmap.draw(display)
        display.blit(player.img, player.pos)

        # Use OpenGL if not web
        if not web:
            opengl.draw(display)
        else:
            pg.transform.scale(display, screen.get_size(), screen)
            pg.display.flip()

        await asyncio.sleep(0)

    pg.quit()
    exit()

if __name__ == "__main__":
    if web:
        asyncio.run(main())
    else:
        main()
