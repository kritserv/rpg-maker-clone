from .menu_reset import reset_menu
import pygame as pg

def turn_based_update(new_size, display, dt, current_time, key, game_input, mobile_key, player, rpgmap, platform, menu_ui, pygame_event, menu_ui_turn_based):
    display.fill('white')
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

            menu_ui_turn_based.menu = player.skills
            menu_ui_turn_based.menu_len = len(player.skills)-1
            menu_ui_turn_based.speed = 20
            menu_ui_turn_based.menu_y = display.get_size()[1]
            menu_ui_turn_based.cursor = 0

        elif select_submenu == 'Item' and menu_ui_turn_based.state == 'main':
            menu_ui_turn_based.state = 'show infomation'
            change_infomation(menu_ui_turn_based.infomation, ['Using Item', 'Your HP Restore by 30', 'Enemy attack you\nusing Bite', 'You\'ve taken 5 damage to HP'])

        elif select_submenu == 'Skip' and menu_ui_turn_based.state == 'main':
            menu_ui_turn_based.state = 'show infomation'
            change_infomation(menu_ui_turn_based.infomation, ['You\'ve skip your turn', 'Enemy attack you\nusing Bite', 'You\'ve taken 5 damage to HP'])

        elif select_submenu == 'Run' and menu_ui_turn_based.state == 'main':
            menu_ui_turn_based.state = 'show infomation'
            change_infomation(menu_ui_turn_based.infomation, ['You try to run away', 'You can\'t run away\nfrom this battle'])

        elif select_submenu == 'Punch' and menu_ui_turn_based.state == 'skill':
            menu_ui_turn_based.state = 'show infomation'
            change_infomation(menu_ui_turn_based.infomation, ['Using Punch', 'It is super effective', 'Enemy take 10 damage to HP', 'Enemy attack you\nusing Bite', 'You\'ve taken 5 damage to HP'])

        elif select_submenu == 'Slash' and menu_ui_turn_based.state == 'skill':
            menu_ui_turn_based.state = 'show infomation'
            change_infomation(menu_ui_turn_based.infomation, ['Using Slash', 'It is super effective', 'Enemy take 10 damage to HP', 'Enemy attack you\nusing Bite', 'You\'ve taken 5 damage to HP'])

        elif select_submenu == 'Back' and menu_ui_turn_based.state == 'skill':
            menu_ui_turn_based.state = 'main'

            menu_ui_turn_based.menu = ('Skill', 'Item', 'Skip', 'Run')
            menu_ui_turn_based.menu_len = 3
            menu_ui_turn_based.speed = 20
            menu_ui_turn_based.menu_y = display.get_size()[1]
            menu_ui_turn_based.cursor = 0

        elif select_submenu == 'Back' and menu_ui_turn_based.state == 'main':
            menu_ui_turn_based.state = 'exit'

            menu_ui_turn_based.speed = 20
            menu_ui_turn_based.menu_y = display.get_size()[1]
            menu_ui_turn_based.cursor = 0
            pygame_event.game_state = 0

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

            menu_ui_turn_based.menu = ('Skill', 'Item', 'Skip', 'Run')
            menu_ui_turn_based.menu_len = 3
            menu_ui_turn_based.speed = 20
            menu_ui_turn_based.menu_y = display.get_size()[1]
            menu_ui_turn_based.cursor = 0

def change_infomation(infomation, new_dialogs):
    infomation.dialogs = new_dialogs
    infomation.active_dialog = 0
    infomation.message_done = False
    infomation.finish = False

    for i in range(len(infomation.dialogs)):
        infomation.dialogs[i] += ' ' * infomation.delay

    infomation.index = 0
