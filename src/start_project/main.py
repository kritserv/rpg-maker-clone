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

display = pg.Surface(
	(window_size))

from src import ctx, \
	quad_buffer, \
	vert_shader, \
	frag_shader, \
	program, \
	render_object, \
	surf_to_texture, \
	Player

pg.display.set_icon(
	pg.image.load(
		"asset/icon.png"
		).convert_alpha()
	)

def check_type(event):
	keydown, keyup, quit, resize = False, False, False, False
	new_size = None
	if event.type == pg.KEYDOWN:
		keydown = True
	elif event.type == pg.KEYUP:
		keyup = True
	elif event.type == pg.QUIT:
		quit = True
	elif event.type == pg.VIDEORESIZE:
		resize = True
		ratio = event.w / window_size[0]
		new_height = int(event.h / ratio)
		new_size = (window_size[0], new_height)
	return keydown, keyup, quit, resize, new_size

def check_arrow_key(event, keydown, keyup):
	up, down, left, right = False, False, False, False
	if keydown:
		if event.key == pg.K_UP:
			up = True
		elif event.key == pg.K_DOWN:
			down = True
		elif event.key == pg.K_LEFT:
			left = True
		elif event.key == pg.K_RIGHT:
			right = True
	elif keyup:
		if event.key == pg.K_UP or event.key == pg.K_DOWN or event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
			up, down, left, right = False, False, False, False

	return up, down, left, right

def check_interact(event, keydown, keyup):
	interact = False
	if keydown:
		if event.key == pg.K_RETURN:
			interact = True
	elif keyup:
		if event.key == pg.K_z or event.key == pg.K_SPACE:
			interact = True

	return interact

def check_cancel(event, keydown, keyup):
	cancel = False
	if keydown:
		if event.key == pg.K_ESCAPE:
			cancel = True
	elif keyup:
		if event.key == pg.K_x or event.key == pg.K_KP0:
			cancel = True

	return cancel

def check_quit_game_event(event, quit, keydown):
	run = True
	if quit:
		run = False
	if keydown:
		if event.key == pg.K_q and pg.key.get_mods() & pg.KMOD_CTRL: # Ctrl + Q
			run = False
		elif event.key == pg.K_F4 and pg.key.get_mods() & pg.KMOD_ALT:  # Alt + F4
			run = False

	return run

def main(display):

	player = Player(display.get_width()/2-16, display.get_height()/2-24)

	clock = pg.time.Clock()

	grey = pg.Color("grey90")

	run = True

	prev_time = time()
	while run:

		dt = time() - prev_time
		prev_time = time()

		clock.tick()

		# Input

		for event in pg.event.get():
			keydown, keyup, quit, resize, new_size = check_type(event)
			if resize:
				display = pg.Surface(new_size)
			interact = check_interact(event, keydown, keyup)
			cancel = check_cancel(event, keydown, keyup)
			run = check_quit_game_event(event, quit, keydown)
			up, down, left, right = check_arrow_key(event, keydown, keyup)

		key = pg.key.get_pressed()

		# Logic

		player.update(key, dt, display)

		# Graphic

		display.fill(grey)

		display.blit(player.image, (player.pos))
		
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
	main(display)