web = False
android = False
pc = True

import asyncio
import pygame as pg
from sys import exit

pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
pg.font.init()

import os
full_path = f"{os.path.abspath('.')}/"

game_size = [256, 137]
native_res_multiplier = 3
game_size_native = (game_size[0]*native_res_multiplier, game_size[1]*native_res_multiplier)

if android:
    phone_width, phone_height = pg.display.get_desktop_sizes()[0]
    # scale game_width to match phone_width
    phone_ratio = phone_width / phone_height
    while game_size[0] / game_size[1] < phone_ratio:
        game_size[0] += 1

def toggle_full_screen():
    pg.display.toggle_fullscreen()

"""
Use this if prefer maximize window instead of the default one.
"""
# from pygame._sdl2 import Window
# Window.from_display_module().maximize()

from src import json_loader, Player, RpgMap, Camera, DeltaTime, PygameEvent, Timer, blit_text

def load_game(player_start_pos, start_map, db, screen):
    player = Player(full_path, player_start_pos)
    rpgmap = RpgMap(full_path, start_map)
    rpgmap.load_map_data(db["maps"])
    camera_width, camera_height = screen.get_size()
    camera = Camera(camera_width, camera_height, game_size[0])
    return player, rpgmap, camera

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
    scale_method = settings["scale_method"]
    scale_on_x_axis = scale_method == "by windows width"

    clock = pg.time.Clock()

    GREY = pg.Color("grey20")
    RED = pg.Color("red")
    BLUE = pg.Color("blue")
    BLACK = pg.Color("black")

    pygame_event = PygameEvent(game_size=game_size, scale_on_x_axis=scale_on_x_axis)

    if pc:
        """
        OpenGL Stuff; for better FPS
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

        screen = pg.display.set_mode(
            (game_size_native),
            pg.RESIZABLE | (pg.OPENGL | pg.DOUBLEBUF)
        )
        pg.display.set_icon(pg.image.load("assets/icon.png").convert_alpha())
        player, rpgmap, camera = load_game(player_start_pos, start_map, db, screen)

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
            camera.update(player)

            # Graphic
            display.fill(GREY)
            rpgmap.draw(display, camera)
            display.blit(player.img, [display.get_size()[0]//2-16, display.get_size()[1]//2+-22])#player.pos)

            # Use OpenGL for desktop
            opengl.draw(display)

            await asyncio.sleep(0)
    elif android:

        screen = pg.display.set_mode((game_size),
            pg.SCALED)
        toggle_full_screen()
        player, rpgmap, camera = load_game(player_start_pos, start_map, db, screen)

        rect1 = (pg.Rect(40, 30, 30, 30), "UP")
        rect2 = (pg.Rect(5, 65, 30, 30), "LEFT")
        rect3 = (pg.Rect(75, 65, 30, 30), "RIGHT")
        rect4 = (pg.Rect(40, 100, 30, 30), "DOWN")
        rect5 = (pg.Rect(game_size[0] - 90, 77, 30, 30), "A")
        rect6 = (pg.Rect(game_size[0] - 50, 77, 30, 30), "B")
        all_rect = [rect1, rect2, rect3, rect4, rect5, rect6]
        use_font = pg.font.SysFont(None, 22)
        fps = 0
        fps_update_timer = Timer()
        fps_update_timer.start()
        active_touches = {}  # Store touch points and their corresponding actions

        while pygame_event.running:
            dt = delta_time.get()
            clock.tick()

            # Input
            for event in pg.event.get():
                if event.type == pg.FINGERDOWN or event.type == pg.FINGERMOTION:
                    touch_pos = (event.x * game_size[0], event.y * game_size[1])
                    for rect, direction in all_rect:
                        if rect.collidepoint(touch_pos):
                            active_touches[event.finger_id] = direction
                elif event.type == pg.FINGERUP:
                    if event.finger_id in active_touches:
                        del active_touches[event.finger_id]
                elif event.type == pg.QUIT:
                    pygame_event.running = False

            mobile_key = {"K_UP": False, "K_LEFT": False, "K_RIGHT": False, "K_DOWN": False, "K_A": False, "K_B": False}
            for direction in active_touches.values():
                if direction == "UP":
                    mobile_key["K_UP"] = True
                if direction == "LEFT":
                    mobile_key["K_LEFT"] = True
                if direction == "RIGHT":
                    mobile_key["K_RIGHT"] = True
                if direction == "DOWN":
                    mobile_key["K_DOWN"] = True
                if direction == "A":
                    mobile_key["K_A"] = True
                if direction == "B":
                    mobile_key["K_B"] = True

            # Logic
            player.update(key=None, dt=dt, mobile_key=mobile_key)
            camera.update(player)

            # Graphic
            display.fill(GREY)
            rpgmap.draw_scaled_screen(display, camera, game_size)
            display.blit(player.img, [display.get_size()[0]//2-16, display.get_size()[1]//2+-22])

            for rect, direction in all_rect:
                if direction in active_touches.values():
                    pg.draw.rect(display, RED, rect, border_radius=5)
                else:
                    pg.draw.rect(display, BLUE, rect, border_radius=5)

            if fps_update_timer.get_elapsed_time() >= 0.5:
                fps = round(clock.get_fps(), 2)
                fps_update_timer.restart()
            blit_text(display, f'FPS:{fps}', use_font, BLACK, (10, 10))

            pg.transform.scale(display, screen.get_size(), screen)
            pg.display.flip()

            await asyncio.sleep(0)
    else:
        screen = pg.display.set_mode(
            (game_size_native),
            pg.RESIZABLE)
        player, rpgmap, camera = load_game(player_start_pos, start_map, db, screen)

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
            camera.update(player)

            # Graphic
            display.fill(GREY)
            rpgmap.draw(display, camera)
            display.blit(player.img, [display.get_size()[0]//2-16, display.get_size()[1]//2+-22])

            pg.transform.scale(display, screen.get_size(), screen)
            pg.display.flip()

            await asyncio.sleep(0)

    pg.quit()
    exit()

if __name__ == "__main__":
    asyncio.run(main())
