from .base_menu import BaseMenuUI
from ..utils import json_loader, json_saver
import pygame as pg

class MenuUILoad(BaseMenuUI):
    def __init__(self, save_file_path, g):
        full_path = g['full_path']
        self.save_path = f"{full_path}/user_data/save.json"
        if save_file_path:
            '''
            file path for android (need to save externally so it doesn't get reset when game update)
            example path: /data/user/0/org.test.myapp/files/save.json
            '''

            self.save_path = f"{save_file_path}/save.json"

        try:
            save_slots = json_loader(self.save_path)
        except FileNotFoundError:
            json_saver(self.save_path, {
              "Slot 0": {},
              "Slot 1": {},
              "Slot 2": {},
              "Slot 3": {},
              "Slot 4": {},
              "Slot 5": {},
              "Slot 6": {}
            })
            save_slots = json_loader(self.save_path)

        menu_items = []
        for key, items in save_slots.items():
            if items.get('name', False):
                menu_items.append(items.get('name'))
            else:
                menu_items.append(key)
        super().__init__(menu_items, g)
        self.play_sound = True

    def load_player_and_map(self, select_save_slot, player, rpgmap):
        if select_save_slot:

            player.last_pos = pg.math.Vector2(select_save_slot.get('player_pos'))
            rpgmap.curr_map = select_save_slot.get('current_map')

            player.pos = player.last_pos
            player.next_pos = player.last_pos
            player.dirvec = pg.math.Vector2(0, 0)
            player.between_tiles = False
            player.rect.topleft = player.pos

            player.direction = select_save_slot.get('player_direction')
            player.remembered_obstacle_pos = {(player.pos.x, player.pos.y, player.direction): False}
            player.levels = select_save_slot.get('player_levels')
            player.xp = select_save_slot.get('player_xp')
            player.items = select_save_slot.get('player_items')
            player.skills = select_save_slot.get('player_skills')
            player.variables = select_save_slot.get('player_variables')
            player.max_hp = select_save_slot.get('player_max_hp')
            player.hp = select_save_slot.get('player_hp')
            player.clear_commands = select_save_slot['player_clear_commands']
            player.clear_achievements = select_save_slot['player_clear_achievements']
            return True
        return False

    def load_game(self, select_slot, player, rpgmap):
        select_slot = f"Slot {self.cursor}"
        save_slots = json_loader(self.save_path)

        select_save_slot = save_slots.get(select_slot, False) # check if empty and ask for confirm

        res = self.load_player_and_map(select_save_slot, player, rpgmap)
        return res

    def update_for_pc(self, key, joysticks, dt, current_time, player, rpgmap):
        select_slot = super(MenuUILoad, self).update_for_pc(key, joysticks, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                load_success = self.load_game(select_slot, player, rpgmap)
                if load_success:
                    return select_slot
                else:
                    select_slot = False

        return select_slot

    def update_for_android(self, mobile_key, joysticks, dt, current_time, player, rpgmap):
        select_slot = super(MenuUILoad, self).update_for_android(mobile_key, joysticks, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                load_success = self.load_game(select_slot, player, rpgmap)
                if load_success:
                    return select_slot
                else:
                    select_slot = False

        return select_slot
