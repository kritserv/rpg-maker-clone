from .ui import blit_text
import pygame as pg
from .state import title_screen_update, reset_title_screen, load_game_update, settings_update, main_game_update, pause_game_update, save_load_game_update, inventory_update, skill_update,achievement_update, reset_menu

def run_game_loop(g, delta_time, clock, pygame_event, input, display, rpgmap, player, camera, debug_ui, debug_message, opengl, menu_ui, menu_ui_save, menu_ui_load, menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, screen):
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
            new_size, key, display = input.update_for_pc(pygame_event, display)
            rpgmap.resize_view(new_size)
        case 'android':
            mobile_key = input.update_for_android(pygame_event)
        case 'web':
            key = input.update_for_web(pygame_event)
        case _:
            raise Exception(f"Unknown platform: {platform}")

    match pygame_event.game_state:
        case -1:
            title_screen_update(menu_ui_title, display, dt, current_time, platform, key, input, mobile_key, player, pygame_event, menu_ui, menu_ui_save, menu_ui_load, menu_ui_settings)

        case -2:
            reset_title_screen(menu_ui_title, display, pygame_event)

        case -3:
            load_game_update(new_size, menu_ui, menu_ui_load, menu_ui_save, display, dt, current_time, key, input, platform, mobile_key, player, rpgmap, pygame_event)

        case -4:
            settings_update(-2, menu_ui_settings, menu_ui, menu_ui_save, menu_ui_load, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, new_size, display, dt, current_time, platform, key, mobile_key, input, pygame_event)

        case _:
            if not platform == 'android':
                for joystick in input.joysticks:
                    if joystick.get_button(10):
                        pygame_event.game_state = 1

            center_x = display.get_size()[0]//2
            center_y = display.get_size()[1]//2
            player.collision = pg.Rect(center_x-16, center_y-2, 16, 16)

            # Graphic
            draw_count = rpgmap.draw(display, camera, player.rect, layers=['layer1', 'layer2'], get_collision=False)
            collision_rects = rpgmap.draw(display, camera, player.rect, layers=['layer3'], get_collision=True)
            # pg.draw.rect(display, g['colors']['green'], player.collision) # player collision box
            display.blit(player.img, [center_x-16, center_y-18])
            draw_count += rpgmap.draw(display, camera, player.rect, layers=['layer4'], get_collision=False)

            # Logic
            if pygame_event.game_state == 0:
                main_game_update(platform, player, key, mobile_key, input, dt, collision_rects, camera, menu_ui, menu_ui_save, menu_ui_load, menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, display)

            match pygame_event.game_state:
                case 1:
                    pause_game_update(display, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, menu_ui, new_size, dt, current_time, platform, key, mobile_key, input, pygame_event, menu_ui_save, menu_ui_load)

                case 2:
                    save_load_game_update(pygame_event, new_size, menu_ui_save, display, dt, current_time, platform, key, mobile_key, input, player, rpgmap, menu_ui_load, menu_ui)

                case 3:
                    settings_update(1, menu_ui_settings, menu_ui, menu_ui_save, menu_ui_load, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, new_size, display, dt, current_time, platform, key, mobile_key, input, pygame_event)

                case 4:
                    inventory_update(new_size, menu_ui_inventory, display, dt, current_time, platform, key, mobile_key, input, menu_ui, pygame_event)

                case 5:
                    skill_update(new_size, menu_ui_skills, display, dt, current_time, platform, key, input, mobile_key, pygame_event, menu_ui)
                case 6:
                    achievement_update(new_size, menu_ui_achievement, display, dt, current_time, key, input, mobile_key, platform, menu_ui, pygame_event)

            pg.draw.line(display, g['colors']['black'], (0,0), (0,display.get_size()[1]))
            pg.draw.line(display, g['colors']['black'], (display.get_size()[0]-1,0), (display.get_size()[0]-1,display.get_size()[1]))

    if menu_ui_settings.debug:
        # Debug
        debug_message = ""
        try:
            debug_message = f"inven: {player.items}"
        except Exception as e:
            debug_message = f"{e}"
        blit_text(display, f"{debug_message}", g['font']['font_9'], g['colors']['black'], (5, 5))
        debug_ui.draw_fps(display, clock)

    match platform:
        case 'pc':
            # Use OpenGL
            opengl.draw(display)
            return display

        case 'android':
            input.draw_for_android(display)
            pg.transform.scale(display, screen.get_size(), screen)
            pg.display.flip()

        case 'web':
            pg.transform.scale(display, screen.get_size(), screen)
            pg.display.flip()
