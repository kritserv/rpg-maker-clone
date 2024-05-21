from os import path
import tkinter as tk
from tkinter import messagebox
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
create_button.pack(side="left")

cancel_button = tk.Button(button_frame, text="Cancel", command=root.destroy)
cancel_button.pack(side="right")

root.mainloop()
