from .menu_reset import reset_menu

def pause_game_update(display, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, menu_ui, new_size, dt, current_time, platform, key, mobile_key, input, pygame_event, menu_ui_save, menu_ui_load):
    reset_meny_y_pos = display.get_size()[1]
    menu_ui_inventory.menu_y = reset_meny_y_pos
    menu_ui_skills.menu_y = reset_meny_y_pos
    menu_ui_achievement.menu_y = reset_meny_y_pos
    if menu_ui.is_open == False:
        menu_ui.is_open = True
        menu_ui.open_menu_sfx.play()
    if new_size:
        reset_menu(menu_ui, display, cursor = menu_ui.cursor)
    select_submenu = False
    slide_in = menu_ui.draw(display, dt, current_time)
    if not slide_in:
        match platform:
            case 'pc':
                select_submenu = menu_ui.update_for_pc(key, input.joysticks, dt, current_time)
            case 'android':
                select_submenu = menu_ui.update_for_android(mobile_key, [], dt, current_time)
            case 'web':
                select_submenu = menu_ui.update_for_pc(key, input.joysticks, dt, current_time)
    if select_submenu:
        match select_submenu:

            case 'Inventory':
                pygame_event.game_state = 4
                reset_menu(menu_ui_inventory, display)

            case 'Skills':
                pygame_event.game_state = 5
                reset_menu(menu_ui_skills, display)

            case 'Achievement':
                pygame_event.game_state = 6
                reset_menu(menu_ui_skills, display)

            case 'Save':
                pygame_event.game_state = 2
                pygame_event.is_save_state = True
                pygame_event.is_load_state = False
                reset_menu(menu_ui_save, display)
                reset_menu(menu_ui_load, display)

            case 'Load':
                pygame_event.game_state = 2
                pygame_event.is_load_state = True
                pygame_event.is_save_state = False
                reset_menu(menu_ui_save, display)
                reset_menu(menu_ui_load, display)

            case 'Setting':
                pygame_event.game_state = 3
                pygame_event.is_save_state = False
                pygame_event.is_load_state = False

            case 'Back':
                pygame_event.game_state -= 1
                pygame_event.is_save_state = False
                pygame_event.is_load_state = False

            case 'Exit to title':
                pygame_event.game_state = -2

            case _:
                pass
