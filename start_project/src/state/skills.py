from .menu_reset import reset_menu

def skill_update(new_size, menu_ui_skills, display, dt, current_time, platform, key, game_input, player, mobile_key, pygame_event, menu_ui, skill_dict):
    select_submenu = False
    if new_size:
        reset_menu(menu_ui_skills, display, cursor = menu_ui_skills.cursor)
    slide_in = menu_ui_skills.draw(display, dt, current_time, skill_dict)
    if player.skills:
        menu_ui_skills.menu = [skill for skill in player.skills]
        menu_ui_skills.menu_len = len(player.skills)-1
    else:
        menu_ui_skills.menu = (' ')
        menu_ui_skills.menu_len = 0
    if not slide_in:
        match platform:
            case 'pc':
                select_submenu = menu_ui_skills.update_for_pc(key, game_input.joysticks, dt, current_time)
            case 'android':
                select_submenu = menu_ui_skills.update_for_android(mobile_key, [], dt, current_time)
            case 'web':
                select_submenu = menu_ui_skills.update_for_pc(key, game_input.joysticks, dt, current_time)
    if select_submenu:
        match select_submenu:
            case 'Back':
                reset_menu(menu_ui_skills, display)
                reset_menu(menu_ui, display, 1)
                pygame_event.game_state = 1
