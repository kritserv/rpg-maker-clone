from .menu_reset import reset_menu

def inventory_update(new_size, menu_ui_inventory, display, dt, current_time, platform, key, mobile_key, input, menu_ui, pygame_event):
    select_submenu = False
    if new_size:
        reset_menu(menu_ui_inventory, display, cursor = menu_ui_inventory.cursor)
    slide_in = menu_ui_inventory.draw(display, dt, current_time)
    if not slide_in:
        match platform:
            case 'pc':
                select_submenu = menu_ui_inventory.update_for_pc(key, input.joysticks, dt, current_time, input)
            case 'android':
                select_submenu = menu_ui_inventory.update_for_android(mobile_key, [], dt, current_time, input)
            case 'web':
                select_submenu = menu_ui_inventory.update_for_pc(key, input.joysticks, dt, current_time, input)
    if select_submenu:
        match select_submenu:
            case 'Back':
                reset_menu(menu_ui_inventory, display)
                reset_menu(menu_ui, display, 0)
                pygame_event.game_state = 1
