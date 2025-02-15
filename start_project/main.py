import asyncio
import pygame as pg
from sys import exit

pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.font.init()
pg.joystick.init()
pg.init()

import os
full_path = f"{os.path.abspath('.')}/"

with open(f"{full_path}/game_data/game_mode.txt") as f:
    game_mode = f.readlines()[0].rstrip('\n') # pc / android / web

g = {
    'game_mode': game_mode,
    'game_size': [256, 137],
    'font': {},
    'full_path': full_path,
    'colors': {
        'black': pg.Color('black'),
        'grey': pg.Color('grey20'),
        'lightgrey': pg.Color('grey90'),
        'green': pg.Color('green'),
        'darkblue': pg.Color('darkblue'),
        'blue': pg.Color('blue'),
        'lightblue': pg.Color('skyblue'),
        'yellow': pg.Color('yellow'),
        'white': pg.Color('white'),
        'pink': pg.Color('hotpink')
    }
}

native_res_multiplier = 4
game_size_native = (
    g['game_size'][0]*native_res_multiplier,
    g['game_size'][1]*native_res_multiplier
)

if g['game_mode'] == 'android':
    phone_width, phone_height = pg.display.get_desktop_sizes()[0]
    # scale game_width to match phone_width
    phone_ratio = phone_width / phone_height
    while g['game_size'][0] / g['game_size'][1] < phone_ratio:
        g['game_size'][0] += 1

from src import json_loader, run_game_loop, \
    Player, RpgMap, Camera, Input, DeltaTime, PygameEvent, Timer, \
    blit_text, DebugUI, \
    MenuUI, MenuUISave, MenuUILoad, MenuUITitle, MenuUISettings, \
    MenuUIInventory, MenuUISkills, MenuUIAchievement, \
    asset_loader, load_player_sprite, load_map_data

def load_asset(db):
    player_img = load_player_sprite()
    all_tile_imgs = {}
    tile_data = json_loader(f'{full_path}game_data/data/maps/tilesets.json')
    for map_name in tile_data:
        for tile_id in tile_data[map_name]:
            all_tile_imgs[tile_data[map_name][tile_id]] = asset_loader(
                'tile', tile_data[map_name][tile_id]
            )
    open_menu_sfx = asset_loader('sfx', 'open_menu')
    select_sfx = asset_loader('sfx', 'select')
    font_9 = asset_loader('font', 'PixelatedElegance', 9)
    font_18 = asset_loader('font', 'PixelatedElegance', 18)
    return player_img, all_tile_imgs, open_menu_sfx, select_sfx, font_9, font_18

def load_game(player_start_pos, start_map, db, screen, save_file_path):
    player_img, all_tile_imgs, open_menu_sfx, select_sfx, font_9, font_18 = load_asset(db)
    g['font']['font_9'] = font_9
    g['font']['font_18'] = font_18
    player = Player(player_start_pos, player_img)
    rpgmap = RpgMap(start_map, g, load_map_data(db["maps"], all_tile_imgs))
    camera_width, camera_height = screen.get_size()
    camera = Camera(camera_width, camera_height, g)
    debug_ui = DebugUI(g)
    menu_ui = MenuUI(g)
    menu_ui.open_menu_sfx = open_menu_sfx
    menu_ui.select_sfx = select_sfx
    menu_ui_save = MenuUISave(save_file_path, g)
    menu_ui_save.select_sfx = select_sfx
    menu_ui_load = MenuUILoad(save_file_path, g)
    menu_ui_load.select_sfx = select_sfx
    menu_ui_title = MenuUITitle(g)
    menu_ui_settings = MenuUISettings(save_file_path, g)
    menu_ui_inventory = MenuUIInventory(save_file_path, g)
    menu_ui_inventory.select_sfx = select_sfx
    menu_ui_skills = MenuUISkills(save_file_path, g)
    menu_ui_skills.select_sfx = select_sfx
    menu_ui_achievement = MenuUIAchievement(save_file_path, g)
    menu_ui_achievement.select_sfx = asset_loader('sfx', 'select')
    first_sound_volume = menu_ui_settings.sound_slider.save_value/100
    first_music_volume = menu_ui_settings.music_slider.save_value/100
    if first_sound_volume<0:
        first_sound_volume=0
    menu_ui.select_sfx.set_volume(first_sound_volume)
    menu_ui.open_menu_sfx.set_volume(first_sound_volume)
    menu_ui_save.select_sfx.set_volume(first_sound_volume)
    menu_ui_load.select_sfx.set_volume(first_sound_volume)
    menu_ui_inventory.select_sfx.set_volume(first_sound_volume)
    menu_ui_skills.select_sfx.set_volume(first_sound_volume)
    menu_ui_achievement.select_sfx.set_volume(first_sound_volume)
    return player, rpgmap, camera, debug_ui, \
        menu_ui, menu_ui_save, menu_ui_load, menu_ui_title, \
        menu_ui_settings, menu_ui_inventory, menu_ui_skills, \
        menu_ui_achievement

async def main():
    delta_time = DeltaTime()
    display = pg.Surface((g['game_size']))

    # load data
    db = json_loader(f"{full_path}game_data/db.json")
    pg.display.set_caption(db["main"]["main_title"])
    start_map = db["start_map"]
    player_start_pos = db["player_start_position"]

    clock = pg.time.Clock()

    pygame_event = PygameEvent(game_size=g['game_size'])

    debug_message = ''

    match g['game_mode']:
        case 'pc':
            """
            OpenGL Stuff; for better FPS, resizable game windows and
            for steam achievement overlay
            I don't know what any of these code do,
            I just copy it from dafluffypotato.
            https://dafluffypotato.itch.io/hue-flowing
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

            pg.display.set_icon(asset_loader('img', 'icon'))
            player, rpgmap, camera, debug_ui, menu_ui, menu_ui_save, menu_ui_load, \
            menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, \
           menu_ui_achievement = load_game(
                player_start_pos, start_map, db, screen, False)
            load_settings = json_loader(menu_ui_settings.settings_path)
            if load_settings['Fullscreen']:
                pg.display.toggle_fullscreen()

            opengl = OpenGLStuff()
            input = Input('pc')
            game_state = 1

            while pygame_event.running:
                display = run_game_loop(g, delta_time, clock, pygame_event, \
                    input, display, rpgmap, player, camera, debug_ui, \
                    debug_message, opengl, menu_ui, menu_ui_save, menu_ui_load, \
                    menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, \
                    menu_ui_achievement, screen)

        case 'android':

            screen = pg.display.set_mode((g['game_size']),
                pg.SCALED)
            try:
                from android.storage import app_storage_path
                from android.permissions import request_permissions, check_permission, Permission
                request_permissions(
                    [
                        Permission.READ_EXTERNAL_STORAGE,
                        Permission.WRITE_EXTERNAL_STORAGE
                    ]
                )
                pg.display.toggle_fullscreen()
            except:
                def app_storage_path():
                    return full_path

            player, rpgmap, camera, debug_ui, menu_ui, menu_ui_save, menu_ui_load, \
            menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, \
           menu_ui_achievement = load_game(
                player_start_pos, start_map, db, screen, app_storage_path())

            input = Input('android', g['game_size'], full_path)
            opengl = False

            while pygame_event.running:
                run_game_loop(
                    g, delta_time, clock, pygame_event, input, display,
                    rpgmap, player, camera, debug_ui, debug_message, opengl,
                    menu_ui, menu_ui_save, menu_ui_load, menu_ui_title,
                    menu_ui_settings, menu_ui_inventory, menu_ui_skills,
                    menu_ui_achievement, screen)

        case 'web':
            import sys, platform
            if sys.platform == "emscripten":
                platform.window.canvas.style.imageRendering = "pixelated"
            screen = pg.display.set_mode(
                (game_size_native),
                pg.RESIZABLE)
            player, rpgmap, camera, debug_ui, menu_ui, menu_ui_save, menu_ui_load, \
            menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, \
           menu_ui_achievement = load_game(
                player_start_pos, start_map, db, screen, False)

            input = Input('web')
            opengl = False

            while pygame_event.running:
                run_game_loop(g, delta_time, clock, pygame_event, input, display,
                    rpgmap, player, camera, debug_ui, debug_message, opengl,
                    menu_ui, menu_ui_save, menu_ui_load, menu_ui_title,
                    menu_ui_settings, menu_ui_inventory, menu_ui_skills, menu_ui_achievement,
                    screen)
                await asyncio.sleep(0)

    pg.quit()
    exit()

if __name__ == "__main__":
    asyncio.run(main())
