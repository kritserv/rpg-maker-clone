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

class SubMenuButton:
	def __init__(self, text, font, white, pos):
		self.width = 220
		self.text = text
		self.font = font
		self.pos = pos
		self.margin_left = 6

		self.hover_bg_color = pg.Color("cyan4")

		self.text_surface = create_text_surface(
			self.text, font, white
			)
		self.rect = pg.Rect(pos[0], pos[1], self.width, self.text_surface.get_height()+4)

	def draw(self, screen, mouse_pos):
		if self.rect.collidepoint(mouse_pos):
			pg.draw.rect(screen, self.hover_bg_color, self.rect)

		text_pos = (
			self.rect.x + self.margin_left,
			self.rect.y
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

class SubMenu:
	def __init__(self, parent_button, options, font, white):
		self.parent_button = parent_button
		self.options = options
		self.font = font
		self.white = white
		self.buttons = []
		self.visible = False

		bg_height = 1
		for i, option in enumerate(self.options):
			bg_height += 21
			pos_x, pos_y = self.parent_button.rect.topleft
			button = SubMenuButton(
				option,
				self.font,
				self.white,
				(pos_x, pos_y + (i+1)*self.parent_button.rect.height))
			self.buttons.append(button)

		self.bg = pg.Surface((220, bg_height))
		self.bg.fill(pg.Color("grey30"))

	def draw(self, screen, mouse_pos):
		if self.visible:
			screen.blit(self.bg, self.parent_button.rect.bottomleft)
			for button in self.buttons:
				button.draw(screen, mouse_pos)

class MenuBar:
	def __init__(self, default_font, white):
		max_screen_width = pg.display.get_desktop_sizes()[0][0]
		self.bg = pg.Surface((max_screen_width, 64))
		self.bg.fill(pg.Color("grey20"))
		self.buttons = []
		self.image_buttons = []
		self.button_margin_left = 6
		self.current_x = self.button_margin_left
		self.any_submenu_opened = False
		
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
			self.image_buttons.append(button)
			self.current_x += 20 + self.button_margin_left
			if img == "save_project" or \
				img == "delete" or \
				img == "events" or \
				img == "select":
					self.current_x += 5

		file_submenu = SubMenu(
			self.buttons[0], 
			[
				"New project (Ctrl + N)", 
				"Open project (Ctrl + O)", 
				"Close project", 
				"Save Project (Ctrl + S)", 
				"Exit (Ctrl + Q)"
			], 
			default_font, 
			white
			)
		edit_submenu = SubMenu(
			self.buttons[1], 
			[
				"Undo (Ctrl + Z)", 
				"Cut (Ctrl + X)", 
				"Copy (Ctrl + C)", 
				"Paste (Ctrl + V)", 
				"Delete (Del)"
			], 
			default_font, 
			white
			)
		view_submenu = SubMenu(
			self.buttons[2], 
			[
				"Current and Below (F2)", 
				"All Layers (F3)", 
				"Dim Other Layers (F4)"
			], 
			default_font, 
			white
			)
		mode_submenu = SubMenu(
			self.buttons[3], 
			[
				"Layer 1 (F5)", 
				"Layer 2 (F6)", 
				"Layer 3 (F7)", 
				"Events (F8)"
			], 
			default_font, 
			white
			)
		draw_submenu = SubMenu(
			self.buttons[4], 
			[
				"Pencil", 
				"Rectangle", 
				"Eclipse", 
				"Flood Fill", 
				"Select"
			], 
			default_font, 
			white
			)
		scale_submenu = SubMenu(
			self.buttons[5], 
			[
				"1:1", 
				"1:2", 
				"1:4"
			], 
			default_font, 
			white
			)
		tools_submenu = SubMenu(
			self.buttons[6], 
			[
				"Database (F9)", 
				"Options"
			], 
			default_font, 
			white
			)
		game_submenu = SubMenu(
			self.buttons[7], 
			[
				"Play Test (F12)", 
				"Change Title", 
				"Open Game Folder"
			], 
			default_font, 
			white
			)

		self.submenus = [
			file_submenu, 
			edit_submenu, 
			view_submenu,
			mode_submenu,
			draw_submenu,
			scale_submenu,
			tools_submenu,
			game_submenu
			]

	def draw(self, screen, mouse_pos):
		screen.blit(self.bg, (0, 0))
		for button in self.buttons:
			button.draw(screen, mouse_pos)

		for button in self.image_buttons:
			button.draw(screen, mouse_pos)

		for submenu in self.submenus:
			submenu.draw(screen, mouse_pos)

	def update(self, mouse_btn_down, mouse_pos):
		if self.any_submenu_opened and mouse_btn_down:
			for submenu in self.submenus:
				submenu.visible = False
			self.any_submenu_opened = False

		for button in self.buttons:
			if button.rect.collidepoint(mouse_pos):
				if self.any_submenu_opened:
					for submenu in self.submenus:
						if submenu.parent_button == button:
							submenu.visible = True
							self.any_submenu_opened = True
						else:
							submenu.visible = False
				elif mouse_btn_down:
					for submenu in self.submenus:
						if submenu.parent_button == button:
							submenu.visible = True
							self.any_submenu_opened = True
		if mouse_btn_down and not self.any_submenu_opened:
			for submenu in self.submenus:
				submenu.visible = False