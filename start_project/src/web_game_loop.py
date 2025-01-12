from .blit_text import blit_text
import pygame as pg

def reset_menu(menu, display, cursor = 0):
    menu.cursor = cursor
    menu.menu_x = display.get_size()[0]
    menu.speed = 450
    menu.animate_in = True

def run_web_game_loop(delta_time, clock, pygame_event, input, display, rpgmap, player, camera, GREY, BLACK, top_ui, menu_ui, menu_ui_save, menu_ui_load, screen):
    dt = delta_time.get()
    clock.tick()

    # Input
    key = input.update_for_web(pygame_event)
    for joystick in input.joysticks:
        if joystick.get_button(10):
            pygame_event.game_state = 1

    center_x = display.get_size()[0]//2
    center_y = display.get_size()[1]//2

    player.collision_border_right = pg.Rect(center_x, center_y-6, 1, 16)
    player.collision_border_left = pg.Rect(center_x-17, center_y-6, 1, 16)
    player.collision_border_top = pg.Rect(center_x-16, center_y-7, 16, 1)
    player.collision_border_bottom = pg.Rect(center_x-16, center_y+10, 16, 1)

    # Graphic
    display.fill(GREY)
    draw_count = rpgmap.draw(display, camera, player.rect, layers=['layer1', 'layer2'], get_collision=False)
    collision_rects = rpgmap.draw(display, camera, player.rect, layers=['layer3'], get_collision=True)

    # handle low fps collision
    if dt > 0.016:
        next_move = []
        if player.direction == "top":
            next_move = player.collision_border_top

        elif player.direction == "bottom":
            next_move = player.collision_border_bottom

        elif player.direction == "left":
            next_move = player.collision_border_left

        elif player.direction == "right":
            next_move = player.collision_border_right

        can_move = True
        for collision_rect in collision_rects:
            if next_move:
                if pg.Rect.colliderect(collision_rect, next_move):
                    can_move = False
                    if player.direction == "top":
                        player.pos.y += 1
                        player.rect.topleft = player.pos
                    elif player.direction == "bottom":
                        player.pos.y -= 1
                        player.rect.topleft = player.pos
                    elif player.direction == "left":
                        player.pos.x += 1
                        player.rect.topleft = player.pos
                    elif player.direction == "right":
                        player.pos.x -= 1
                        player.rect.topleft = player.pos

    display.blit(player.img, [display.get_size()[0]//2-16, display.get_size()[1]//2+-22])
    draw_count = rpgmap.draw(display, camera, player.rect, layers=['layer4'], get_collision=False)

    # Logic
    if pygame_event.game_state == 0:
        player.update(key, dt, joysticks=input.joysticks, collision_rects=collision_rects)
        camera.update(player)
        reset_menu(menu_ui, display)
        reset_menu(menu_ui_save, display)
        reset_menu(menu_ui_load, display)

    current_time = pg.time.get_ticks()
    if pygame_event.game_state == 1:
        select_submenu = False
        slide_in = menu_ui.draw(display, dt)
        if not slide_in:
            select_submenu = menu_ui.update_for_pc(key, input.joysticks, dt, current_time)
        if select_submenu:
            if select_submenu == 'Save':
                pygame_event.game_state = 2
                pygame_event.is_save_state = True
                pygame_event.is_load_state = False
                reset_menu(menu_ui_save, display)
                reset_menu(menu_ui_load, display)

            elif select_submenu == 'Load':
                pygame_event.game_state = 2
                pygame_event.is_load_state = True
                pygame_event.is_save_state = False
                reset_menu(menu_ui_save, display)
                reset_menu(menu_ui_load, display)

            elif select_submenu == 'Back':
                pygame_event.game_state -= 1
                pygame_event.is_save_state = False
                pygame_event.is_load_state = False

    elif pygame_event.game_state == 2:
        select_submenu = False
        if pygame_event.is_save_state:
            slide_in = menu_ui_save.draw(display, dt)
            if not slide_in:
                select_submenu = menu_ui_save.update_for_pc(key, input.joysticks, dt, current_time, player, rpgmap)
        elif pygame_event.is_load_state:
            slide_in = menu_ui_load.draw(display, dt)
            if not slide_in:
                select_submenu = menu_ui_load.update_for_pc(key, input.joysticks, dt, current_time, player, rpgmap)
        if select_submenu:
            if select_submenu == 'Back':
                pygame_event.game_state -= 1
                if pygame_event.is_save_state:
                    reset_menu(menu_ui, display, 3)
                    pygame_event.is_save_state = False
                elif pygame_event.is_load_state:
                    reset_menu(menu_ui, display, 4)
                    pygame_event.is_load_state = False
            else:
                menu_ui_load.menu = menu_ui_save.menu
                pygame_event.game_state = 0
                pygame_event.is_save_state = False
                pygame_event.is_load_state = False

    top_ui.draw_fps(display, clock)
    pg.draw.line(display, BLACK, (0,0), (0,display.get_size()[1]))
    pg.draw.line(display, BLACK, (display.get_size()[0]-1,0), (display.get_size()[0]-1,display.get_size()[1]))

    pg.transform.scale(display, screen.get_size(), screen)
    pg.display.flip()
