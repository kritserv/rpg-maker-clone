import pygame as pg
from ..ui import blit_img

class Command(pg.sprite.Sprite):
    def __init__(self, name, trigger_by, sequence, xy, show, img, has_collision, map_name, run_in_loop):
        self.name = name
        self.trigger_by = trigger_by # beginning / action / step on / always on / change map
        self.has_triggered = False
        self.finish = False
        self.sequence = sequence
        self.pos = pg.math.Vector2(xy)

        self.show = show
        self.img = img
        self.tile_size = 16
        self.has_collision = has_collision
        self.map_name = map_name
        self.run_in_loop = run_in_loop

        if self.img:
            self.rect = self.img.get_rect(topleft=self.pos)

    def reset(self):
        self.has_triggered = False
        for sequence in self.sequence:
            sequence.finish = False
        self.finish = False

    def start_new_game(self):
        self.reset()

    def draw(self, display, player, rpgmap, camera):
        if self.show and (rpgmap.curr_map==self.map_name or self.map_name=='all_map'):
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

    def update_for_pc(self, display, dt, current_time, key, joysticks, player, rpgmap, camera, item_dict, game_state):
        if not self.name in player.clear_commands and (rpgmap.curr_map==self.map_name or self.map_name=='all_map'):
            finish_sequence = 0
            for i, sequence in enumerate(self.sequence):
                if i == finish_sequence:
                    match self.trigger_by:
                        case 'beginning':
                            if not self.has_triggered:
                                self.has_triggered = True
                            if self.has_triggered:
                                sequence.draw(display, dt, current_time)
                                sequence.update_for_pc(key, joysticks, player, rpgmap)
                        case 'action':
                            if not self.has_triggered:
                                action = key[pg.K_RETURN] or key[pg.K_KP_ENTER] or key[pg.K_z] or key[pg.K_SPACE]
                                for joystick in joysticks:
                                    action = joystick.get_button(0)
                                if game_state == 0 and self.rect.collidepoint(player.focus_point):
                                    if action:
                                        self.has_triggered = True
                            if self.has_triggered:
                                sequence.draw(display, dt, current_time)
                                sequence.update_for_pc(key, joysticks, player, rpgmap)
                        case 'step on':
                            if not self.has_triggered:
                                step_on = player.last_pos == self.pos or player.pos == self.pos
                                if step_on:
                                    self.has_triggered = True
                            if self.has_triggered:
                                sequence.draw(display, dt, current_time)
                                sequence.update_for_pc(key, joysticks, player, rpgmap)

                if sequence.finish:
                    finish_sequence += 1

            if finish_sequence == len(self.sequence):
                player.clear_commands.append(self.name)
                self.finish = True

        if self.trigger_by == 'always on':
            for sequence in self.sequence:
                sequence.always_on = True
                sequence.draw(display, dt, current_time)
                sequence.update_for_pc(key, joysticks, player, rpgmap)

        if self.run_in_loop and self.name in player.clear_commands:
            player.clear_commands.remove(self.name)
            self.reset()


    def update_for_android(self, display, dt, current_time, mobile_key, player, rpgmap, camera, item_dict, game_state):
        if not self.name in player.clear_commands and (rpgmap.curr_map==self.map_name or self.map_name=='all_map'):
            finish_sequence = 0
            for i, sequence in enumerate(self.sequence):
                if i == finish_sequence:
                    match self.trigger_by:
                        case 'beginning':
                            if not self.has_triggered:
                                self.has_triggered = True
                            if self.has_triggered:
                                sequence.draw(display, dt, current_time)
                                sequence.update_for_android(mobile_key, player, rpgmap)
                        case 'action':
                            if not self.has_triggered:
                                action = mobile_key["K_A"]
                                if game_state == 0 and self.rect.collidepoint(player.focus_point):
                                    if action:
                                        self.has_triggered = True
                            if self.has_triggered:
                                sequence.draw(display, dt, current_time)
                                sequence.update_for_android(mobile_key, player, rpgmap)
                        case 'step on':
                            if not self.has_triggered:
                                step_on = int(player.pos.x) == int(self.pos.x) and int(player.pos.y) == int(self.pos.y)
                                if step_on:
                                    self.has_triggered = True
                            if self.has_triggered:
                                sequence.draw(display, dt, current_time)
                                sequence.update_for_android(mobile_key, player, rpgmap)

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
                sequence.update_for_android(mobile_key, player, rpgmap)

        if self.run_in_loop and self.name in player.clear_commands:
            player.clear_commands.remove(self.name)
            self.reset()

class PythonScript:
    def __init__(self, script):
        self.script = script
        self.finish = False
        self.always_on = False

    def update(self, player, rpgmap):
        if not self.finish:
            exec(self.script)
            if not self.always_on:
                self.finish = True

    def draw(self, display, dt, current_time):
        pass

    def update_for_pc(self, key, joysticks, player, rpgmap):
        self.update(player, rpgmap)

    def update_for_android(self, mobile_key, player, rpgmap):
        self.update(player, rpgmap)

class AddItem:
    def __init__(self, item, quant):
        self.item = item
        self.quant = quant
        self.finish = False
        self.always_on = False

    def update(self, player):
        if not self.finish:
            if player.items.get(self.item.name):
                player.items[self.item.name]['quant'] += self.quant
                player.items[self.item.name]['is_equip'] = False
            else:
                player.items[self.item.name] = {'desc': self.item.description, 'quant': 1, 'is_equip': False}
            if not self.always_on:
                self.finish = True

    def draw(self, display, dt, current_time):
        pass

    def update_for_pc(self, key, joysticks, player, rpgmap):
        self.update(player)

    def update_for_android(self, mobile_key, player, rpgmap):
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

    def update_for_pc(self, key, joysticks, player, rpgmap):
        self.update(player)

    def update_for_android(self, mobile_key, player, rpgmap):
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

    def update_for_pc(self, key, joysticks, player, rpgmap):
        self.update(player)

    def update_for_android(self, mobile_key, player, rpgmap):
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

    def update_for_pc(self, key, joysticks, player, rpgmap):
        self.update(player)

    def update_for_android(self, mobile_key, player, rpgmap):
        self.update(player)

class Teleport:
    def __init__(self, map_name, pos):
        self.map_name = map_name
        self.pos = pos
        self.finish = False
        self.always_on = False

    def update(self, player, rpgmap):
        if not self.finish:
            player.last_pos = pg.math.Vector2(self.pos)
            rpgmap.curr_map = self.map_name

            player.pos = player.last_pos
            player.next_pos = player.last_pos
            player.dirvec = pg.math.Vector2(0, 0)
            player.between_tiles = False
            player.rect.topleft = self.pos

            player.remembered_obstacle_pos = {}

            if player.pos == self.pos:
                if not self.always_on:
                    self.finish = True

    def draw(self, display, dt, current_time):
        pass

    def update_for_pc(self, key, joysticks, player, rpgmap):
        self.update(player, rpgmap)

    def update_for_android(self, mobile_key, player, rpgmap):
        self.update(player, rpgmap)

class FadeOut:
    def __init__(self):
        self.fade_level = 0
        self.finish = False
        self.always_on = False

    def draw(self, display, dt, current_time):
        if not self.finish:
            rect = pg.Rect([0, 0, display.get_width(), display.get_height()])
            shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
            pg.draw.rect(shape_surf, (0, 0, 0, int(self.fade_level)), shape_surf.get_rect())
            display.blit(shape_surf, rect)
            if self.fade_level < 254:
                self.fade_level += 1000 * dt


    def update(self, player, rpgmap):
        if self.fade_level >= 254:
            if not self.always_on:
                self.finish = True
                self.fade_level = 0
            else:
                self.fade_level = 255

    def update_for_pc(self, key, joysticks, player, rpgmap):
        self.update(player, rpgmap)

    def update_for_android(self, mobile_key, player, rpgmap):
        self.update(player, rpgmap)

class FadeIn:
    def __init__(self):
        self.fade_level = 255
        self.finish = False
        self.always_on = False

    def draw(self, display, dt, current_time):
        if not self.finish:
            rect = pg.Rect([0, 0, display.get_width(), display.get_height()])
            shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
            pg.draw.rect(shape_surf, (0, 0, 0, int(self.fade_level)), shape_surf.get_rect())
            display.blit(shape_surf, rect)
            if self.fade_level > 1:
                self.fade_level -= 1000 * dt

    def update(self, player, rpgmap):
        if self.fade_level < 1:
            if not self.always_on:
                self.finish = True
                self.fade_level = 255

    def update_for_pc(self, key, joysticks, player, rpgmap):
        self.update(player, rpgmap)

    def update_for_android(self, mobile_key, player, rpgmap):
        self.update(player, rpgmap)
