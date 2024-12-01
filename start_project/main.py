web = False
android = False

import asyncio
import pygame as pg
from sys import exit

pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()


if not web:
    """
    OpenGL Stuff; for better FPS in desktop high resolution.
    I don't know what any of these code do, I copy it from dafluffypotato.
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

game_size = (240, 137)
native_res_multiplier = 3
game_size_native = (game_size[0]*native_res_multiplier, game_size[1]*native_res_multiplier)


screen = pg.display.set_mode(
    (game_size_native),
    pg.RESIZABLE | (pg.OPENGL | pg.DOUBLEBUF if not web else 0)
)

"""
Use this if prefer maximize window instead of the default one.
"""
# from pygame._sdl2 import Window
# Window.from_display_module().maximize()

from src import json_loader, Player, RpgMap, DeltaTime, PygameEvent, Timer, blit_text

def toggle_full_screen():
    pg.display.toggle_fullscreen()

if android:
    screen = pg.display.set_mode(game_size,
        pg.SCALED)
    toggle_full_screen()

pg.display.set_icon(pg.image.load("assets/icon.png").convert_alpha())

async def main():
    display = pg.Surface((game_size))

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
    # print(game_size_native)
    pygame_event = PygameEvent(game_size=game_size, scale_on_x_axis=scale_on_x_axis)

    if not web and not android:
        opengl = OpenGLStuff()
        fullscreen_toggle_timer = Timer()
        fullscreen_toggle_timer.start()
        while pygame_event.running:
            dt = delta_time.get()
            clock.tick()

            # Input
            new_size = pygame_event.check()
            if new_size:
                display = new_size
            key = pg.key.get_pressed()
            if key[pg.K_f] or key[pg.K_F11]:
                if fullscreen_toggle_timer.get_elapsed_time() >= 0.3:
                    toggle_full_screen()
                    fullscreen_toggle_timer.restart()
            if fullscreen_toggle_timer.get_elapsed_time() >= 0.5:
                fullscreen_toggle_timer.pause()

            # Logic
            player.update(key, dt)

            # Graphic
            display.fill(grey)
            rpgmap.draw(display)
            display.blit(player.img, player.pos)
            display.blit(player.img, player.pos)

            # Use OpenGL for desktop
            opengl.draw(display)

            await asyncio.sleep(0)
    elif android:
        rect1 = (pg.Rect(15, 100, 10, 10), "UP")
        rect2 = (pg.Rect(5, 110, 10, 10), "LEFT")
        rect3 = (pg.Rect(25, 110, 10, 10), "RIGHT")
        rect4 = (pg.Rect(15, 120, 10, 10), "DOWN")
        all_rect = [rect1, rect2, rect3, rect4]
        RED = (255, 0 , 0)
        BLUE = (0, 0, 255)
        while pygame_event.running:
            dt = delta_time.get()
            clock.tick()

            # Input
            new_size = pygame_event.check()
            if new_size:
                display = new_size
            key = pg.key.get_pressed()
            mouse = pg.mouse.get_pos()

            mobile_key = {"K_UP": False, "K_LEFT": False, "K_RIGHT": False, "K_DOWN": False}
            if pygame_event.click:
                for rect, direction in all_rect:
                    if rect.collidepoint(mouse):
                        if direction == "UP":
                            mobile_key["K_UP"] = True
                        if direction == "LEFT":
                            mobile_key["K_LEFT"] = True
                        if direction == "RIGHT":
                            mobile_key["K_RIGHT"] = True
                        if direction == "DOWN":
                            mobile_key["K_DOWN"] = True

            # Logic
            player.update(key, dt, mobile_key)

            # Graphic
            display.fill(grey)
            rpgmap.draw(display)
            display.blit(player.img, player.pos)

            for rect, direction in all_rect:
                if rect.collidepoint(mouse):
                    pg.draw.rect(display, RED, rect)
                else:
                    pg.draw.rect(display, BLUE, rect)

            # Can't use OpenGL for android (Mobile Controller will not work.)
            pg.transform.scale(display, screen.get_size(), screen)
            pg.display.flip()

            await asyncio.sleep(0)
    elif web:
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

            # Can't use OpenGL if web
            pg.transform.scale(display, screen.get_size(), screen)
            pg.display.flip()

            await asyncio.sleep(0)

    pg.quit()
    exit()

if __name__ == "__main__":
    asyncio.run(main())