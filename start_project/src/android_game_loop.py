from .blit_text import blit_text
import pygame as pg

def run_android_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, top_ui, screen):
    dt = delta_time.get()
    clock.tick()

    # Input
    mobile_key = input.update_for_android(pygame_event)

    # Logic
    player.update(key=None, dt=dt, mobile_key=mobile_key)
    camera.update(player)

    # Graphic
    display.fill(GREY)
    rpgmap.draw_scaled_screen(display, camera, player.rect)
    display.blit(player.img, [display.get_size()[0]//2-16, display.get_size()[1]//2+-22])
    input.draw_for_android(display)
    top_ui.draw_fps(display, clock)

    pg.transform.scale(display, screen.get_size(), screen)
    pg.display.flip()
