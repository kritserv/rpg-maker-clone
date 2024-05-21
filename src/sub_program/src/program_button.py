import pygame as pg
from .blit_text import create_text_surface

class ProgramBtn:
	def __init__(self, text, width, font, col, black, pos):
		self.text = text
		self.width = width
		self.black = black

		self.hover_bg_color = pg.Color("cyan4")

		self.text_surface = create_text_surface(
			self.text, font, col
			)
		self.rect = pg.Rect(pos[0], pos[1], self.width, self.text_surface.get_height()+4)

	def draw(self, display, mouse_pos) -> None:
		if self.rect.collidepoint(mouse_pos):
			pg.draw.rect(display, self.hover_bg_color, self.rect)
		else:
			pg.draw.rect(display, self.black, self.rect)

		text_pos = (
			self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2,
			self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2
			)

		display.blit(self.text_surface, text_pos)

	def update(self, click, mouse_pos) -> bool:
		if self.rect.collidepoint(mouse_pos) and click:
			return True
		else:
			return False