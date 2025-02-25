from .menu_reset import reset_menu

def achievement_update(new_size, menu_ui_achievement, display, dt, current_time, key, game_input, mobile_key, platform, menu_ui, pygame_event):
    select_submenu = False
    if new_size:
        reset_menu(menu_ui_achievement, display, cursor = menu_ui_achievement.cursor)
    slide_in = menu_ui_achievement.draw(display, dt, current_time)
    if not slide_in:
        match platform:
            case 'pc':
                select_submenu = menu_ui_achievement.update_for_pc(key, game_input.joysticks, dt, current_time)
            case 'android':
                select_submenu = menu_ui_achievement.update_for_android(mobile_key, [], dt, current_time)
            case 'web':
                select_submenu = menu_ui_achievement.update_for_pc(key, game_input.joysticks, dt, current_time)
    if select_submenu:
        match select_submenu:
            case 'Back':
                reset_menu(menu_ui_achievement, display)
                reset_menu(menu_ui, display, 2)
                pygame_event.game_state = 1
