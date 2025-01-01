from .blit_text import blit_text
import pygame as pg

def run_pc_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, BLACK, top_ui, debug_message, debug_font, opengl, menu_ui):
    dt = delta_time.get()
    clock.tick()

    # Input
    new_size, key, display = input.update_for_pc(pygame_event, display)
    rpgmap.resize_view(new_size)

    # Logic
    if pygame_event.game_state == 0:
        player.update(key, dt)
        camera.update(player)
        menu_ui.cursor = 0

    # Graphic
    display.fill(GREY)
    rpgmap.draw(display, camera, player.rect)
    display.blit(player.img, [display.get_size()[0]//2-16, display.get_size()[1]//2+-22])

    if pygame_event.game_state == 1:
        current_time = pg.time.get_ticks()
        menu_ui.update_for_pc(key, dt, current_time)
        menu_ui.draw(display)

    top_ui.draw_fps(display, clock)

    # Debug
    blit_text(display, f"{debug_message}", debug_font, BLACK, (5, 50))

    # Use OpenGL
    opengl.draw(display)
    return display
