import tkinter as tk
from tkinter import messagebox
from os import listdir
from pathlib import Path

def open_project(project_name):
	state = f"working_state/workonproject_{project_name}"
	Path(state).touch()
	root.destroy()

root = tk.Tk()
root.geometry("360x120")

projects_folder = "projects/"
projects = listdir(projects_folder)

if not projects:
	messagebox.showerror("Error", "No projects found in the projects folder.")
else:
	for project in projects:
		project_button = tk.Button(root, text=project, command=lambda project=project: open_project(project))
		project_button.pack(fill=tk.X)

cancel_button = tk.Button(root, text="Cancel", command=root.destroy)
cancel_button.pack(side=tk.BOTTOM, anchor="e")

if projects:
	root.mainloop()
