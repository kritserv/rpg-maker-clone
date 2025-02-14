from .menu_reset import reset_menu

def main_game_update(platform, player, key, mobile_key, input, dt, collision_rects, camera, menu_ui, menu_ui_save, menu_ui_load, menu_ui_title, menu_ui_settings, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, display):
    match platform:
        case 'pc':
            player.update(key, dt, joysticks=input.joysticks, collision_rects=collision_rects)
        case 'android':
            player.update(key=None, dt=dt, mobile_key=mobile_key, joysticks=[], collision_rects=collision_rects)
        case 'web':
            player.update(key, dt, joysticks=input.joysticks, collision_rects=collision_rects)

    camera.update(player)
    reset_menu(menu_ui, display)
    reset_menu(menu_ui_save, display)
    reset_menu(menu_ui_load, display)
    reset_menu(menu_ui_title, display)
    reset_menu(menu_ui_settings, display)
    reset_menu(menu_ui_inventory, display)
    reset_menu(menu_ui_skills, display)
    reset_menu(menu_ui_achievement, display)
    menu_ui.is_open = False
