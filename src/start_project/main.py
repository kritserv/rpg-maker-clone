import numpy as np
import moderngl
import pygame as pg
from time import time

pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
pg.display.set_caption("Game Title")

window_size = (640, 360)

screen = pg.display.set_mode(
	(window_size), 
	pg.RESIZABLE | pg.OPENGL | pg.DOUBLEBUF
	)

from pjsrc import ctx, \
	quad_buffer, \
	vert_shader, \
	frag_shader, \
	program, \
	render_object, \
	surf_to_texture

from pjsrc import Player, \
	DeltaTime, \
	PygameEvent, \
	blit_text

pg.display.set_icon(
	pg.image.load(
		"assets/icon.png"
		).convert_alpha()
	)

def main():
	display = pg.Surface(
		(window_size))

	player = Player(display.get_width()/2-16, display.get_height()/2-24)

	clock = pg.time.Clock()

	grey = pg.Color("grey20")

	delta_time = DeltaTime()

	pygame_event = PygameEvent(window_size)

	prev_time = time()
	while pygame_event.running:

		dt = delta_time.get()
		clock.tick()

		# Input

		new_size = pygame_event.check()
		if new_size:
			display = new_size
		key = pg.key.get_pressed()

		# Logic

		player.update(key, dt, display)

		# Graphic

		display.fill(grey)

		display.blit(player.img, (player.pos))
		
		frame_tex = surf_to_texture(display)
		frame_tex.use(0)
		program["tex"] = 0
		render_object.render(
			mode=moderngl.TRIANGLE_STRIP
			)

		pg.display.flip()

		frame_tex.release()

	pg.quit()


if __name__ == "__main__":
	main()