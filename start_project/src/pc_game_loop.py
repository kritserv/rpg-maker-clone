from .blit_text import blit_text
import pygame as pg

def reset_menu(menu, display, cursor = 0):
    menu.cursor = cursor
    menu.menu_x = display.get_size()[0]
    menu.speed = 450
    menu.animate_in = True

def run_pc_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, BLACK, top_ui, debug_message, debug_font, opengl, menu_ui, menu_ui_save, menu_ui_load, menu_ui_title):
    dt = delta_time.get()
    clock.tick()
    current_time = pg.time.get_ticks()
    display.fill(GREY)

    # Input
    new_size, key, display = input.update_for_pc(pygame_event, display)
    rpgmap.resize_view(new_size)

    match pygame_event.game_state:
        case -1:
            slide_in = menu_ui_title.draw(display, dt, current_time)
            select_submenu = False
            if not slide_in:
                select_submenu = menu_ui_title.update_for_pc(key, input.joysticks, dt, current_time)
                match select_submenu:
                    case 'New Game':
                        player.start_new_game()
                        pygame_event.game_state = 0
                    case 'Continue':
                        reset_menu(menu_ui_load, display)
                        pygame_event.game_state = -3
                    case 'Quit':
                        pygame_event.running = False
                    case _:
                        pass
            reset_menu(menu_ui, display)
            reset_menu(menu_ui_save, display)
            reset_menu(menu_ui_load, display)

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

        case _:

            for joystick in input.joysticks:
                if joystick.get_button(10):
                    pygame_event.game_state = 1

            center_x = display.get_size()[0]//2
            center_y = display.get_size()[1]//2

            # Graphic
            draw_count = rpgmap.draw(display, camera, player.rect, layers=['layer1', 'layer2'], get_collision=False)
            collision_rects = rpgmap.draw(display, camera, player.rect, layers=['layer3'], get_collision=True)

            player.collision = pg.Rect(center_x-16, center_y-2, 16, 16)
            # pg.draw.rect(display, pg.Color('green'), player.collision) # player collision box

            display.blit(player.img, [display.get_size()[0]//2-16, display.get_size()[1]//2+-18])
            draw_count = rpgmap.draw(display, camera, player.rect, layers=['layer4'], get_collision=False)

            # Logic

            if pygame_event.game_state == 0:
                player.update(key, dt, joysticks=input.joysticks, collision_rects=collision_rects)
                camera.update(player)
                reset_menu(menu_ui, display)
                reset_menu(menu_ui_save, display)
                reset_menu(menu_ui_load, display)
                reset_menu(menu_ui_title, display)
                menu_ui.is_open = False

            match pygame_event.game_state:
                case 1:
                    if menu_ui.is_open == False:
                        menu_ui.is_open = True
                        menu_ui.open_menu_sfx.play()
                    if new_size:
                        reset_menu(menu_ui, display, cursor = menu_ui.cursor)
                    select_submenu = False
                    slide_in = menu_ui.draw(display, dt, current_time)
                    if not slide_in:
                        select_submenu = menu_ui.update_for_pc(key, input.joysticks, dt, current_time)
                    if select_submenu:
                        match select_submenu:
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
                            select_submenu = menu_ui_save.update_for_pc(key, input.joysticks, dt, current_time, player, rpgmap)
                    elif pygame_event.is_load_state:
                        if new_size:
                            reset_menu(menu_ui_load, display, cursor = menu_ui_load.cursor)
                        slide_in = menu_ui_load.draw(display, dt, current_time)
                        if not slide_in:
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


            # Debug
            debug_message = f"rem {len(player.remembered_obstacle_pos)}"
            blit_text(display, f"{debug_message}", debug_font, BLACK, (5, 5))
            debug_message = f"pos {player.pos}"
            blit_text(display, f"{debug_message}", debug_font, BLACK, (5, 17)) #pg.Surface((16, 16))
            pg.draw.line(display, BLACK, (0,0), (0,display.get_size()[1]))
            pg.draw.line(display, BLACK, (display.get_size()[0]-1,0), (display.get_size()[0]-1,display.get_size()[1]))
    top_ui.draw_fps(display, clock)

    # Use OpenGL
    opengl.draw(display)
    return display
