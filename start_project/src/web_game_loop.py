from .blit_text import blit_text
import pygame as pg

def run_web_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, top_ui, screen):
    dt = delta_time.get()
    clock.tick()

    # Input
    key = input.update_for_web(pygame_event)

    # Logic
    player.update(key, dt)
    camera.update(player)

    # Graphic
    display.fill(GREY)
    rpgmap.draw(display, camera, player.rect)
    display.blit(player.img, [display.get_size()[0]//2-16, display.get_size()[1]//2+-22])
    top_ui.draw_fps(display, clock)

    pg.transform.scale(display, screen.get_size(), screen)
    pg.display.flip()
