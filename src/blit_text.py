import pygame as pg

def create_text_surface(text, font, col) -> object:
	return font.render(text, True, col)

def blit_text(display, text, font, col, x_y_pos) -> None:
	text_surface = create_text_surface(text, font, col)
	display.blit(text_surface, x_y_pos)