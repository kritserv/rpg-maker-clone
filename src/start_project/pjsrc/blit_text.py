import pygame as pg

def create_text_surface(text, font, col):
	return font.render(text, True, col)

def blit_text(screen, text, font, col, x_y_pos):
	text_surface = create_text_surface(text, font, col)
	screen.blit(text_surface, x_y_pos)