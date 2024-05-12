import pygame as pg
from .blit_text import create_text_surface
from .timer import Timer

class MenuBtn:
	def __init__(self, text, font, white, pos):
		self.width = 36
		self.text = text

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

class SubMenuBtn:
	def __init__(self, text, font, white, pos):
		self.width = 220
		self.text = text
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

	def update(self, click, mouse_pos):
		if self.rect.collidepoint(mouse_pos) and click:
			print(f"click {self.text}")
			if self.text == "Exit (Ctrl + Q)":
				return 1
			elif self.text == "Play Test (F12)":
				return 2

class ImageMenuBtn:
	def __init__(self, image_name, pos):
		self.image_name = image_name
		image_path = f"src/assets/imgs/{image_name}.png"
		self.image = pg.image.load(image_path).convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.image_hover = pg.Surface((self.rect.width + 2, self.rect.height + 2))
		self.image_hover.fill(pg.Color("cyan4"))
		self.image_hover.blit(self.image, (1, 1))

	def draw(self, screen, mouse_pos, any_submenu_opened):
		if self.rect.collidepoint(mouse_pos) and not any_submenu_opened:
			screen.blit(self.image_hover, self.rect)
		else:
			screen.blit(self.image, (self.rect[0]+1, self.rect[1]+1))

	def update(self, click, mouse_pos):
		if self.rect.collidepoint(mouse_pos) and click:
			print(f"click {self.image_name}")
			if self.image_name == "play_test":
				return 2


class SubMenu:
	def __init__(self, parent_btn, options, font, white):
		self.parent_btn = parent_btn
		self.btns = []
		self.visible = False

		bg_height = 1
		for i, option in enumerate(options):
			bg_height += 21
			pos_x, pos_y = self.parent_btn.rect.topleft
			btn = SubMenuBtn(
				option,
				font,
				white,
				(pos_x, pos_y + (i+1)*self.parent_btn.rect.height))
			self.btns.append(btn)

		self.bg = pg.Surface((220, bg_height))
		self.bg.fill(pg.Color("grey30"))

	def draw(self, screen, mouse_pos):
		if self.visible:
			screen.blit(self.bg, self.parent_btn.rect.bottomleft)
			for btn in self.btns:
				btn.draw(screen, mouse_pos)

class MenuBar:
	def __init__(self, default_font, white):
		max_screen_width = pg.display.get_desktop_sizes()[0][0]
		self.bg = pg.Surface((max_screen_width, 64))
		self.bg.fill(pg.Color("grey20"))
		self.btns = []
		self.image_btns = []
		self.btn_margin_left = 6
		self.current_x = self.btn_margin_left
		self.any_submenu_opened = False
		self.click_cooldown = Timer()
		self.click_cooldown.start()
		
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
			btn = MenuBtn(
				menu_text, 
				default_font, 
				white, 
				(self.current_x, 5)
				)
			self.btns.append(btn)
			self.current_x += btn.rect.width + self.btn_margin_left

		self.btn_margin_left = 12
		self.current_x = self.btn_margin_left
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
			btn = ImageMenuBtn(
				img,
				(self.current_x, 35)
			)
			self.image_btns.append(btn)
			self.current_x += 20 + self.btn_margin_left
			if img == "save_project" or \
				img == "delete" or \
				img == "events" or \
				img == "select":
					self.current_x += 5

		file_submenu = SubMenu(
			self.btns[0], 
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
			self.btns[1], 
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
			self.btns[2], 
			[
				"Current and Below (F2)", 
				"All Layers (F3)", 
				"Dim Other Layers (F4)"
			], 
			default_font, 
			white
			)
		mode_submenu = SubMenu(
			self.btns[3], 
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
			self.btns[4], 
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
			self.btns[5], 
			[
				"1:1", 
				"1:2", 
				"1:4"
			], 
			default_font, 
			white
			)
		tools_submenu = SubMenu(
			self.btns[6], 
			[
				"Database (F9)", 
				"Options"
			], 
			default_font, 
			white
			)
		game_submenu = SubMenu(
			self.btns[7], 
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
		for btn in self.btns:
			btn.draw(screen, mouse_pos)

		for btn in self.image_btns:
			btn.draw(screen, mouse_pos, self.any_submenu_opened)

		for submenu in self.submenus:
			submenu.draw(screen, mouse_pos)

	def update(self, click, mouse_pos):
		if click and self.click_cooldown.now()>=0.2:
			self.click_cooldown.restart()

			if not self.any_submenu_opened:
				for btn in self.image_btns:
					return_value = btn.update(click, mouse_pos)
					if return_value:
						return return_value

			for submenu in self.submenus:
				if submenu.visible:
					for btn in submenu.btns:
						return_value = btn.update(click, mouse_pos)
						if return_value:
							return return_value
			
		if self.any_submenu_opened and click:
			for submenu in self.submenus:
				submenu.visible = False
			self.any_submenu_opened = False

		for btn in self.btns:
			if btn.rect.collidepoint(mouse_pos):
				if self.any_submenu_opened:
					for submenu in self.submenus:
						if submenu.parent_btn == btn:
							submenu.visible = True
							self.any_submenu_opened = True
						else:
							submenu.visible = False
				elif click:
					for submenu in self.submenus:
						if submenu.parent_btn == btn:
							submenu.visible = True
							self.any_submenu_opened = True
		if click and not self.any_submenu_opened:
			for submenu in self.submenus:
				submenu.visible = False

		return 0