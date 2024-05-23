import pygame as pg
from dataclasses import dataclass, field
from .blit_text import create_text_surface
from .timer import Timer

@dataclass(slots=True, kw_only=True)
class MenuBtn:
	width: int = 36
	text: str
	white: object
	pos: tuple
	font: object
	hover_bg_color: object = field(
		default_factory=lambda: pg.Color("cyan4")
		)
	text_surface: object = field(
		default_factory=object
		)
	rect: object = field(
		default_factory=object
		)

	def create_text(self):
		self.text_surface: object = create_text_surface(
			self.text, self.font, self.white
			)
		self.rect: object = pg.Rect(
			self.pos[0], 
			self.pos[1], 
			self.width, 
			self.text_surface.get_height()+4
			)

	def draw(self, display, mouse_pos) -> None:
		if self.rect.collidepoint(mouse_pos):
			pg.draw.rect(display, self.hover_bg_color, self.rect)

		text_pos = (
			self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2,
			self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2
			)

		display.blit(self.text_surface, text_pos)

@dataclass(slots=True, kw_only=True)
class SubMenuBtn:
	width: int = 220
	text: str
	margin_left: int = 6
	white: object
	pos: tuple
	font: object
	hover_bg_color: object = field(
		default_factory=lambda: pg.Color("cyan4")
		)
	text_surface: object = field(
		default_factory=object
		)
	rect: object = field(
		default_factory=object
		)

	def create_text(self):
		self.text_surface = create_text_surface(
			self.text, self.font, self.white
			)
		self.rect = pg.Rect(
			self.pos[0], 
			self.pos[1], 
			self.width, 
			self.text_surface.get_height()+4
			)

	def draw(self, display, mouse_pos) -> None:
		if self.rect.collidepoint(mouse_pos):
			pg.draw.rect(display, self.hover_bg_color, self.rect)

		text_pos = (
			self.rect.x + self.margin_left,
			self.rect.y
			)

		display.blit(self.text_surface, text_pos)

	def update(self, left_click, mouse_pos) -> str or None:
		if self.rect.collidepoint(mouse_pos) and left_click:
			return self.text

@dataclass(slots=True, kw_only=True)
class ImageMenuBtn:
	img_name: str
	pos: tuple
	image_path: str = field(
		default_factory=str
		)
	image: object = field(
		default_factory=object
		)
	rect: object = field(
		default_factory=object
		)
	image_hover: object = field(
		default_factory=object
		)

	def create_img(self):
		image_path = f"assets/imgs/{self.img_name}.png"
		self.image = pg.image.load(image_path).convert_alpha()
		self.rect = self.image.get_rect(topleft=self.pos)
		self.image_hover = pg.Surface((self.rect.width + 2, self.rect.height + 2))
		self.image_hover.fill(pg.Color("cyan4"))
		self.image_hover.blit(self.image, (1, 1))

	def draw(self, display, mouse_pos, any_submenu_opened) -> None:
		if self.rect.collidepoint(mouse_pos) and not any_submenu_opened:
			display.blit(self.image_hover, self.rect)
		else:
			display.blit(self.image, (self.rect[0]+1, self.rect[1]+1))

	def update(self, left_click, mouse_pos) -> str or None:
		if self.rect.collidepoint(mouse_pos) and left_click:
			return self.img_name

@dataclass(slots=True, kw_only=True)
class SubMenu:
	parent_btn: object
	options: list
	font: object
	white: object
	btns: list = field(
		default_factory=list
		)
	visible: bool = False
	bg: object = field(
		default_factory=object
		)

	def create_menu(self):
		bg_height = 1
		for i, option in enumerate(self.options):
			bg_height += 21
			pos_x, pos_y = self.parent_btn.rect.topleft
			btn = SubMenuBtn(
				text=option,
				font=self.font,
				white=self.white,
				pos=(pos_x, pos_y + (i+1)*self.parent_btn.rect.height))
			btn.create_text()
			self.btns.append(btn)

		self.bg = pg.Surface((220, bg_height))
		self.bg.fill(pg.Color("grey30"))

	def draw(self, display, mouse_pos) -> None:
		if self.visible:
			display.blit(self.bg, self.parent_btn.rect.bottomleft)
			for btn in self.btns:
				btn.draw(display, mouse_pos)

@dataclass(slots=True, kw_only=True)
class MenuBar:
	max_display_width: int = pg.display.get_desktop_sizes()[0][0]
	font: object
	white: object
	bg: object = field(
		default_factory=object
		)
	btns: list = field(
		default_factory=list
		)
	image_btns: list = field(
		default_factory=list
		)
	btn_margin_left: int = 6
	current_x: int = 6
	any_submenu_opened: bool = False
	left_click_cooldown: object = Timer()
	submenus: list = field(
		default_factory=list
		)

	def create_menu(self):
		self.bg = pg.Surface((self.max_display_width, 64))
		self.bg.fill(pg.Color("grey20"))
		
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
				text=menu_text, 
				font=self.font, 
				white=self.white, 
				pos=(self.current_x, 5)
				)
			btn.create_text()
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
			"ellipse", 
			"flood_fill", 
			"select", 
			"1to1", 
			"1to2", 
			"1to4", 
			"database", 
			"play_test"
			]:
			btn = ImageMenuBtn(
				img_name=img,
				pos=(self.current_x, 35)
			)
			btn.create_img()
			self.image_btns.append(btn)
			self.current_x += 20 + self.btn_margin_left
			if img == "save_project" or \
				img == "delete" or \
				img == "events" or \
				img == "select":
					self.current_x += 5

		file_submenu = SubMenu(
			parent_btn=self.btns[0], 
			options=[
				"New project (Ctrl + N)", 
				"Open project (Ctrl + O)", 
				"Close project", 
				"Save Project (Ctrl + S)", 
				"Exit (Ctrl + Q)"
			], 
			font=self.font, 
			white=self.white
			)
		file_submenu.create_menu()
		edit_submenu = SubMenu(
			parent_btn=self.btns[1], 
			options=[
				"Undo (Ctrl + Z)", 
				"Cut (Ctrl + X)", 
				"Copy (Ctrl + C)", 
				"Paste (Ctrl + V)", 
				"Delete (Del)"
			], 
			font=self.font, 
			white=self.white
			)
		edit_submenu.create_menu()
		view_submenu = SubMenu(
			parent_btn=self.btns[2], 
			options=[
				"Current and Below (F2)", 
				"All Layers (F3)", 
				"Dim Other Layers (F4)"
			], 
			font=self.font, 
			white=self.white
			)
		view_submenu.create_menu()
		mode_submenu = SubMenu(
			parent_btn=self.btns[3], 
			options=[
				"Layer 1 (F5)", 
				"Layer 2 (F6)", 
				"Layer 3 (F7)", 
				"Events (F8)"
			], 
			font=self.font, 
			white=self.white
			)
		mode_submenu.create_menu()
		draw_submenu = SubMenu(
			parent_btn=self.btns[4], 
			options=[
				"Pencil", 
				"Rectangle", 
				"Ellipse", 
				"Flood Fill", 
				"Select"
			], 
			font=self.font, 
			white=self.white
			)
		draw_submenu.create_menu()
		scale_submenu = SubMenu(
			parent_btn=self.btns[5], 
			options=[
				"1:1", 
				"1:2", 
				"1:4"
			], 
			font=self.font, 
			white=self.white
			)
		scale_submenu.create_menu()
		tools_submenu = SubMenu(
			parent_btn=self.btns[6], 
			options=[
				"Database (F9)", 
				"Options"
			], 
			font=self.font, 
			white=self.white
			)
		tools_submenu.create_menu()
		game_submenu = SubMenu(
			parent_btn=self.btns[7], 
			options=[
				"Play Test (F12)", 
				"Change Title", 
				"Open Game Folder"
			], 
			font=self.font, 
			white=self.white
			)
		game_submenu.create_menu()
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
		self.left_click_cooldown.start()

	def draw(self, display, mouse_pos) -> None:
		display.blit(self.bg, (0, 0))
		for btn in self.btns:
			btn.draw(display, mouse_pos)

		for btn in self.image_btns:
			btn.draw(display, mouse_pos, self.any_submenu_opened)

		for submenu in self.submenus:
			submenu.draw(display, mouse_pos)

	def update(self, left_click, mouse_pos) -> str or int or None:
		if left_click and self.left_click_cooldown.now()>=0.2:
			self.left_click_cooldown.restart()

			if not self.any_submenu_opened:
				for btn in self.image_btns:
					return_value = btn.update(left_click, mouse_pos)
					if return_value:
						return return_value

			for submenu in self.submenus:
				if submenu.visible:
					for btn in submenu.btns:
						return_value = btn.update(left_click, mouse_pos)
						if return_value:
							return return_value
			
		if self.any_submenu_opened and left_click:
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
				elif left_click:
					for submenu in self.submenus:
						if submenu.parent_btn == btn:
							submenu.visible = True
							self.any_submenu_opened = True
		if left_click and not self.any_submenu_opened:
			for submenu in self.submenus:
				submenu.visible = False

		return 0