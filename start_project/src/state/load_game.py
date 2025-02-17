from .menu_reset import reset_menu

def load_game_update(new_size, menu_ui, menu_ui_load, menu_ui_save, display, dt, current_time, key, game_input, platform, mobile_key, player, rpgmap, pygame_event):
    select_submenu = False
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
                pygame_event.game_state = -2
                if pygame_event.is_save_state:
                    reset_menu(menu_ui, display, 3)
                    pygame_event.is_save_state = False
                elif pygame_event.is_load_state:
                    reset_menu(menu_ui, display, 4)
                    pygame_event.is_load_state = False
            case _:
                menu_ui_load.menu = menu_ui_save.menu
                pygame_event.game_state = 0
                pygame_event.is_save_state = False
                pygame_event.is_load_state = False
