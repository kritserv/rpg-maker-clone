import pygame as pg

def filter_effect(display, filter):
    match filter:
        case 'blur':
            screen_copy = display.copy()
            scale = 1/10
            small_size = (int(screen_copy.get_width() * scale), int(screen_copy.get_height() * scale))
            smaller_surface = pg.transform.smoothscale(screen_copy, small_size)
            blurred = pg.transform.smoothscale(smaller_surface, screen_copy.get_size())
            display.blit(blurred, (0, 0))

        case 'darken':
            # darken display
            rect = pg.Rect([0, 0, display.get_width(), display.get_height()])
            shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
            pg.draw.rect(shape_surf, (25, 25, 25, 125), shape_surf.get_rect())
            display.blit(shape_surf, rect)
