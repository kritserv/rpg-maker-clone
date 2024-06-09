import pygame as pg
pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

import moderngl
from sys import exit

game_size = (865, 660)
screen = pg.display.set_mode(
		(
			game_size[0], 
			game_size[1]), 
		pg.RESIZABLE | \
		pg.OPENGL | \
		pg.DOUBLEBUF
		)

from os import listdir

from src import OpenGLStuff, \
	DeltaTime, \
	PygameEvent, \
	MenuBar, MenuFunc, \
	SideBarMenu, \
	Terminal, \
	RpgMap, \
	Timer, \
	blit_text

def main():
	pg.display.set_icon(
		pg.image.load(
			"assets/imgs/icon.png"
			)
		)
	pg.display.set_caption("RPPYG Maker")

	opengl = OpenGLStuff()

	terminal = Terminal(
		venv_dir_exist="venv" in listdir()
		)

	display = pg.Surface(
			(game_size))

	default_font = pg.font.Font(
		"assets/fonts/IBMPlexSans-Regular.ttf", 
		13
		)
	black = pg.Color("black")
	white = pg.Color("white")

	rpgmap = RpgMap()

	menu_bar = MenuBar(
		font=default_font, 
		white=white
		)
	menu_bar.create_menu()
	menu_func = MenuFunc()

	sidebar_menu = SideBarMenu(
		rect = pg.Rect(
			0, 
			64, 
			280, 
			pg.display.get_desktop_sizes()[0][1]-64
			)
		)

	clock = pg.time.Clock()
	delta_time = DeltaTime()

	pygame_event = PygameEvent(
		game_size
		)

	while pygame_event.running:

		dt = delta_time.get()
		clock.tick()

		# Input

		mouse_pos = pg.mouse.get_pos()
		new_size = pygame_event.check()
		if new_size:
			display = new_size
		any_click = pygame_event.left_click or pygame_event.right_click

		# Logic

		return_value = menu_bar.update(
			any_click, 
			mouse_pos
			)
		
		return_value = menu_func.update(
			return_value, 
			terminal, 
			rpgmap
			)
		if return_value == 0:
			return 0

		sidebar_menu.update(
			menu_func.current_project_name
			)

		# Graphic

		display.fill(black)

		if rpgmap.map_data:
			rpgmap.draw(display)

		sidebar_menu.draw(display)
		menu_bar.draw(display, mouse_pos)

		curr_fps = "fps:"+str(clock.get_fps()//0.1/10)
		draw_fps_pos = (display.get_width()-100, 0)
		blit_text(
			display, 
			curr_fps, 
			default_font, 
			white, 
			draw_fps_pos
			)

		opengl.draw(display)

	pg.quit()
	exit()

if __name__ == "__main__":
	main()

