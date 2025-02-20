from .ui import blit_text, blit_img, filter_effect
import pygame as pg
from .utils import asset_loader
from .state import title_screen_update, reset_title_screen, load_game_update, settings_update, main_game_update, pause_game_update, save_load_game_update, inventory_update, skill_update,achievement_update, reset_menu

def run_game_loop(g, delta_time, clock, pygame_event, game_input, display, rpgmap, player, camera, debug_ui, debug_message, opengl, menu_ui, menu_ui_save, menu_ui_load, menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, screen, music_player, command_list, item_dict, skill_dict):
    platform = g['game_mode']
    dt = delta_time.get()

    if pygame_event.game_state == 3 or pygame_event.game_state == -4:
        clock.tick(60)
    else:
        clock.tick(menu_ui_settings.cap_fps)
    current_time = pg.time.get_ticks()
    display.fill(g['colors']['grey'])

    # Input
    new_size = False
    mobile_key, key = False, False
    match platform:
        case 'pc':
            new_size, key, display = game_input.update_for_pc(pygame_event, display)
            rpgmap.resize_view(new_size)
        case 'android':
            mobile_key = game_input.update_for_android(pygame_event)
        case 'web':
            key = game_input.update_for_web(pygame_event)
        case _:
            raise Exception(f"Unknown platform: {platform}")

    match pygame_event.game_state:
        case -1:
            title_screen_update(menu_ui_title, display, dt, current_time, platform, key, game_input, mobile_key, player, pygame_event, menu_ui, menu_ui_save, menu_ui_load, menu_ui_settings, command_list)

        case -2:
            reset_title_screen(menu_ui_title, display, pygame_event)

        case -3:
            load_game_update(new_size, menu_ui, menu_ui_load, menu_ui_save, display, dt, current_time, key, game_input, platform, mobile_key, player, rpgmap, pygame_event)

        case -4:
            settings_update(-2, menu_ui_settings, menu_ui, menu_ui_save, menu_ui_load, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, player, new_size, display, dt, current_time, platform, key, mobile_key, game_input, pygame_event)

        case _:
            if not platform == 'android':
                for joystick in game_input.joysticks:
                    if joystick.get_button(10):
                        pygame_event.game_state = 1

            center_x = display.get_width()//2
            center_y = display.get_height()//2
            player.collision = pg.Rect(center_x-16, center_y-2, 16, 16)

            # Graphic
            collision_rects = []
            draw_count = rpgmap.draw(display, camera, player.rect, layers=['layer1', 'layer2'], get_collision=False)
            for command in command_list:
                collision = command.draw(display, player, rpgmap, camera)
                if collision:
                    collision_rects.append(collision)
            collision_rects += rpgmap.draw(display, camera, player.rect, layers=['layer3'], get_collision=True)
            # pg.draw.rect(display, g['colors']['green'], player.collision) # player collision box
            blit_img(display, player.img, (center_x-16, center_y-18))
            draw_count += rpgmap.draw(display, camera, player.rect, layers=['layer4'], get_collision=False)

            # Logic

            game_pause = False
            if pygame_event.game_state >= 0:
                for command in command_list:
                    match platform:
                        case 'android':
                            command.update_for_android(display, dt, current_time, mobile_key, player, rpgmap, camera, item_dict, pygame_event.game_state)
                        case _:
                            command.update_for_pc(display, dt, current_time, key, game_input.joysticks, player, rpgmap, camera, item_dict, pygame_event.game_state)

                    if command.has_triggered and not command.finish:
                        game_pause = True

            if pygame_event.game_state == 0:
                main_game_update(platform, game_pause, player, key, mobile_key, game_input, dt, collision_rects, camera, menu_ui, menu_ui_save, menu_ui_load, menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, display)

            elif pygame_event.game_state > 1:
                filter_effect(display, 'darken')
                # filter_effect(display, 'blur')

            match pygame_event.game_state:
                case 1:
                    if not game_pause:
                        pause_game_update(display, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, menu_ui, new_size, dt, current_time, platform, key, mobile_key, game_input, pygame_event, menu_ui_save, menu_ui_load)
                    else:
                        pygame_event.game_state = 0
                case 2:
                    save_load_game_update(pygame_event, new_size, menu_ui_save, display, dt, current_time, platform, key, mobile_key, game_input, player, rpgmap, menu_ui_load, menu_ui)

                case 3:
                    settings_update(1, menu_ui_settings, menu_ui, menu_ui_save, menu_ui_load, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, player, new_size, display, dt, current_time, platform, key, mobile_key, game_input, pygame_event)

                case 4:
                    inventory_update(new_size, menu_ui_inventory, display, dt, current_time, platform, key, mobile_key, game_input, player, item_dict, menu_ui, pygame_event)

                case 5:
                    skill_update(new_size, menu_ui_skills, display, dt, current_time, platform, key, game_input, player, mobile_key, pygame_event, menu_ui, skill_dict)
                case 6:
                    achievement_update(new_size, menu_ui_achievement, display, dt, current_time, key, game_input, mobile_key, platform, menu_ui, pygame_event)

            pg.draw.line(display, g['colors']['black'], (0,0), (0,display.get_size()[1]))
            pg.draw.line(display, g['colors']['black'], (display.get_size()[0]-1,0), (display.get_size()[0]-1,display.get_size()[1]))

    # Debug
    if menu_ui_settings.debug:
        debug_message = ""
        try:
            debug_message = f"state: {pygame_event.game_state}"
        except Exception as e:
            debug_message = f"{e}"
        blit_text(display, f"{debug_message}", g['font']['font_9'], g['colors']['black'], (5, 5))
        debug_ui.draw_fps(display, clock)

    match pygame_event.game_state:
        case -1:
            music_player.current_music = 'sonatina_letsadventure_1ATaleForTheJourney'
        case 0:
            music_player.current_music = 'sonatina_letsadventure_4IslandScenery'
    music_player.update()

    match platform:
        case 'pc':
            # Use OpenGL
            opengl.draw(display)
            return display

        case 'android':
            game_input.draw_for_android(display)
            pg.transform.scale(display, screen.get_size(), screen)
            pg.display.flip()

        case 'web':
            pg.transform.scale(display, screen.get_size(), screen)
            pg.display.flip()
