import pygame as pg
from .blit_text import create_text_surface

class MenuButton:
	def __init__(self, text, font, white, pos):
		self.width = 35
		self.text = text
		self.font = font
		self.pos = pos

		self.hover_bg_color = pg.Color("cyan4")

		self.text_surface = create_text_surface(
			self.text, font, white
			)
		self.rect = pg.Rect(pos[0], pos[1], self.width, self.text_surface.get_height()+4)

	def draw(self, screen, mouse_pos):
		if self.rect.collidepoint(mouse_pos):
			pg.draw.rect(screen, self.hover_bg_color, self.rect)

		text_pos = (
			self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2,
			self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2
			)

		screen.blit(self.text_surface, text_pos)

class MenuBar:
	def __init__(self, default_font, white):
		self.buttons = []
		for menu in [
			["File", (5,5)], 
			["Edit", (40,5)], 
			["View", (75,5)], 
			["Mode", (116,5)], 
			["Draw", (161,5)], 
			["Tools", (203,5)], 
			["Tools", (248,5)], 
			["Game", (292,5)], 
			["Help", (340,5)]
			]:
			menu_text, menu_pos = menu
			self.buttons.append(
				MenuButton(
					menu_text, 
					default_font, 
					white, 
					menu_pos
					)
				)

	def draw(self, screen, mouse_pos):
		for button in self.buttons:
			button.draw(screen, mouse_pos)