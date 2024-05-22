import pygame as pg

pg.init()

from sys import exit

win_size = (480, 160)

screen = pg.display.set_mode(
	(win_size)
	)

from src import PygameEvent, ProgramBtn, blit_text, write_line_to_file
from os import path
from pathlib import Path
from distutils.dir_util import copy_tree

def main():
	pg.display.set_icon(
		pg.image.load(
			"assets/imgs/icon.png"
			)
		)
	pg.display.set_caption("Create New Project")
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

	text_box = pg.Rect(20, 50, 440, 20)

	submit_btn = ProgramBtn(
		"Create & Open", 
		150, 
		default_font, 
		white, 
		black, 
		(70, 111)
		)

	cancel_btn = ProgramBtn(
		"Cancel", 
		150, 
		default_font, 
		white, 
		black, 
		(280, 111)
		)

	error_message = ""

	while pygame_event.running:

		clock.tick(60)

		# Input

		mouse_pos = pg.mouse.get_pos()
		pygame_event.check()
		project_name = pygame_event.user_input

		enter = False
		click_submit = submit_btn.update(pygame_event.click, mouse_pos)
		click_cancel = cancel_btn.update(pygame_event.click, mouse_pos)

		if enter or click_submit:
			if project_name:
				if not path.isdir(f"projects/{project_name}"):
					state = "working_state/work_on_project"
					write_line_to_file(project_name, state)
					return 0
				else:
					error_message = "Error, Project with that name already exists."
			else:
				error_message = "Error, Please enter a project name."

		if click_cancel:
			return 0

		# Graphic

		screen.fill(grey)
		pg.draw.rect(screen, white, text_box)
		blit_text(
			screen,
			"Enter Project Name:",
			default_font,
			white,
			(15, 20)
			)

		blit_text(
			screen,
			project_name,
			default_font,
			black,
			(30, 50)
			)

		blit_text(
			screen,
			error_message,
			default_font,
			error_col,
			(21, 77)
			)

		submit_btn.draw(screen, mouse_pos)
		cancel_btn.draw(screen, mouse_pos)

		pg.display.update()

	pg.quit()
	exit()

if __name__ == "__main__":
	try:
		main()
	except FileNotFoundError:
		print("Error: Program need to be running from root directory.")