from .blit_text import blit_text
import pygame as pg

def reset_menu(menu, cursor = 0):
    menu.cursor = cursor
    menu.menu_x = 0
    menu.speed = 450
    menu.animate_in = True

def run_android_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, top_ui, menu_ui, menu_ui_save, screen):
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

    # Graphic
    display.fill(GREY)
    rpgmap.draw_scaled_screen(display, camera, player.rect)
    display.blit(player.img, [display.get_size()[0]//2-16, display.get_size()[1]//2+-22])

    if pygame_event.game_state == 1:
        current_time = pg.time.get_ticks()
        select_submenu = menu_ui.update_for_android(mobile_key, dt, current_time)
        if select_submenu:
            if select_submenu == 'Save':
                pygame_event.game_state = 2
            elif select_submenu == 'Back':
                pygame_event.game_state -= 1
        menu_ui.draw(display, dt)

    elif pygame_event.game_state == 2:
        current_time = pg.time.get_ticks()
        select_submenu = menu_ui_save.update_for_android(mobile_key, dt, current_time)
        if select_submenu:
            if select_submenu == 'Back':
                pygame_event.game_state = 1
                reset_menu(menu_ui, 3)
            else:
                pygame_event.game_state = 0
        menu_ui_save.draw(display, dt)

    input.draw_for_android(display)
    top_ui.draw_fps(display, clock)

    pg.transform.scale(display, screen.get_size(), screen)
    pg.display.flip()
