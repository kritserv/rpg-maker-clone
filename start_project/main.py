web = False

import pygame as pg
from time import time

import asyncio
if web:
    OpenGLStuff = None
else:
    """
    OpenGL Stuff
    I don't know what any of these code do, I copy it from dafluffypotato.
    """
    import pygame as pg
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

    if not web:
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
            opengl.draw(display)

            await asyncio.sleep(0)

    else:
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

            # Not use OpenGL if not web
            pg.transform.scale(display, screen.get_size(), screen)
            pg.display.flip()

            await asyncio.sleep(0)

    pg.quit()
    exit()

if __name__ == "__main__":
    asyncio.run(main())
