import tkinter as tk
from tkinter import messagebox
from os import listdir
from pathlib import Path

def open_project(project_name) -> None:
	state = f"working_state/workonproject_{project_name}"
	Path(state).touch()
	root.destroy()

projects_folder = "projects/"
projects = listdir(projects_folder)

if not projects:
	messagebox.showerror("Error", "No projects found in the projects folder.")
else:
	root = tk.Tk()

	for project in projects:
		project_button = tk.Button(root, text=project, command=lambda project=project: open_project(project))
		project_button.pack(fill=tk.X)

	root.geometry("360x120")
	root.title("Open Project")
	cancel_button = tk.Button(root, text="Cancel", command=root.destroy)
	cancel_button.pack(side=tk.BOTTOM, anchor="e")
	root.mainloop()
