from .base_menu import BaseMenuUI
from ..utils import json_loader, json_saver
from datetime import datetime

class MenuUISave(BaseMenuUI):
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

    def save_game(self, select_slot, player, rpgmap):
        select_slot = f"Slot {self.cursor}"
        save_slots = json_loader(self.save_path)

        select_save_slot = save_slots.get(select_slot, False) # check if empty and ask for confirm

        save_name = f"{select_slot} {datetime.now().strftime('%Y%m%d')}"
        if player.pos != player.next_pos:
            save_pos = [player.last_pos.x, player.last_pos.y]
        else:
            save_pos = [player.pos.x, player.pos.y]
        save_slots[select_slot] = {
            'name': save_name,
            'player_levels': player.levels,
            'player_xp': player.xp,
            'player_items': player.items,
            'player_variables': player.variables,
            'player_skills': player.skills,
            'player_max_hp': player.max_hp,
            'player_hp': player.hp,
            'player_pos': save_pos,
            'player_direction': player.direction,
            'player_clear_commands': player.clear_commands,
            'player_clear_achievements': player.clear_achievements,
            'current_map': rpgmap.curr_map,
            'time': datetime.now().strftime('%Y:%m:%d %H:%M:%S')
            }

        json_saver(self.save_path, save_slots)
        self.menu[self.cursor] = save_name

    def update_for_pc(self, key, joysticks, dt, current_time, player, rpgmap):
        select_slot = super(MenuUISave, self).update_for_pc(key, joysticks, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                self.save_game(select_slot, player, rpgmap)

        return select_slot

    def update_for_android(self, mobile_key, joysticks, dt, current_time, player, rpgmap):
        select_slot = super(MenuUISave, self).update_for_android(mobile_key, joysticks, dt, current_time)
        if select_slot:
            if select_slot != "Back":
                self.save_game(select_slot, player, rpgmap)

        return select_slot
