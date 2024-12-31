import asyncio
import pygame as pg
from sys import exit

pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.font.init()
pg.init()

import os
full_path = f"{os.path.abspath('.')}/"

with open(f"{full_path}/game_data/game_mode.txt") as f:
    game_mode = f.readlines()[0].rstrip('\n') # pc / android / web

game_size = [256, 137]
native_res_multiplier = 3
game_size_native = (game_size[0]*native_res_multiplier, game_size[1]*native_res_multiplier)

if game_mode == 'android':
    phone_width, phone_height = pg.display.get_desktop_sizes()[0]
    # scale game_width to match phone_width
    phone_ratio = phone_width / phone_height
    while game_size[0] / game_size[1] < phone_ratio:
        game_size[0] += 1

from src import json_loader, Player, RpgMap, Camera, Input, DeltaTime, PygameEvent, Timer, blit_text, TopUI

def load_game(player_start_pos, start_map, db, screen):
    player = Player(full_path, player_start_pos)
    rpgmap = RpgMap(full_path, start_map, game_size)
    rpgmap.load_map_data(db["maps"])
    camera_width, camera_height = screen.get_size()
    camera = Camera(camera_width, camera_height, game_size[0])
    top_ui = TopUI(full_path)
    return player, rpgmap, camera, top_ui

async def main():
    delta_time = DeltaTime()
    display = pg.Surface((game_size))

    # load data
    db = json_loader(f"{full_path}game_data/db.json")
    pg.display.set_caption(db["main"]["main_title"])
    start_map = db["start_map"]
    player_start_pos = db["player_start_position"]

    # load settings
    settings = json_loader(f"{full_path}user_data/settings.json")

    clock = pg.time.Clock()

    GREY = pg.Color("grey20")
    BLACK = pg.Color("black")

    font_path = f"{full_path}assets/fonts/PixelatedElegance.ttf"
    fps_font = pg.font.Font(font_path, 16)

    pygame_event = PygameEvent(game_size=game_size)

    if game_mode == 'pc':
        """
        OpenGL Stuff; for better FPS, resizable game windows and for steam achievement overlay
        I don't know what any of these code do, I just copy it from dafluffypotato.
        """
        import moderngl
        from array import array

        class OpenGLStuff:
            def __init__(self):
                self.ctx = moderngl.create_context()
                self.quad_buffer = self.ctx.buffer(data=array("f", [
                    -1.0, 1.0, 0.0, 0.0,
                    1.0, 1.0, 1.0, 0.0,
                    -1.0, -1.0, 0.0, 1.0,
                    1.0, -1.0, 1.0, 1.0
                    ]))

                vert_shader = '''
                #version 330 core

                in vec2 vert;
                in vec2 textcoord;
                out vec2 uvs;

                void main() {
                    uvs = textcoord;
                    gl_Position = vec4(vert, 0.0, 1.0);
                }
                '''

                frag_shader = '''
                #version 330 core

                uniform sampler2D tex;

                in vec2 uvs;
                out vec4 f_color;

                void main() {
                    f_color = vec4(texture(tex, uvs).rgb, 1.0);
                }
                '''

                self.program = self.ctx.program(
                    vertex_shader=vert_shader,
                    fragment_shader=frag_shader
                    )

                self.render_object = self.ctx.vertex_array(
                    self.program,
                    [
                        (
                            self.quad_buffer,
                             "2f 2f",
                             "vert",
                             "textcoord"
                            )
                    ]
                    )

            def surf_to_texture(self, surf) -> object:
                tex = self.ctx.texture(surf.get_size(), 4)
                tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
                tex.swizzle = "BGRA"
                tex.write(surf.get_view("1"))
                return tex

            def draw(self, display) -> None:
                frame_tex = self.surf_to_texture(display)
                frame_tex.use(0)
                self.program["tex"] = 0
                self.render_object.render(
                    mode=moderngl.TRIANGLE_STRIP
                    )

                pg.display.flip()

                frame_tex.release()

        screen = pg.display.set_mode(
            (game_size_native),
            pg.RESIZABLE | (pg.OPENGL | pg.DOUBLEBUF)
        )

        """
        Use this if prefer game to open in maximize window instead of the default one.
        """
        # from pygame._sdl2 import Window
        # Window.from_display_module().maximize()

        pg.display.set_icon(pg.image.load("assets/icon.png").convert_alpha())
        player, rpgmap, camera, top_ui = load_game(player_start_pos, start_map, db, screen)

        opengl = OpenGLStuff()
        input = Input('pc')

        debug_message = ''
        from src import run_pc_game_loop
        while pygame_event.running:
            display = run_pc_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, BLACK, top_ui, debug_message, fps_font, opengl)
            await asyncio.sleep(0)

    elif game_mode == 'android':
        screen = pg.display.set_mode((game_size),
            pg.SCALED)
        pg.display.toggle_fullscreen()
        player, rpgmap, camera, top_ui = load_game(player_start_pos, start_map, db, screen)

        input = Input('android', game_size, full_path)

        from src import run_android_game_loop
        while pygame_event.running:
            run_android_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, top_ui, screen)
            await asyncio.sleep(0)
    else:
        import sys, platform
        if sys.platform == "emscripten":
            platform.window.canvas.style.imageRendering = "pixelated"
        screen = pg.display.set_mode(
            (game_size_native),
            pg.RESIZABLE)
        player, rpgmap, camera, top_ui = load_game(player_start_pos, start_map, db, screen)

        input = Input('web')

        from src import run_web_game_loop
        while pygame_event.running:
            run_web_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, top_ui, screen)
            await asyncio.sleep(0)

    pg.quit()
    exit()

if __name__ == "__main__":
    asyncio.run(main())
