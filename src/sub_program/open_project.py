import pygame as pg

pg.font.init()

from sys import exit
from os import listdir

projects = listdir("projects/")

win_height = 160 + (20 * (len(projects) - 1))

win_size = (480, win_height)

screen = pg.display.set_mode(
	(win_size)
	)

from src import PygameEvent, ProgramBtn, blit_text, write_line_to_file
from distutils.dir_util import copy_tree

def main(projects):
	pg.display.set_icon(
		pg.image.load(
			"assets/imgs/icon.png"
			)
		)
	pg.display.set_caption("Open Project")
	default_font = pg.font.Font(
		"assets/fonts/IBMPlexSans-Regular.ttf",
		13
		)
	grey = pg.Color("grey15")
	black = pg.Color("black")
	white = pg.Color("white")
	error_col = pg.Color("yellow")

	clock = pg.time.Clock()

	pygame_event = PygameEvent()

	btn_y = 50
	project_btns = dict()
	for project in projects:
		project_btn = ProgramBtn(
			project,
			220,
			default_font,
			white,
			black,
			(15, btn_y)
			)
		btn_y += 22
		project_btns[project_btn] = project

	cancel_btn_y = 111 + (20 * (len(projects) - 1))
	cancel_btn = ProgramBtn(
		"Cancel",
		150,
		default_font,
		white,
		black,
		(280, cancel_btn_y)
		)

	error_message = ""

	if not projects:
		error_message = "Error, No projects found in the projects folder."

	while pygame_event.running:

		clock.tick(60)

		# Input

		mouse_pos = pg.mouse.get_pos()
		pygame_event.check()

		project_name = None
		for project_btn in project_btns:
			click_project = project_btn.update(pygame_event.click, mouse_pos)
			if click_project:
				project_name = project_btns[project_btn]
				break
		click_cancel = cancel_btn.update(pygame_event.click, mouse_pos)

		if project_name:
			state = "working_state/work_on_project"
			write_line_to_file(project_name, state)
			return 0

		if click_cancel:
			return 0

		# Graphic

		screen.fill(grey)

		blit_text(
			screen,
			"Select Project:",
			default_font,
			white,
			(15, 20)
			)

		blit_text(
			screen,
			error_message,
			default_font,
			error_col,
			(21, 77)
			)

		for project_btn in project_btns:
			project_btn.draw(screen, mouse_pos)

		cancel_btn.draw(screen, mouse_pos)

		pg.display.update()

	pg.quit()
	exit()

if __name__ == '__main__':
	try:
		main(projects)
	except FileNotFoundError:
		print("Error: Program need to be running from root directory.")
