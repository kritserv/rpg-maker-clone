from .menu_reset import reset_menu
import pygame as pg
from ..gameplay import RemoveItem
from ..ui import blit_img, blit_text
import random

def turn_based_update(new_size, display, dt, current_time, key, game_input, mobile_key, player, rpgmap, platform, menu_ui, pygame_event, menu_ui_turn_based, item_dict, enemy_dict):

    slide_in = False
    select_submenu = False
    enemy = enemy_dict[menu_ui_turn_based.current_enemy]

    menu_ui_turn_based.draw2(display, dt, current_time, player, enemy)
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

    if select_submenu:
        player_hp_before_turn_start = player.hp
        enemy_hp_before_turn_start = enemy.hp
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
            menu_ui_turn_based.state = 'show infomation'
            select_submenu = select_submenu.split(' x ')[0]
            select_item = player.items[select_submenu]

            if select_item['quant'] > 0:
                exec(item_dict[select_submenu].consume_effect)
                player.consume_sfx.play()
            else:
                player.battle_info = []
            RemoveItem(item_dict[select_submenu], 1).update(player)

            info = player.battle_info
            if enemy.hp > 0:
                exec(enemy.moves)
                info += enemy.battle_info
            else:
                menu_ui_turn_based.state = 'end battle'
                exec(enemy.defeat_reward)
                info += enemy.battle_info

            if player.hp <= 0:
                menu_ui_turn_based.state = 'game over'
                info.append('You\'ve been defeated')

            change_infomation(menu_ui_turn_based.infomation, info)

        elif select_submenu == 'Skip' and menu_ui_turn_based.state == 'main':
            menu_ui_turn_based.state = 'show infomation'
            info = ['You\'ve skip your turn']
            if enemy.hp > 0:
                exec(enemy.moves)
                info += enemy.battle_info
            else:
                menu_ui_turn_based.state = 'end battle'
                exec(enemy.defeat_reward)
                info += enemy.battle_info

            if player.hp <= 0:
                menu_ui_turn_based.state = 'game over'
                info.append('You\'ve been defeated')

            change_infomation(menu_ui_turn_based.infomation, info)

        elif select_submenu == 'Run' and menu_ui_turn_based.state == 'main':
            if random.random() < 0.3:
                menu_ui_turn_based.state = 'end battle'
                change_infomation(menu_ui_turn_based.infomation, ['You\'ve manage\nto run away'])
            else:
                menu_ui_turn_based.state = 'show infomation'
                info = ['You try to run away', 'You can\'t run away']
                if enemy.hp > 0:
                    exec(enemy.moves)
                    info += enemy.battle_info
                else:
                    menu_ui_turn_based.state = 'end battle'
                    exec(enemy.defeat_reward)
                    info += enemy.battle_info

                if player.hp <= 0:
                    menu_ui_turn_based.state = 'game over'
                    info.append('You\'ve been defeated')

                change_infomation(menu_ui_turn_based.infomation, info)

        elif select_submenu != ' ' and select_submenu != 'Back' and menu_ui_turn_based.state == 'skill':
            menu_ui_turn_based.state = 'show infomation'
            exec(player.skill_dict[select_submenu].skill_effect)
            info = player.battle_info
            if enemy.hp > 0:
                exec(enemy.moves)
                info += enemy.battle_info
            else:
                menu_ui_turn_based.state = 'end battle'
                exec(enemy.defeat_reward)
                info += enemy.battle_info

            if player.hp <= 0:
                menu_ui_turn_based.state = 'game over'
                info.append('You\'ve been defeated')

            change_infomation(menu_ui_turn_based.infomation, info)

        elif select_submenu == 'Back' and menu_ui_turn_based.state == 'skill':
            menu_ui_turn_based.state = 'main'
            change_choice(menu_ui_turn_based, ('Skill', 'Item', 'Skip', 'Run'), display)

        elif select_submenu == 'Back' and menu_ui_turn_based.state == 'item':
            menu_ui_turn_based.state = 'main'
            change_choice(menu_ui_turn_based, ('Skill', 'Item', 'Skip', 'Run'), display)

        elif select_submenu == 'Back' and menu_ui_turn_based.state == 'main':
            pass

        if player.hp < player_hp_before_turn_start:
            player.enemy_attack_sfx.play()
        if enemy.hp < enemy_hp_before_turn_start:
            player.player_attack_sfx.play()

    if menu_ui_turn_based.state == 'show infomation':
        menu_ui_turn_based.infomation.draw(display, dt, current_time)

        match platform:
            case 'pc':
                menu_ui_turn_based.infomation.update_for_pc(dt, key, game_input.joysticks, player, rpgmap, pygame_event, False, False)
            case 'android':
                menu_ui_turn_based.infomation.update_for_android(dt, mobile_key, player, rpgmap, pygame_event, False, False)
            case 'web':
                menu_ui_turn_based.infomation.update_for_pc(dt, key, game_input.joysticks, player, rpgmap, pygame_event, False, False)

        if menu_ui_turn_based.infomation.finish:
            menu_ui_turn_based.state = 'main'
            change_choice(menu_ui_turn_based, ('Skill', 'Item', 'Skip', 'Run'), display)

    elif menu_ui_turn_based.state == 'end battle':
        menu_ui_turn_based.infomation.draw(display, dt, current_time)

        match platform:
            case 'pc':
                menu_ui_turn_based.infomation.update_for_pc(dt, key, game_input.joysticks, player, rpgmap, pygame_event, False, False)
            case 'android':
                menu_ui_turn_based.infomation.update_for_android(dt, mobile_key, player, rpgmap, pygame_event, False, False)
            case 'web':
                menu_ui_turn_based.infomation.update_for_pc(dt, key, game_input.joysticks, player, rpgmap, pygame_event, False, False)

        if menu_ui_turn_based.infomation.finish:
            menu_ui_turn_based.state = 'exit'
            change_choice(menu_ui_turn_based, ('Skill', 'Item', 'Skip', 'Run'), display)
            reset_menu_position(menu_ui_turn_based, display)
            enemy.hp = enemy.max_hp
            pygame_event.game_state = 0

    elif menu_ui_turn_based.state == 'game over':
        menu_ui_turn_based.infomation.draw(display, dt, current_time)

        match platform:
            case 'pc':
                menu_ui_turn_based.infomation.update_for_pc(dt, key, game_input.joysticks, player, rpgmap, pygame_event, False, False)
            case 'android':
                menu_ui_turn_based.infomation.update_for_android(dt, mobile_key, player, rpgmap, pygame_event, False, False)
            case 'web':
                menu_ui_turn_based.infomation.update_for_pc(dt, key, game_input.joysticks, player, rpgmap, pygame_event, False, False)

        if menu_ui_turn_based.infomation.finish:
            menu_ui_turn_based.state = 'exit'
            change_choice(menu_ui_turn_based, ('Skill', 'Item', 'Skip', 'Run'), display)
            reset_menu_position(menu_ui_turn_based, display)
            enemy.hp = enemy.max_hp
            pygame_event.game_state = -2

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
