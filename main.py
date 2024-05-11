import pygame as pg
pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

from sys import exit

from src import DeltaTime, PygameEvent, MenuBar, blit_text

def main():

	pg.display.set_icon(pg.image.load("assets/imgs/icon.png"))
	pg.display.set_caption("RPPYG Maker")

	screen = pg.display.set_mode((865, 660), pg.RESIZABLE)

	default_font = pg.font.Font("assets/fonts/IBMPlexSans-Regular.ttf", 13)
	black = pg.Color("black")
	white = pg.Color("white")

	clock = pg.time.Clock()
	menu_bar = MenuBar(default_font, white)
	delta_time = DeltaTime()

	pygame_event = PygameEvent()

	while pygame_event.running:
		dt = delta_time.get()
		clock.tick()

		mouse_pos = pg.mouse.get_pos()
		pygame_event.check()
		menu_bar.update(pygame_event.click, mouse_pos)

		screen.fill(black)

		menu_bar.draw(screen, mouse_pos)

		curr_fps = f"fps: {str(clock.get_fps() // 0.1 / 10)}"
		draw_fps_pos = (screen.get_width()-100, 0)
		blit_text(screen, curr_fps, default_font, white, draw_fps_pos)

		blit_text(screen, f"click: {pygame_event.click}", default_font, white, (draw_fps_pos[0], draw_fps_pos[1]+20))
		blit_text(screen, f"submenu: {menu_bar.any_submenu_opened}", default_font, white, (draw_fps_pos[0], draw_fps_pos[1]+40))
		pg.display.update()

	pg.quit()
	exit()

if __name__ == "__main__":
	main()

