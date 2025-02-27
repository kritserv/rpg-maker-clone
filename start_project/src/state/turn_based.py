from .menu_reset import reset_menu
import pygame as pg
from ..gameplay import RemoveItem
from ..ui import blit_img, blit_text
import random

def turn_based_update(new_size, display, dt, current_time, key, game_input, mobile_key, player, rpgmap, platform, menu_ui, pygame_event, menu_ui_turn_based, item_dict, enemy_dict):
    display.fill('black')
    slide_in = False
    select_submenu = False
    enemy = enemy_dict[menu_ui_turn_based.current_enemy]

    if player.hp < 0:
        player.hp = 0
    if enemy.hp < 0:
        enemy.hp = 0

    if enemy.hp > 0:
        blit_img(display, enemy.img, enemy.img.get_rect(center=(display.get_width()//2, display.get_height()//4)))

    player_hp = player.hp/player.max_hp
    if 0.4 > player_hp >= 0:
        rect_col = 'red'
        font_col = 'darkred'
    elif 0.7 > player_hp >= 0.4:
        rect_col = 'yellow'
        font_col = 'orange'
    else:
        rect_col = 'green'
        font_col = 'darkgreen'

    blit_text(display, f'player: {player.hp} / {player.max_hp}', menu_ui_turn_based.menu_font, pg.Color(font_col), (5,70))
    pg.draw.rect(display, pg.Color('grey20'), (5, 80, 100, 6))
    pg.draw.rect(display, pg.Color(rect_col), (5, 80, int(player.hp/player.max_hp*100), 6))

    enemy_hp = enemy.hp/enemy.max_hp
    if 0.4 > enemy_hp >= 0:
        rect_col = 'red'
        font_col = 'darkred'
    elif 0.7 > enemy_hp >= 0.4:
        rect_col = 'yellow'
        font_col = 'orange'
    else:
        rect_col = 'green'
        font_col = 'darkgreen'

    blit_text(display, f'{enemy.name}: {enemy.hp} / {enemy.max_hp}', menu_ui_turn_based.menu_font, font_col, (display.get_width()-135,5))
    pg.draw.rect(display, pg.Color('grey20'), (display.get_width()-135, 15, 100, 6))
    pg.draw.rect(display, rect_col, (display.get_width()-135, 15, int(enemy.hp/enemy.max_hp*100), 6))

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
