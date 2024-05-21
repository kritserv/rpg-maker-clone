import pygame as pg

pg.init()

from sys import exit

win_size = (360, 120)

screen = pg.display.set_mode(
	(win_size)
	)

from src import PygameEvent, blit_text
from os import path
from pathlib import Path
from distutils.dir_util import copy_tree

def create_and_open() -> None:
	project_name = entry.get()
	if not project_name:
		messagebox.showerror("Error", "Please enter a project name.")
		return
	if not path.isdir(f"projects/{project_name}"):
		state = f"working_state/workonproject_{project_name}"
		Path(state).touch()
		root.destroy()
	else:
		messagebox.showerror("Error", "Project with that name already exists.")

def main():
	pg.display.set_caption("Create New Project")
	default_font = pg.font.Font(
		"assets/fonts/IBMPlexSans-Regular.ttf",
		13
		)
	black = pg.Color("black")
	white = pg.Color("White")

	clock = pg.time.Clock()

	pygame_event = PygameEvent()

	while pygame_event.running:

		clock.tick(60)

		# Input

		mouse_pos = pg.mouse.get_pos()
		print(mouse_pos)
		pygame_event.check()

		# Graphic

		screen.fill(black)
		blit_text(
			screen,
			"test",
			default_font,
			white,
			(0, 0)
			)

		pg.display.update()

	pg.quit()
	exit()

if __name__ == "__main__":
	try:
		main()
	except FileNotFoundError:
		print("Error: Program need to be running from root directory.")
		pass

'''
root = tk.Tk()
root.minsize(360, 120)
root.title("Create New Project")

label = tk.Label(root, text="Enter Project Name:")
label.pack()

entry = tk.Entry(root)
entry.pack()

button_frame = tk.Frame(root)
button_frame.pack()

create_button = tk.Button(button_frame, text="Create & Open", command=create_and_open)
create_button.pack()

cancel_frame = tk.Frame(root)
cancel_frame.pack(side=tk.BOTTOM, fill=tk.X)

cancel_button = tk.Button(cancel_frame, text="Cancel", command=root.destroy)
cancel_button.pack(side="right")

root.mainloop()
'''