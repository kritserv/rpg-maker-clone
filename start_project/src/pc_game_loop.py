from .blit_text import blit_text
import pygame as pg

def reset_menu(menu, cursor = 0):
    menu.cursor = cursor
    menu.menu_x = 0
    menu.speed = 450
    menu.animate_in = True

def run_pc_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, BLACK, top_ui, debug_message, debug_font, opengl, menu_ui, menu_ui_save):
    dt = delta_time.get()
    clock.tick()

    # Input
    new_size, key, display = input.update_for_pc(pygame_event, display)
    rpgmap.resize_view(new_size)

    # Logic
    if pygame_event.game_state == 0:
        player.update(key, dt)
        camera.update(player)
        reset_menu(menu_ui)
        reset_menu(menu_ui_save)

    # Graphic
    display.fill(GREY)
    rpgmap.draw(display, camera, player.rect)
    display.blit(player.img, [display.get_size()[0]//2-16, display.get_size()[1]//2+-22])

    current_time = pg.time.get_ticks()
    if pygame_event.game_state == 1:
        select_submenu = menu_ui.update_for_pc(key, dt, current_time)
        if select_submenu:
            if select_submenu == 'Save':
                pygame_event.game_state = 2
                reset_menu(menu_ui_save)
            elif select_submenu == 'Back':
                pygame_event.game_state -= 1
        menu_ui.draw(display, dt)

    elif pygame_event.game_state == 2:
        select_submenu = menu_ui_save.update_for_pc(key, dt, current_time, player, rpgmap)
        if select_submenu:
            if select_submenu == 'Back':
                pygame_event.game_state -= 1
                reset_menu(menu_ui, 3)
            else:
                pygame_event.game_state = 0
        menu_ui_save.draw(display, dt)

    top_ui.draw_fps(display, clock)

    # Debug
    blit_text(display, f"{debug_message}", debug_font, BLACK, (5, 50))

    # Use OpenGL
    opengl.draw(display)
    return display
