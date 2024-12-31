from .blit_text import blit_text

def run_pc_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, BLACK, top_ui, debug_message, debug_font, opengl):
    dt = delta_time.get()
    clock.tick()

    # Input
    new_size, key, display = input.update_for_pc(pygame_event, display)
    rpgmap.resize_view(new_size)

    # Logic
    player.update(key, dt)
    camera.update(player)

    # Graphic
    display.fill(GREY)
    rpgmap.draw(display, camera, player.rect)
    display.blit(player.img, [display.get_size()[0]//2-16, display.get_size()[1]//2+-22])
    top_ui.draw_fps(display, clock)

    # Debug
    blit_text(display, f"{debug_message}", debug_font, BLACK, (5, 50))

    # Use OpenGL
    opengl.draw(display)
    return display
