from .blit_text import blit_text
import pygame as pg

def reset_menu(menu, cursor = 0):
    menu.cursor = cursor
    menu.menu_x = 0
    menu.speed = 450
    menu.animate_in = True

def run_android_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, top_ui, menu_ui, menu_ui_save, menu_ui_load, screen):
    dt = delta_time.get()
    clock.tick()

    # Input
    mobile_key = input.update_for_android(pygame_event)

    # Logic
    if pygame_event.game_state == 0:
        player.update(key=None, dt=dt, mobile_key=mobile_key)
        camera.update(player)
        reset_menu(menu_ui)
        reset_menu(menu_ui_save)
        reset_menu(menu_ui_load)

    # Graphic
    display.fill(GREY)
    rpgmap.draw_scaled_screen(display, camera, player.rect)
    display.blit(player.img, [display.get_size()[0]//2-16, display.get_size()[1]//2+-22])

    current_time = pg.time.get_ticks()
    if pygame_event.game_state == 1:
        select_submenu = menu_ui.update_for_android(mobile_key, dt, current_time)
        if select_submenu:
            if select_submenu == 'Save':
                pygame_event.game_state = 2
                pygame_event.is_save_state = True
                pygame_event.is_load_state = False
                reset_menu(menu_ui_save)
                reset_menu(menu_ui_load)

            elif select_submenu == 'Load':
                pygame_event.game_state = 2
                pygame_event.is_load_state = True
                pygame_event.is_save_state = False
                reset_menu(menu_ui_save)
                reset_menu(menu_ui_load)

            elif select_submenu == 'Back':
                pygame_event.game_state -= 1
                pygame_event.is_save_state = False
                pygame_event.is_load_state = False

    elif pygame_event.game_state == 2:
        select_submenu = False
        if pygame_event.is_save_state:
            menu_ui_save.draw(display, dt)
            select_submenu = menu_ui_save.update_for_android(mobile_key, dt, current_time, player, rpgmap)
        elif pygame_event.is_load_state:
            menu_ui_load.draw(display, dt)
            select_submenu = menu_ui_load.update_for_android(mobile_key, dt, current_time, player, rpgmap)
        if select_submenu:
            if select_submenu == 'Back':
                pygame_event.game_state -= 1
                if pygame_event.is_save_state:
                    reset_menu(menu_ui, 3)
                    pygame_event.is_save_state = False
                elif pygame_event.is_load_state:
                    reset_menu(menu_ui, 4)
                    pygame_event.is_load_state = False
            else:
                menu_ui_load.menu = menu_ui_save.menu
                pygame_event.game_state = 0
                pygame_event.is_save_state = False
                pygame_event.is_load_state = False

    input.draw_for_android(display)
    top_ui.draw_fps(display, clock)

    pg.transform.scale(display, screen.get_size(), screen)
    pg.display.flip()
