from moderngl import Error
from .blit_text import blit_text
import pygame as pg

def reset_menu(menu, display, cursor = 0):
    menu.cursor = cursor
    menu.menu_x = display.get_size()[0]
    menu.speed = 450
    menu.animate_in = True

def run_game_loop(g, delta_time, clock, pygame_event, input, display, rpgmap, player, camera, top_ui, debug_message, opengl, menu_ui, menu_ui_save, menu_ui_load, menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, screen):
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
            slide_in = menu_ui_title.draw(display, dt, current_time)
            select_submenu = False
            if not slide_in:
                match platform:
                    case 'pc':
                        select_submenu = menu_ui_title.update_for_pc(key, input.joysticks, dt, current_time)
                    case 'android':
                        select_submenu = menu_ui_title.update_for_android(mobile_key, [], dt, current_time)
                    case 'web':
                        select_submenu = menu_ui_title.update_for_pc(key, input.joysticks, dt, current_time)

                match select_submenu:
                    case 'New Game':
                        player.start_new_game()
                        pygame_event.game_state = 0
                    case 'Continue':
                        reset_menu(menu_ui_load, display)
                        pygame_event.game_state = -3
                    case 'Setting':
                        pygame_event.game_state = -4
                    case 'Quit':
                        pygame_event.running = False
                    case _:
                        pass
            reset_menu(menu_ui, display)
            reset_menu(menu_ui_save, display)
            reset_menu(menu_ui_load, display)
            reset_menu(menu_ui_settings, display)

        case -2:
            menu_ui_title.speed = 20
            menu_ui_title.menu_y = display.get_size()[1]
            pygame_event.game_state = -1

        case -3:
            select_submenu = False
            if new_size:
                reset_menu(menu_ui_load, display, cursor = menu_ui_load.cursor)
            slide_in = menu_ui_load.draw(display, dt, current_time)
            if not slide_in:
                match platform:
                    case 'pc':
                        select_submenu = menu_ui_load.update_for_pc(key, input.joysticks, dt, current_time, player, rpgmap)
                    case 'android':
                        select_submenu = menu_ui_load.update_for_android(mobile_key, [], dt, current_time, player, rpgmap)
                    case 'web':
                        select_submenu = menu_ui_load.update_for_pc(key, input.joysticks, dt, current_time, player, rpgmap)
            if select_submenu:
                match select_submenu:
                    case 'Back':
                        pygame_event.game_state = -1
                        if pygame_event.is_save_state:
                            reset_menu(menu_ui, display, 3)
                            pygame_event.is_save_state = False
                        elif pygame_event.is_load_state:
                            reset_menu(menu_ui, display, 4)
                            pygame_event.is_load_state = False
                    case _:
                        menu_ui_load.menu = menu_ui_save.menu
                        pygame_event.game_state = 0
                        pygame_event.is_save_state = False
                        pygame_event.is_load_state = False

        case -4:
            new_sound_volume = menu_ui_settings.sound_slider.save_value/100
            menu_ui.select_sfx.set_volume(new_sound_volume)
            menu_ui.open_menu_sfx.set_volume(new_sound_volume)
            menu_ui_save.select_sfx.set_volume(new_sound_volume)
            menu_ui_load.select_sfx.set_volume(new_sound_volume)
            menu_ui_inventory.select_sfx.set_volume(new_sound_volume)
            menu_ui_skills.select_sfx.set_volume(new_sound_volume)
            menu_ui_achievement.select_sfx.set_volume(new_sound_volume)
            select_submenu = False
            if new_size:
                reset_menu(menu_ui_settings, display, cursor = menu_ui_settings.cursor)
            slide_in = menu_ui_settings.draw(display, dt, current_time)
            if not slide_in:
                match platform:
                    case 'pc':
                        select_submenu = menu_ui_settings.update_for_pc(key, input.joysticks, dt, current_time, input)
                    case 'android':
                        select_submenu = menu_ui_settings.update_for_android(mobile_key, [], dt, current_time, input)
                    case 'web':
                        select_submenu = menu_ui_settings.update_for_pc(key, input.joysticks, dt, current_time, input)
            if select_submenu:
                match select_submenu:
                    case 'Back':
                        pygame_event.game_state = -2

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
                match platform:
                    case 'pc':
                        player.update(key, dt, joysticks=input.joysticks, collision_rects=collision_rects)
                    case 'android':
                        player.update(key=None, dt=dt, mobile_key=mobile_key, joysticks=[], collision_rects=collision_rects)
                    case 'web':
                        player.update(key, dt, joysticks=input.joysticks, collision_rects=collision_rects)

                camera.update(player)
                reset_menu(menu_ui, display)
                reset_menu(menu_ui_save, display)
                reset_menu(menu_ui_load, display)
                reset_menu(menu_ui_title, display)
                reset_menu(menu_ui_settings, display)
                reset_menu(menu_ui_inventory, display)
                reset_menu(menu_ui_skills, display)
                reset_menu(menu_ui_achievement, display)
                menu_ui.is_open = False

            match pygame_event.game_state:
                case 1:
                    reset_meny_y_pos = display.get_size()[1]
                    menu_ui_inventory.menu_y = reset_meny_y_pos
                    menu_ui_skills.menu_y = reset_meny_y_pos
                    menu_ui_achievement.menu_y = reset_meny_y_pos
                    if menu_ui.is_open == False:
                        menu_ui.is_open = True
                        menu_ui.open_menu_sfx.play()
                    if new_size:
                        reset_menu(menu_ui, display, cursor = menu_ui.cursor)
                    select_submenu = False
                    slide_in = menu_ui.draw(display, dt, current_time)
                    if not slide_in:
                        match platform:
                            case 'pc':
                                select_submenu = menu_ui.update_for_pc(key, input.joysticks, dt, current_time)
                            case 'android':
                                select_submenu = menu_ui.update_for_android(mobile_key, [], dt, current_time)
                            case 'web':
                                select_submenu = menu_ui.update_for_pc(key, input.joysticks, dt, current_time)
                    if select_submenu:
                        match select_submenu:

                            case 'Inventory':
                                pygame_event.game_state = 4
                                reset_menu(menu_ui_inventory, display)

                            case 'Skills':
                                pygame_event.game_state = 5
                                reset_menu(menu_ui_skills, display)

                            case 'Achievement':
                                pygame_event.game_state = 6
                                reset_menu(menu_ui_skills, display)

                            case 'Save':
                                pygame_event.game_state = 2
                                pygame_event.is_save_state = True
                                pygame_event.is_load_state = False
                                reset_menu(menu_ui_save, display)
                                reset_menu(menu_ui_load, display)

                            case 'Load':
                                pygame_event.game_state = 2
                                pygame_event.is_load_state = True
                                pygame_event.is_save_state = False
                                reset_menu(menu_ui_save, display)
                                reset_menu(menu_ui_load, display)

                            case 'Setting':
                                pygame_event.game_state = 3
                                pygame_event.is_save_state = False
                                pygame_event.is_load_state = False

                            case 'Back':
                                pygame_event.game_state -= 1
                                pygame_event.is_save_state = False
                                pygame_event.is_load_state = False

                            case 'Exit to title':
                                pygame_event.game_state = -2

                            case _:
                                pass

                case 2:
                    select_submenu = False
                    if pygame_event.is_save_state:
                        if new_size:
                            reset_menu(menu_ui_save, display, cursor = menu_ui_save.cursor)
                        slide_in = menu_ui_save.draw(display, dt, current_time)
                        if not slide_in:
                            match platform:
                                case 'pc':
                                    select_submenu = menu_ui_save.update_for_pc(key, input.joysticks, dt, current_time, player, rpgmap)
                                case 'android':
                                    select_submenu = menu_ui_save.update_for_android(mobile_key, [], dt, current_time, player, rpgmap)
                                case 'web':
                                    select_submenu = menu_ui_save.update_for_pc(key, input.joysticks, dt, current_time, player, rpgmap)
                    elif pygame_event.is_load_state:
                        if new_size:
                            reset_menu(menu_ui_load, display, cursor = menu_ui_load.cursor)
                        slide_in = menu_ui_load.draw(display, dt, current_time)
                        if not slide_in:
                            match platform:
                                case 'pc':
                                    select_submenu = menu_ui_load.update_for_pc(key, input.joysticks, dt, current_time, player, rpgmap)
                                case 'android':
                                    select_submenu = menu_ui_load.update_for_android(mobile_key, [], dt, current_time, player, rpgmap)
                                case 'web':
                                    select_submenu = menu_ui_load.update_for_pc(key, input.joysticks, dt, current_time, player, rpgmap)
                    if select_submenu:
                        match select_submenu:
                            case 'Back':
                                pygame_event.game_state -= 1
                                if pygame_event.is_save_state:
                                    reset_menu(menu_ui, display, 3)
                                    pygame_event.is_save_state = False
                                elif pygame_event.is_load_state:
                                    reset_menu(menu_ui, display, 4)
                                    pygame_event.is_load_state = False
                            case _:
                                menu_ui_load.menu = menu_ui_save.menu
                                pygame_event.game_state = 0
                                pygame_event.is_save_state = False
                                pygame_event.is_load_state = False

                case 3:
                    new_sound_volume = menu_ui_settings.sound_slider.save_value/100
                    menu_ui.select_sfx.set_volume(new_sound_volume)
                    menu_ui.open_menu_sfx.set_volume(new_sound_volume)
                    menu_ui_save.select_sfx.set_volume(new_sound_volume)
                    menu_ui_load.select_sfx.set_volume(new_sound_volume)
                    menu_ui_inventory.select_sfx.set_volume(new_sound_volume)
                    menu_ui_skills.select_sfx.set_volume(new_sound_volume)
                    menu_ui_achievement.select_sfx.set_volume(new_sound_volume)
                    select_submenu = False
                    if new_size:
                        reset_menu(menu_ui_settings, display, cursor = menu_ui_settings.cursor)
                    slide_in = menu_ui_settings.draw(display, dt, current_time)
                    if not slide_in:
                        match platform:
                            case 'pc':
                                select_submenu = menu_ui_settings.update_for_pc(key, input.joysticks, dt, current_time, input)
                            case 'android':
                                select_submenu = menu_ui_settings.update_for_android(mobile_key, [], dt, current_time, input)
                            case 'web':
                                select_submenu = menu_ui_settings.update_for_pc(key, input.joysticks, dt, current_time, input)
                    if select_submenu:
                        match select_submenu:
                            case 'Back':
                                reset_menu(menu_ui_settings, display)
                                reset_menu(menu_ui, display, 5)
                                pygame_event.game_state = 1

                case 4:
                    select_submenu = False
                    if new_size:
                        reset_menu(menu_ui_inventory, display, cursor = menu_ui_inventory.cursor)
                    slide_in = menu_ui_inventory.draw(display, dt, current_time)
                    if not slide_in:
                        match platform:
                            case 'pc':
                                select_submenu = menu_ui_inventory.update_for_pc(key, input.joysticks, dt, current_time, input)
                            case 'android':
                                select_submenu = menu_ui_inventory.update_for_android(mobile_key, [], dt, current_time, input)
                            case 'web':
                                select_submenu = menu_ui_inventory.update_for_pc(key, input.joysticks, dt, current_time, input)
                    if select_submenu:
                        match select_submenu:
                            case 'Back':
                                reset_menu(menu_ui_inventory, display)
                                reset_menu(menu_ui, display, 0)
                                pygame_event.game_state = 1
                case 5:
                    select_submenu = False
                    if new_size:
                        reset_menu(menu_ui_skills, display, cursor = menu_ui_skills.cursor)
                    slide_in = menu_ui_skills.draw(display, dt, current_time)
                    if not slide_in:
                        match platform:
                            case 'pc':
                                select_submenu = menu_ui_skills.update_for_pc(key, input.joysticks, dt, current_time, input)
                            case 'android':
                                select_submenu = menu_ui_skills.update_for_android(mobile_key, [], dt, current_time, input)
                            case 'web':
                                select_submenu = menu_ui_skills.update_for_pc(key, input.joysticks, dt, current_time, input)
                    if select_submenu:
                        match select_submenu:
                            case 'Back':
                                reset_menu(menu_ui_skills, display)
                                reset_menu(menu_ui, display, 1)
                                pygame_event.game_state = 1
                case 6:
                    select_submenu = False
                    if new_size:
                        reset_menu(menu_ui_achievement, display, cursor = menu_ui_achievement.cursor)
                    slide_in = menu_ui_achievement.draw(display, dt, current_time)
                    if not slide_in:
                        match platform:
                            case 'pc':
                                select_submenu = menu_ui_achievement.update_for_pc(key, input.joysticks, dt, current_time, input)
                            case 'android':
                                select_submenu = menu_ui_achievement.update_for_android(mobile_key, [], dt, current_time, input)
                            case 'web':
                                select_submenu = menu_ui_achievement.update_for_pc(key, input.joysticks, dt, current_time, input)
                    if select_submenu:
                        match select_submenu:
                            case 'Back':
                                reset_menu(menu_ui_achievement, display)
                                reset_menu(menu_ui, display, 2)
                                pygame_event.game_state = 1

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
        top_ui.draw_fps(display, clock)

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
