from .menu_reset import reset_menu

def title_screen_update(menu_ui_title, display, dt, current_time, platform, key, game_input, mobile_key, player, rpgmap, pygame_event, menu_ui, menu_ui_save, menu_ui_load, menu_ui_settings, command_list):
    slide_in = menu_ui_title.draw(display, dt, current_time)
    select_submenu = False
    if not slide_in:
        match platform:
            case 'pc':
                select_submenu = menu_ui_title.update_for_pc(key, game_input.joysticks, dt, current_time)
            case 'android':
                select_submenu = menu_ui_title.update_for_android(mobile_key, [], dt, current_time)
            case 'web':
                select_submenu = menu_ui_title.update_for_pc(key, game_input.joysticks, dt, current_time)

        match select_submenu:
            case 'New Game':
                player.start_new_game()
                pygame_event.game_state = 0
                for command in command_list:
                    command.start_new_game()
                rpgmap.start_new_game()
            case 'Continue':
                reset_menu(menu_ui_load, display)
                pygame_event.game_state = -3
            case 'Setting':
                pygame_event.game_state = -4
            case 'Quit':
                pygame_event.running = False
            case _:
                pass
    reset_menu(menu_ui, display)
    reset_menu(menu_ui_save, display)
    reset_menu(menu_ui_load, display)
    reset_menu(menu_ui_settings, display)

def reset_title_screen(menu_ui_title, display, pygame_event):
    menu_ui_title.speed = 20
    menu_ui_title.menu_y = display.get_size()[1]
    pygame_event.game_state = -1
