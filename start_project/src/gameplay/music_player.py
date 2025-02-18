import pygame as pg
from ..utils import asset_loader

class MusicPlayer:
    def __init__(self):
        self.current_music = ''
        self.old_music = ''

    def update(self):
        if self.old_music != self.current_music:
            asset_loader('music', self.current_music)
            self.old_music = self.current_music
            pg.mixer.music.play(-1)
