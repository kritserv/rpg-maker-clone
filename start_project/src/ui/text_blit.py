import pygame as pg

def create_text_surface(text, font, col):
	return font.render(text, True, col)

def blit_text(screen, text, font, col, x_y_pos, rotate=False, center=False):
    text_surface = create_text_surface(text, font, col)
    if rotate:
        text_surface = pg.transform.rotate(text_surface, rotate)

    if center:
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_width // 2, screen_height // 2)
        screen.blit(text_surface, text_rect)
    else:
        screen.blit(text_surface, x_y_pos)
