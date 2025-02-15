import pygame as pg

def create_text_surface(text, font, col):
	return font.render(text, True, col)

def blit_text(screen, text, font, col, x_y_pos, rotate=False):
	text_surface = create_text_surface(text, font, col)
	if rotate:
		text_surface = pg.transform.rotate(text_surface, rotate)
	screen.blit(text_surface, x_y_pos)
