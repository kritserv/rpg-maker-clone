from .blit_text import blit_text
import pygame as pg

def run_web_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, top_ui, menu_ui, menu_ui_save, screen):
    dt = delta_time.get()
    clock.tick()

    # Input
    key = input.update_for_web(pygame_event)

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
        select_submenu = menu_ui.update_for_pc(key, dt, current_time)
        if select_submenu:
            pygame_event.game_state = 0
        menu_ui.draw(display)

    top_ui.draw_fps(display, clock)

    pg.transform.scale(display, screen.get_size(), screen)
    pg.display.flip()
