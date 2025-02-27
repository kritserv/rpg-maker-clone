from .ui import blit_text, blit_img, filter_effect, Alert
import pygame as pg
from .utils import asset_loader
from .state import title_screen_update, reset_title_screen, load_game_update, settings_update, main_game_update, pause_game_update, save_load_game_update, inventory_update, skill_update,achievement_update, turn_based_update, reset_menu

def run_game_loop(g, delta_time, clock, pygame_event, game_input, display, rpgmap, player, camera, debug_ui, debug_message, opengl, menu_ui, menu_ui_save, menu_ui_load, menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, menu_ui_turn_based, alert, screen, music_player, command_list, item_dict, skill_dict, enemy_dict):
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
            title_screen_update(menu_ui_title, display, dt, current_time, platform, key, game_input, mobile_key, player, rpgmap, pygame_event, menu_ui, menu_ui_save, menu_ui_load, menu_ui_settings, command_list, enemy_dict)

        case -2:
            reset_title_screen(menu_ui_title, display, pygame_event)

        case -3:
            load_game_update(new_size, menu_ui, menu_ui_load, menu_ui_save, display, dt, current_time, key, game_input, platform, mobile_key, player, rpgmap, pygame_event, command_list, enemy_dict)

        case -4:
            settings_update(-2, menu_ui_settings, menu_ui, menu_ui_save, menu_ui_load, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, menu_ui_turn_based, player, new_size, display, dt, current_time, platform, key, mobile_key, game_input, pygame_event)

        case _:
            if not platform == 'android':
                for joystick in game_input.joysticks:
                    if joystick.get_button(10):
                        pygame_event.game_state = 1

            center_x = display.get_width()//2
            center_y = display.get_height()//2
            player.collision = pg.Rect(center_x-16, center_y-2, 16, 15)

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
                            command.update_for_android(display, dt, current_time, pygame_event, mobile_key, player, rpgmap, camera, item_dict, pygame_event.game_state, menu_ui_turn_based, command_list)
                        case _:
                            command.update_for_pc(display, dt, current_time, pygame_event, key, game_input.joysticks, player, rpgmap, camera, item_dict, pygame_event.game_state, menu_ui_turn_based, command_list)

                    if command.has_triggered and not command.finish:
                        game_pause = True

            if pygame_event.game_state == 0:
                main_game_update(platform, game_pause, player, key, mobile_key, game_input, dt, collision_rects, camera, menu_ui, menu_ui_save, menu_ui_load, menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, display)

            elif 7 > pygame_event.game_state > 1:
                filter_effect(display, 'darken')
                filter_effect(display, 'blur')

            player_ui_x = display.get_width()-55
            pg.draw.rect(display, pg.Color('black'), (player_ui_x, 9, 50, 9))
            player_hp = player.hp/player.max_hp
            if 0.4 > player_hp >= 0:
                pg.draw.rect(display, pg.Color('red'), (player_ui_x, 9, int(player.hp/player.max_hp*50), 9))
                blit_text(display, f'HP: {player.hp}', menu_ui_turn_based.menu_font, pg.Color('darkred'), (player_ui_x+5, 10))
            elif 0.7 > player_hp >= 0.4:
                pg.draw.rect(display, pg.Color('yellow'), (player_ui_x, 9, int(player.hp/player.max_hp*50), 9))
                blit_text(display, f'HP: {player.hp}', menu_ui_turn_based.menu_font, pg.Color('orange'), (player_ui_x+5, 10))
            else:
                pg.draw.rect(display, pg.Color('green'), (player_ui_x, 9, int(player.hp/player.max_hp*50), 9))
                blit_text(display, f'HP: {player.hp}', menu_ui_turn_based.menu_font, pg.Color('darkgreen'), (player_ui_x+5, 10))

            pg.draw.rect(display, pg.Color('black'), (player_ui_x, 20, 50, 9))
            pg.draw.rect(display, pg.Color('white'), (player_ui_x, 20, int(player.xp/100*50), 9))
            blit_text(display, f'LV: {player.levels}', menu_ui_turn_based.menu_font, pg.Color('grey20'), (player_ui_x+5, 21))

            match pygame_event.game_state:
                case 1:
                    if not game_pause:
                        pause_game_update(display, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, menu_ui, new_size, dt, current_time, platform, key, mobile_key, game_input, pygame_event, menu_ui_save, menu_ui_load)
                    else:
                        pygame_event.game_state = 0
                case 2:
                    save_load_game_update(pygame_event, new_size, menu_ui_save, display, dt, current_time, platform, key, mobile_key, game_input, player, rpgmap, menu_ui_load, menu_ui, command_list, enemy_dict)

                case 3:
                    settings_update(1, menu_ui_settings, menu_ui, menu_ui_save, menu_ui_load, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, menu_ui_turn_based, player, new_size, display, dt, current_time, platform, key, mobile_key, game_input, pygame_event)

                case 4:
                    inventory_update(new_size, menu_ui_inventory, display, dt, current_time, platform, key, mobile_key, game_input, player, item_dict, menu_ui, pygame_event)

                case 5:
                    skill_update(new_size, menu_ui_skills, display, dt, current_time, platform, key, game_input, player, mobile_key, pygame_event, menu_ui, skill_dict)
                case 6:
                    achievement_update(new_size, menu_ui_achievement, display, dt, player, current_time, key, game_input, mobile_key, platform, menu_ui, pygame_event)
                case 7:
                    turn_based_update(new_size, display, dt, current_time, key, game_input, mobile_key, player, rpgmap, platform, menu_ui, pygame_event, menu_ui_turn_based, item_dict, enemy_dict)

            pg.draw.line(display, g['colors']['black'], (0,0), (0,display.get_size()[1]))
            pg.draw.line(display, g['colors']['black'], (display.get_size()[0]-1,0), (display.get_size()[0]-1,display.get_size()[1]))

    # Debug
    if menu_ui_settings.debug:
        debug_ui.draw(display, clock, pygame_event, player, rpgmap)

    # Alert
    if player.alert:
        alert.menu = player.alert
        player.alert = False
    alert.draw(display, dt, current_time)

    match pygame_event.game_state:
        case -1:
            music_player.current_music = 'titlescreen'
        case 0:
            music_player.current_music = 'forest'
        case 7:
            music_player.current_music = 'battle'
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
