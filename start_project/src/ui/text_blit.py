import pygame as pg

def create_text_surface(text, font, col):
    '''
    (not sure if already fix for older version) pygame-ce can insert new row with '\n'
    but not pygame, so here are the implement for that.
    '''
    lines = text.split('\n')
    line_surfaces = [font.render(line, True, col) for line in lines]

    line_height = font.get_linesize()
    total_height = line_height * len(lines)
    max_width = max(surface.get_width() for surface in line_surfaces)

    complete_surface = pg.Surface((max_width, total_height), pg.SRCALPHA)

    for i, line_surface in enumerate(line_surfaces):
        complete_surface.blit(line_surface, (0, i * line_height))

    return complete_surface

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
