from .base_menu import BaseMenuUI

class MenuUI(BaseMenuUI):
    def __init__(self, g):
        menu_items = ('Inventory', 'Skills', 'Achievement', 'Save', 'Load', 'Setting', 'Exit to title')
        super().__init__(menu_items, g)

        self.play_sound = True
