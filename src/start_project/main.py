import numpy as np
import pygame as pg
from time import time

pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

import moderngl
from sys import exit

game_size = (240, 135)

native_res_multiplier = 3
screen = pg.display.set_mode(
	(
		game_size[0]*native_res_multiplier, 
		game_size[1]*native_res_multiplier), 
	pg.RESIZABLE | pg.OPENGL | pg.DOUBLEBUF
	)

from src import ctx, \
	quad_buffer, \
	vert_shader, \
	frag_shader, \
	program, \
	render_object, \
	surf_to_texture

from src import json_loader, \
	Player, \
	RpgMap, \
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
		(game_size))

	db = json_loader("game_data/db.json")

	pg.display.set_caption(db["main"]["main_title"])

	settings = json_loader("user_data/settings.json")
	
	scale_method = settings["scale_method"]

	player = Player(0, 64)

	rpgmap = RpgMap()
	rpgmap.load_map_data(db["maps"])

	clock = pg.time.Clock()

	grey = pg.Color("grey20")

	delta_time = DeltaTime()

	pygame_event = PygameEvent(game_size, scale_method)

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

		player.update(key, dt)

		# Graphic

		display.fill(grey)
		rpgmap.draw(display)

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
	exit()

if __name__ == "__main__":
	main()
