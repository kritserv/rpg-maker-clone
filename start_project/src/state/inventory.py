from .menu_reset import reset_menu
import pygame as pg

def inventory_update(new_size, menu_ui_inventory, display, dt, current_time, platform, key, mobile_key, game_input, player, item_dict, menu_ui, pygame_event):
    select_submenu = False

    if new_size:
        reset_menu(menu_ui_inventory, display, cursor = menu_ui_inventory.cursor)
    slide_in = menu_ui_inventory.draw(display, dt, current_time, player.items, item_dict)
    if player.items:
        menu_ui_inventory.menu = [key for key in player.items]
    else:
        menu_ui_inventory.menu = (' ')
    if not slide_in:
        match platform:
            case 'android':
                select_submenu = menu_ui_inventory.update_for_android(mobile_key, [], dt, current_time, game_input)
            case _:
                select_submenu = menu_ui_inventory.update_for_pc(key, game_input.joysticks, dt, current_time, game_input)
    if select_submenu:
        match select_submenu:
            case 'Back':
                reset_menu(menu_ui_inventory, display)
                reset_menu(menu_ui, display, 0)
                pygame_event.game_state = 1
            case _:
                if current_time - menu_ui_inventory.last_cursor_move_time > menu_ui_inventory.cursor_cooldown_time:
                    if player.items.get(select_submenu):
                        if player.items[select_submenu]['is_equip']:
                            player.items[select_submenu]['is_equip'] = False
                            player.unequip_sfx.play()
                        else:
                            player.items[select_submenu]['is_equip'] = True
                            player.equip_sfx.play()
                    menu_ui_inventory.last_cursor_move_time = current_time
