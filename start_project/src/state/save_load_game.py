from .menu_reset import reset_menu

def save_load_game_update(pygame_event, new_size, menu_ui_save, display, dt, current_time, platform, key, mobile_key, game_input, player, rpgmap, menu_ui_load, menu_ui, command_list):
    select_submenu = False
    if pygame_event.is_save_state:
        if new_size:
            reset_menu(menu_ui_save, display, cursor = menu_ui_save.cursor)
        slide_in = menu_ui_save.draw(display, dt, current_time)
        if not slide_in:
            match platform:
                case 'pc':
                    select_submenu = menu_ui_save.update_for_pc(key, game_input.joysticks, dt, current_time, player, rpgmap)
                case 'android':
                    select_submenu = menu_ui_save.update_for_android(mobile_key, [], dt, current_time, player, rpgmap)
                case 'web':
                    select_submenu = menu_ui_save.update_for_pc(key, game_input.joysticks, dt, current_time, player, rpgmap)
    elif pygame_event.is_load_state:
        if new_size:
            reset_menu(menu_ui_load, display, cursor = menu_ui_load.cursor)
        slide_in = menu_ui_load.draw(display, dt, current_time)
        if not slide_in:
            match platform:
                case 'pc':
                    select_submenu = menu_ui_load.update_for_pc(key, game_input.joysticks, dt, current_time, player, rpgmap)
                case 'android':
                    select_submenu = menu_ui_load.update_for_android(mobile_key, [], dt, current_time, player, rpgmap)
                case 'web':
                    select_submenu = menu_ui_load.update_for_pc(key, game_input.joysticks, dt, current_time, player, rpgmap)
    if select_submenu:
        match select_submenu:
            case 'Back':
                pygame_event.game_state -= 1
                if pygame_event.is_save_state:
                    reset_menu(menu_ui, display, 3)
                    pygame_event.is_save_state = False
                elif pygame_event.is_load_state:
                    reset_menu(menu_ui, display, 4)
                    pygame_event.is_load_state = False
            case _:
                for command in command_list:
                    command.start_new_game()

                menu_ui_load.menu = menu_ui_save.menu
                pygame_event.game_state = 0
                pygame_event.is_save_state = False
                pygame_event.is_load_state = False
