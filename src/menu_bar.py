import pygame as pg
from .blit_text import create_text_surface

class MenuButton:
	def __init__(self, text, font, white, pos):
		self.width = 36
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

class ImageMenuButton:
	def __init__(self, image_path, pos):
		self.image = pg.image.load(image_path).convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.image_hover = pg.Surface((self.rect.width + 2, self.rect.height + 2))
		self.image_hover.fill(pg.Color("cyan4"))
		self.image_hover.blit(self.image, (1, 1))

	def draw(self, screen, mouse_pos):
		if self.rect.collidepoint(mouse_pos):
			screen.blit(self.image_hover, self.rect)
		else:
			screen.blit(self.image, (self.rect[0]+1, self.rect[1]+1))

class MenuBar:
	def __init__(self, default_font, white):
		max_screen_width = pg.display.get_desktop_sizes()[0][0]
		self.bg = pg.Surface((max_screen_width, 64))
		self.bg.fill(pg.Color("grey20"))
		self.buttons = []
		self.button_margin_left = 6
		self.current_x = self.button_margin_left
		
		for menu_text in [
			"File", 
			"Edit", 
			"View", 
			"Mode", 
			"Draw", 
			"Scale", 
			"Tools", 
			"Game"
			]:
			button = MenuButton(
				menu_text, 
				default_font, 
				white, 
				(self.current_x, 5)
				)
			self.buttons.append(button)
			self.current_x += button.rect.width + self.button_margin_left

		self.button_margin_left = 12
		self.current_x = self.button_margin_left
		for img in [
			"new_project", 
			"open_project", 
			"save_project", 
			"cut", 
			"copy", 
			"paste", 
			"delete", 
			"undo", 
			"layer_1", 
			"layer_2", 
			"layer_3", 
			"events", 
			"pencil", 
			"rectangle", 
			"eclipse", 
			"flood_fill", 
			"select", 
			"1to1", 
			"1to2", 
			"1to4", 
			"database", 
			"play_test"
			]:
			button = ImageMenuButton(
				f"assets/imgs/{img}.png",
				(self.current_x, 35)
			)
			self.buttons.append(button)
			self.current_x += 20 + self.button_margin_left
			if img == "save_project" or \
				img == "delete" or \
				img == "events" or \
			 	img == "select":
					self.current_x += 5

	def draw(self, screen, mouse_pos):
		screen.blit(self.bg, (0, 0))
		for button in self.buttons:
			button.draw(screen, mouse_pos)