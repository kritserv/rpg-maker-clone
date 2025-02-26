from .menu_reset import reset_menu
import pygame as pg
from ..gameplay import RemoveItem
import random

def turn_based_update(new_size, display, dt, current_time, key, game_input, mobile_key, player, rpgmap, platform, menu_ui, pygame_event, menu_ui_turn_based, item_dict):
    display.fill('red')
    slide_in = False
    select_submenu = False
    if not menu_ui_turn_based.state == 'show infomation':
        slide_in = menu_ui_turn_based.draw(display, dt, current_time)
        if not slide_in:
            match platform:
                case 'pc':
                    select_submenu = menu_ui_turn_based.update_for_pc(key, game_input.joysticks, dt, current_time)
                case 'android':
                    select_submenu = menu_ui_turn_based.update_for_android(mobile_key, [], dt, current_time)
                case 'web':
                    select_submenu = menu_ui_turn_based.update_for_pc(key, game_input.joysticks, dt, current_time)

    # print('state:', menu_ui_turn_based.state, ', select:', select_submenu)

    if select_submenu:
        if select_submenu == 'Skill' and menu_ui_turn_based.state == 'main':
            menu_ui_turn_based.state = 'skill'
            if player.skills:
                change_choice(menu_ui_turn_based, player.skills, display)
            else:
                change_choice(menu_ui_turn_based, [' '], display)

        elif select_submenu == 'Item' and menu_ui_turn_based.state == 'main':
            menu_ui_turn_based.state = 'item'
            item_choices = [key + ' x ' + str(player.items[key]['quant']) for key in player.items if item_dict[key].is_consumable]
            if item_choices:
                change_choice(menu_ui_turn_based, item_choices, display)
            else:
                change_choice(menu_ui_turn_based, [' '], display)

        elif select_submenu != ' ' and select_submenu != 'Back' and menu_ui_turn_based.state == 'item':
            select_submenu = select_submenu.split(' x ')[0]
            select_item = player.items[select_submenu]

            player_hp_before_consume = player.hp

            if select_item['quant'] > 0:
                exec(item_dict[select_submenu].consume_effect)
                player.consume_sfx.play()
            RemoveItem(item_dict[select_submenu], 1).update(player)

            player_hp_after_consume = player.hp

            menu_ui_turn_based.state = 'show infomation'
            change_infomation(menu_ui_turn_based.infomation, [f'Using {select_submenu}', f'Your HP Restore by {player_hp_after_consume-player_hp_before_consume}', 'Enemy attack you\nusing Bite', 'You\'ve taken 5 damage\nto HP'])

        elif select_submenu == 'Skip' and menu_ui_turn_based.state == 'main':
            menu_ui_turn_based.state = 'show infomation'
            change_infomation(menu_ui_turn_based.infomation, ['You\'ve skip your turn', 'Enemy attack you\nusing Bite', 'You\'ve taken 5 damage\nto HP'])

        elif select_submenu == 'Run' and menu_ui_turn_based.state == 'main':
            success = random.random() < 0.3
            if success:
                menu_ui_turn_based.state = 'run away'
                change_infomation(menu_ui_turn_based.infomation, ['You\'ve manage\nto run away'])
            else:
                menu_ui_turn_based.state = 'show infomation'
                change_infomation(menu_ui_turn_based.infomation, ['You try to run away', 'You can\'t run away', 'Enemy attack you\nusing Bite', 'You\'ve taken 5 damage\nto HP'])

        elif select_submenu != ' ' and select_submenu != 'Back' and menu_ui_turn_based.state == 'skill':
            exec(player.skill_dict[select_submenu].skill_effect)
            menu_ui_turn_based.state = 'show infomation'
            change_infomation(menu_ui_turn_based.infomation, [f'Using {select_submenu}', 'Enemy take 5 damage\nto HP', 'Enemy attack you\nusing Bite', 'You\'ve taken 5 damage\nto HP'])

        elif select_submenu == 'Back' and menu_ui_turn_based.state == 'skill':
            menu_ui_turn_based.state = 'main'
            change_choice(menu_ui_turn_based, ('Skill', 'Item', 'Skip', 'Run'), display)

        elif select_submenu == 'Back' and menu_ui_turn_based.state == 'item':
            menu_ui_turn_based.state = 'main'
            change_choice(menu_ui_turn_based, ('Skill', 'Item', 'Skip', 'Run'), display)

        elif select_submenu == 'Back' and menu_ui_turn_based.state == 'main':
            pass

    if menu_ui_turn_based.state == 'show infomation':
        menu_ui_turn_based.infomation.draw(display, dt, current_time)

        match platform:
            case 'pc':
                menu_ui_turn_based.infomation.update_for_pc(key, game_input.joysticks, player, rpgmap)
            case 'android':
                menu_ui_turn_based.infomation.update_for_android(mobile_key, player, rpgmap)
            case 'web':
                menu_ui_turn_based.infomation.update_for_pc(key, game_input.joysticks, player, rpgmap)

        if menu_ui_turn_based.infomation.finish:
            menu_ui_turn_based.state = 'main'
            change_choice(menu_ui_turn_based, ('Skill', 'Item', 'Skip', 'Run'), display)

    elif menu_ui_turn_based.state == 'run away':
        menu_ui_turn_based.infomation.draw(display, dt, current_time)

        match platform:
            case 'pc':
                menu_ui_turn_based.infomation.update_for_pc(key, game_input.joysticks, player, rpgmap)
            case 'android':
                menu_ui_turn_based.infomation.update_for_android(mobile_key, player, rpgmap)
            case 'web':
                menu_ui_turn_based.infomation.update_for_pc(key, game_input.joysticks, player, rpgmap)

        if menu_ui_turn_based.infomation.finish:
            menu_ui_turn_based.state = 'exit'
            reset_menu_position(menu_ui_turn_based, display)
            pygame_event.game_state = 0

def change_infomation(infomation, new_dialogs):
    infomation.dialogs = new_dialogs
    infomation.active_dialog = 0
    infomation.message_done = False
    infomation.finish = False

    for i in range(len(infomation.dialogs)):
        infomation.dialogs[i] += ' ' * infomation.delay

    infomation.index = 0

def change_choice(menu_ui_turn_based, new_choices, display):
    menu_ui_turn_based.menu = new_choices
    menu_ui_turn_based.menu_len = len(new_choices)-1
    reset_menu_position(menu_ui_turn_based, display)

def reset_menu_position(menu_ui_turn_based, display):
    menu_ui_turn_based.speed = 20
    menu_ui_turn_based.menu_y = display.get_size()[1]
    menu_ui_turn_based.cursor = 0
