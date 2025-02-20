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

correct_path = True
if not os.path.exists(f"{full_path}/game_data/game_mode.txt") \
or not os.path.exists(f"{full_path}/game_data/db.json") \
or not os.path.exists(f"{full_path}/game_data/data/items.json") \
or not os.path.exists(f"{full_path}/game_data/data/skills.json") \
    or not os.path.exists(f"{full_path}/game_data/data/commands"):
    correct_path = False

if not correct_path:
    from src import PygameEvent, Timer, blit_text
    pygame_event = PygameEvent(game_size=[800, 400])
    display = pg.Surface((800, 400))
    exit_timer = Timer()
    exit_timer.start()
    error_font = pg.font.SysFont('', size=40)
    white = pg.Color('white')
    blue = pg.Color(53, 126, 199)
    screen = pg.display.set_mode(
        ((800, 400)))
    while pygame_event.running:
        display.fill(blue)
        message = ':( \n\nCan\'t find the necessary files to start the game.\n(You have to run executable inside its root folder.)'
        exit_countdown = exit_timer.get_elapsed_time()
        message += f'\n\nAutomatically exit in {5-int(exit_countdown)} ...'
        blit_text(display, message, error_font, white, (0, 0), 0, True)
        pg.display.flip()
        pg.transform.scale(display, screen.get_size(), screen)
        if exit_countdown > 5:
            pygame_event.running = False
    pg.quit()
    exit()

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
    Player, RpgMap, Camera, MusicPlayer, \
    Item, Skill, \
    Command, Conversation, PythonScript, \
    AddItem, RemoveItem, AddSkill, RemoveSkill, \
    GameInput, DeltaTime, PygameEvent, Timer, \
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
    player.equip_sfx = asset_loader('sfx', 'equip')
    player.unequip_sfx = asset_loader('sfx', 'unequip')
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
    menu_ui_title.bg = asset_loader('sprite', 'title_screen')
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

    pg.mixer.music.set_volume(first_music_volume)
    music_player = MusicPlayer()
    music_player.current_music = 'sonatina_letsadventure_1ATaleForTheJourney'
    music_player.update()

    menu_ui.select_sfx.set_volume(first_sound_volume)
    menu_ui.open_menu_sfx.set_volume(first_sound_volume)
    menu_ui_save.select_sfx.set_volume(first_sound_volume)
    menu_ui_load.select_sfx.set_volume(first_sound_volume)
    menu_ui_inventory.select_sfx.set_volume(first_sound_volume)
    menu_ui_skills.select_sfx.set_volume(first_sound_volume)
    menu_ui_achievement.select_sfx.set_volume(first_sound_volume)

    player.equip_sfx.set_volume(first_sound_volume)
    player.unequip_sfx.set_volume(first_sound_volume)

    item_data = json_loader(f'{full_path}game_data/data/items.json')
    item_dict = {}
    for item_name in item_data:
        data = item_data[item_name]

        item_dict[item_name] = Item(
            name=item_name,
            img=asset_loader('sprite', data['img']),
            description=data['description'],
            is_key_item=data['key_item'],
            is_equipable=data['equipable']
        )

    skill_data = json_loader(f'{full_path}game_data/data/skills.json')
    skill_dict = {}
    for skill_name in skill_data:
        data = skill_data[skill_name]

        skill_dict[skill_name] = Skill(
            name=skill_name,
            img=asset_loader('sprite', 'slash'),
            description=data['description'],
            attrs=data['attrs'],
        )

    player.skill_dict = skill_dict

    command_data = json_loader(f'{full_path}game_data/data/commands/{start_map}.json')
    command_list = []
    for command_name in command_data:
        data = command_data[command_name]

        sequence = []
        for sequence_data in data['sequence']:
            match sequence_data['type']:
                case 'python_script':
                    sequence.append(
                        PythonScript(sequence_data['script'])
                    )
                case 'conversation':
                    sequence.append(
                        Conversation(font_9, sequence_data['dialogs'])
                    )
                case 'add_item':
                    sequence.append(
                        AddItem(item_dict[sequence_data['item']], sequence_data['quant'])
                    )
                case 'remove_item':
                    sequence.append(
                        RemoveItem(item_dict[sequence_data['item']], sequence_data['quant'])
                    )
                case 'add_skill':
                    sequence.append(
                        AddSkill(skill_dict[sequence_data['skill']])
                    )
                case 'remove_skill':
                    sequence.append(
                        RemoveSkill(skill_dict[sequence_data['skill']])
                    )

        img = False
        if data['img']:
            img = asset_loader("sprite", data['img'])

        command_list.append(
            Command(
                name=command_name,
                trigger_by=data['trigger_by'],
                sequence=sequence,
                xy=data['position'],
                show=data['show'],
                img=img,
                has_collision=data['has_collision']
            )
        )

    return player, rpgmap, camera, debug_ui, \
        menu_ui, menu_ui_save, menu_ui_load, menu_ui_title, \
        menu_ui_settings, menu_ui_inventory, menu_ui_skills, \
        menu_ui_achievement, music_player, command_list, item_dict, skill_dict

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
           menu_ui_achievement, music_player, command_list, item_dict, skill_dict = load_game(
                player_start_pos, start_map, db, screen, False)
            load_settings = json_loader(menu_ui_settings.settings_path)
            if load_settings['Fullscreen']:
                pg.display.toggle_fullscreen()

            opengl = OpenGLStuff()
            game_input = GameInput('pc')
            game_state = 1

            while pygame_event.running:
                display = run_game_loop(g, delta_time, clock, pygame_event, \
                    game_input, display, rpgmap, player, camera, debug_ui, \
                    debug_message, opengl, menu_ui, menu_ui_save, menu_ui_load, \
                    menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, \
                    menu_ui_achievement, screen, music_player, command_list, item_dict, skill_dict)

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
           menu_ui_achievement, music_player, command_list, item_dict, skill_dict = load_game(
                player_start_pos, start_map, db, screen, app_storage_path())

            game_input = GameInput('android', g['game_size'], full_path)
            opengl = False

            while pygame_event.running:
                run_game_loop(
                    g, delta_time, clock, pygame_event, game_input, display,
                    rpgmap, player, camera, debug_ui, debug_message, opengl,
                    menu_ui, menu_ui_save, menu_ui_load, menu_ui_title,
                    menu_ui_settings, menu_ui_inventory, menu_ui_skills,
                    menu_ui_achievement, screen, music_player, command_list, item_dict, skill_dict)

        case 'web':
            import sys, platform
            if sys.platform == "emscripten":
                platform.window.canvas.style.imageRendering = "pixelated"
            screen = pg.display.set_mode(
                (game_size_native),
                pg.RESIZABLE)
            player, rpgmap, camera, debug_ui, menu_ui, menu_ui_save, menu_ui_load, \
            menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, \
           menu_ui_achievement, music_player, command_list, item_dict, skill_dict = load_game(
                player_start_pos, start_map, db, screen, False)

            game_input = GameInput('web')
            opengl = False

            while pygame_event.running:
                run_game_loop(g, delta_time, clock, pygame_event, game_input, display,
                    rpgmap, player, camera, debug_ui, debug_message, opengl,
                    menu_ui, menu_ui_save, menu_ui_load, menu_ui_title,
                    menu_ui_settings, menu_ui_inventory, menu_ui_skills, menu_ui_achievement,
                    screen, music_player, command_list, item_dict, skill_dict)
                await asyncio.sleep(0)

    pg.quit()
    exit()

if __name__ == "__main__":
    asyncio.run(main())
