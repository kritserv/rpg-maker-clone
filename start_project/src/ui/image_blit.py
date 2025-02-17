def blit_img(display, img, x_y_pos, center=False):
    if center:
        display.blit(img, img.get_rect(center=(display.get_width()//2, display.get_height()//2)))
    else:
        display.blit(img, x_y_pos)
