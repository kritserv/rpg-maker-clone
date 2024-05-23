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

from src import ctx, \
	quad_buffer, \
	vert_shader, \
	frag_shader, \
	program, \
	render_object, \
	surf_to_texture

from src import DeltaTime, \
	PygameEvent, \
	MenuBar, MenuFunc, \
	Terminal, \
	Timer, \
	blit_text

def main():
	pg.display.set_icon(
		pg.image.load(
			"assets/imgs/icon.png"
			)
		)
	pg.display.set_caption("RPPYG Maker")

	terminal = Terminal()

	display = pg.Surface(
			(game_size))

	default_font = pg.font.Font(
		"assets/fonts/IBMPlexSans-Regular.ttf", 
		13
		)
	black = pg.Color("black")
	white = pg.Color("white")

	menu_bar = MenuBar(
		font=default_font, 
		white=white
		)
	menu_bar.create_menu()
	menu_func = MenuFunc()

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
		
		return_value = menu_func.update(return_value, terminal)
		if return_value == 0:
			return 0

		# Graphic

		display.fill(black)

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

		frame_tex = surf_to_texture(display)
		frame_tex.use(0)
		program["tex"] = 0
		render_object.render(
			mode=moderngl.TRIANGLE_STRIP
			)

		pg.display.flip()

		frame_tex.release()

	pg.quit()
	exit()

if __name__ == "__main__":
	main()

