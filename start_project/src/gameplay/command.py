import pygame as pg
from ..ui import blit_img

class Command(pg.sprite.Sprite):
    def __init__(self, trigger_by, sequence, xy, show, img, has_collision):
        self.trigger_by = trigger_by
        self.has_triggered = False
        self.sequence = sequence
        self.pos = pg.math.Vector2(xy)

        self.show = show
        self.img = img
        self.tile_size = 16
        self.has_collision = has_collision
        if self.img:
            self.rect = self.img.get_rect(topleft=self.pos)

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
        for sequence in self.sequence:
            if self.trigger_by == 'beginning':
                if not self.has_triggered:
                    self.has_triggered = True
                if self.has_triggered:
                    sequence.draw(display, dt, current_time)
                    sequence.update_for_pc(key, joysticks, player, item_dict)
            elif self.trigger_by == 'action':
                if not self.has_triggered:
                    action = key[pg.K_RETURN] or key[pg.K_KP_ENTER] or key[pg.K_z] or key[pg.K_SPACE]
                    for joystick in joysticks:
                        action = joystick.get_button(1)
                    if self.rect.collidepoint(player.focus_point):
                        if action:
                            self.has_triggered = True
                if self.has_triggered:
                    sequence.draw(display, dt, current_time)
                    sequence.update_for_pc(key, joysticks, player, item_dict)



    def update_for_android(self, display, dt, current_time, mobile_key, player, rpgmap, camera, item_dict):
        for sequence in self.sequence:
            if self.trigger_by == 'beginning':
                    if not self.has_triggered:
                        self.has_triggered = True
                    if self.has_triggered:
                        sequence.draw(display, dt, current_time)
                        sequence.update_for_android(mobile_key, player, item_dict)
            elif self.trigger_by == 'action':
                if not self.has_triggered:
                    action = mobile_key["K_A"]
                    if self.rect.collidepoint(player.focus_point):
                        if action:
                            self.has_triggered = True
                if self.has_triggered:
                    sequence.draw(display, dt, current_time)
                    sequence.update_for_android(mobile_key, player, item_dict)


class AddItem:
    def __init__(self, item):
        self.item = item
        self.finish = False

    def update(self, action, player, item_dict):
        if not self.finish:
            if player.items.get(self.item.name):
                player.items[self.item.name]['quant'] += 1
            else:
                player.items[self.item.name] = {'attrs': self.item.attrs, 'quant': 1}
            self.finish = True

    def draw(self, display, dt, current_time):
        pass

    def update_for_pc(self, key, joysticks, player, item_dict):
        action = key[pg.K_RETURN] or key[pg.K_KP_ENTER] or key[pg.K_z] or key[pg.K_SPACE]
        for joystick in joysticks:
            action = joystick.get_button(1)
        self.update(action, player, item_dict)

    def update_for_android(self, mobile_key, player, item_dict):
        action = mobile_key["K_A"]
        self.update(action, player, item_dict)
