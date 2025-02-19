import pygame as pg
from ..ui import blit_img

class Command(pg.sprite.Sprite):
    def __init__(self, name, trigger_by, sequence, xy, show, img, has_collision):
        self.name = name
        self.trigger_by = trigger_by # beginning / action / step on / always on
        self.has_triggered = False
        self.finish = False
        self.sequence = sequence
        self.pos = pg.math.Vector2(xy)

        self.show = show
        self.img = img
        self.tile_size = 16
        self.has_collision = has_collision
        if self.img:
            self.rect = self.img.get_rect(topleft=self.pos)

    def start_new_game(self):
        self.has_triggered = False
        for sequence in self.sequence:
            sequence.finish = False
        self.finish = False

    def draw(self, display, player, rpgmap, camera):
        if self.show:
            bottom_edge = player.rect.y - rpgmap.view_height
            top_edge = player.rect.y + rpgmap.view_height
            left_edge = player.rect.x + rpgmap.view_width
            right_edge = player.rect.x - rpgmap.view_width
            if bottom_edge < self.rect.y < top_edge and right_edge < self.rect.x < left_edge:
                adjusted_x = self.rect.x - camera.offset_x + display.get_size()[0] // 2
                adjusted_y = self.rect.y - camera.offset_y
                display.blit(self.img, (adjusted_x, adjusted_y))
                if self.has_collision:
                    return pg.Rect(adjusted_x, adjusted_y, self.tile_size, self.tile_size)
        return False

    def update_for_pc(self, display, dt, current_time, key, joysticks, player, rpgmap, camera, item_dict):
        if not self.name in player.clear_commands:
            finish_sequence = 0
            for sequence in self.sequence:
                if self.trigger_by == 'beginning':
                    if not self.has_triggered:
                        self.has_triggered = True
                    if self.has_triggered:
                        sequence.draw(display, dt, current_time)
                        sequence.update_for_pc(key, joysticks, player)
                elif self.trigger_by == 'action':
                    if not self.has_triggered:
                        action = key[pg.K_RETURN] or key[pg.K_KP_ENTER] or key[pg.K_z] or key[pg.K_SPACE]
                        for joystick in joysticks:
                            action = joystick.get_button(0)
                        if self.rect.collidepoint(player.focus_point):
                            if action:
                                self.has_triggered = True
                    if self.has_triggered:
                        sequence.draw(display, dt, current_time)
                        sequence.update_for_pc(key, joysticks, player)
                elif self.trigger_by == 'step on':
                    if not self.has_triggered:
                        step_on = int(player.pos.x) == int(self.pos.x) and int(player.pos.y) == int(self.pos.y)
                        if step_on:
                            self.has_triggered = True
                    if self.has_triggered:
                        sequence.draw(display, dt, current_time)
                        sequence.update_for_pc(key, joysticks, player)

                if sequence.finish:
                    finish_sequence += 1

            if finish_sequence == len(self.sequence):
                player.clear_commands.append(self.name)
                self.finish = True

        if self.trigger_by == 'always on':
            for sequence in self.sequence:
                sequence.always_on = True
                sequence.draw(display, dt, current_time)
                sequence.update_for_pc(key, joysticks, player)


    def update_for_android(self, display, dt, current_time, mobile_key, player, rpgmap, camera, item_dict):
        if not self.name in player.clear_commands:
            finish_sequence = 0
            for sequence in self.sequence:
                if self.trigger_by == 'beginning':
                        if not self.has_triggered:
                            self.has_triggered = True
                        if self.has_triggered:
                            sequence.draw(display, dt, current_time)
                            sequence.update_for_android(mobile_key, player)
                elif self.trigger_by == 'action':
                    if not self.has_triggered:
                        action = mobile_key["K_A"]
                        if self.rect.collidepoint(player.focus_point):
                            if action:
                                self.has_triggered = True
                    if self.has_triggered:
                        sequence.draw(display, dt, current_time)
                        sequence.update_for_android(mobile_key, player)

                if sequence.finish:
                    finish_sequence += 1

            if finish_sequence == len(self.sequence):
                player.clear_commands.append(self.name)
                self.finish = True

        if self.trigger_by == 'always on':
            require_game_to_pause = False
            for sequence in self.sequence:
                sequence.always_on = True
                sequence.draw(display, dt, current_time)
                sequence.update_for_android(mobile_key, player)

class PythonScript:
    def __init__(self, script):
        self.script = script
        self.finish = False
        self.always_on = False

    def update(self, player):
        if not self.finish:
            exec(self.script)
            if not self.always_on:
                self.finish = True

    def draw(self, display, dt, current_time):
        pass

    def update_for_pc(self, key, joysticks, player):
        self.update(player)

    def update_for_android(self, mobile_key, player):
        self.update(player)

class AddItem:
    def __init__(self, item):
        self.item = item
        self.finish = False
        self.always_on = False

    def update(self, player):
        if not self.finish:
            if player.items.get(self.item.name):
                player.items[self.item.name]['quant'] += 1
                player.items[self.item.name]['is_equip'] = False
            else:
                player.items[self.item.name] = {'desc': self.item.description, 'quant': 1, 'is_equip': False}
            if not self.always_on:
                self.finish = True

    def draw(self, display, dt, current_time):
        pass

    def update_for_pc(self, key, joysticks, player):
        self.update(player)

    def update_for_android(self, mobile_key, player):
        self.update(player)

class RemoveItem:
    def __init__(self, item, quant):
        self.item = item
        self.quant = quant
        self.finish = False
        self.always_on = False

    def update(self, player):
        if not self.finish:
            if player.items.get(self.item.name):
                player.items[self.item.name]['quant'] -= self.quant
            else:
                player.items[self.item.name] = {'desc': self.item.description, 'quant': 0, 'is_equip': False}
            if not self.always_on:
                self.finish = True

    def draw(self, display, dt, current_time):
        pass

    def update_for_pc(self, key, joysticks, player):
        self.update(player)

    def update_for_android(self, mobile_key, player):
        self.update(player)

class AddSkill:
    def __init__(self, skill):
        self.skill = skill
        self.finish = False
        self.always_on = False

    def update(self, player):
        if not self.finish:
            if self.skill.name not in player.skills:
                player.skills.append(self.skill.name)
                self.finish = True
            if not self.always_on:
                self.finish = True

    def draw(self, display, dt, current_time):
        pass

    def update_for_pc(self, key, joysticks, player):
        self.update(player)

    def update_for_android(self, mobile_key, player):
        self.update(player)

class RemoveSkill:
    def __init__(self, skill):
        self.skill = skill
        self.finish = False
        self.always_on = False

    def update(self, player):
        if not self.finish:
            if self.skill.name in player.skills:
                player.skills.remove(self.skill.name)
                self.finish = True
            if not self.always_on:
                self.finish = True

    def draw(self, display, dt, current_time):
        pass

    def update_for_pc(self, key, joysticks, player):
        self.update(player)

    def update_for_android(self, mobile_key, player):
        self.update(player)
