import pygame as pg

pg.font.init()

from sys import exit

win_size = (480, 160)

screen = pg.display.set_mode(
	(win_size)
	)

from src import PygameEvent, ProgramBtn, blit_text, read_line_from_file, json_dumper, json_loader
from os import path
from pathlib import Path
from distutils.dir_util import copy_tree

def main():
	pg.display.set_icon(
		pg.image.load(
			"assets/imgs/icon.png"
			)
		)
	pg.display.set_caption("Change Title")
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

	project_name = read_line_from_file("working_state/last_open_project")

	db_path = f"projects/{project_name}/game_data/db.json"
	db = json_loader(db_path)

	pygame_event.user_input = db["main"]["main_title"]
	pygame_event.need_input = True

	text_box = pg.Rect(20, 50, 440, 20)

	submit_btn = ProgramBtn(
		"Rename", 
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
		new_project_name = pygame_event.user_input

		enter = pygame_event.enter
		click_submit = submit_btn.update(pygame_event.click, mouse_pos)
		click_cancel = cancel_btn.update(pygame_event.click, mouse_pos)

		if enter or click_submit:
			if new_project_name:
				db["main"]["main_title"] = new_project_name
				json_dumper(db_path, db)
				return 0
			else:
				error_message = "Error, Please enter a project name."

		if click_cancel:
			return 0

		# Graphic

		screen.fill(grey)
		pg.draw.rect(screen, white, text_box)
		blit_text(
			screen,
			"Enter New Project Name:",
			default_font,
			white,
			(15, 20)
			)

		blit_text(
			screen,
			new_project_name,
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