from os import listdir, makedirs, remove
from distutils.dir_util import copy_tree

class MenuFunc:
	def __init__(self):
		self.current_project_name = ""
		self.func = {
			"New project (Ctrl + N)": 0, "new_project": 0,
			"Open project (Ctrl + O)": 1, "open_project": 1,
			"Close project": 2,
			"Save Project (Ctrl + S)": 3, "save_project": 3,
			"Exit (Ctrl + Q)": 4,
			"Undo (Ctrl + Z)": 5, "undo": 5,
			"Cut (Ctrl + Z)": 6, "cut": 6,
			"Copy (Ctrl + C)": 7, "copy": 7,
			"Paste (Ctrl + V)": 8, "paste": 8,
			"Delete (Del)": 9, "delete": 9,
			"Current and Below (F2)": 10,
			"All Layers (F3)": 11,
			"Dim Other Layers (F4)": 12,
			"Layer 1 (F5)": 13, "layer_1": 13,
			"Layer 2 (F6)": 14, "layer_2": 14,
			"Layer 3 (F7)": 15, "layer_3": 15,
			"Events (F8)": 16, "events": 16,
			"Pencil": 17, "pencil": 17,
			"Rectangle": 18, "rectangle": 18,
			"Eclipse": 19, "eclipse": 19,
			"Flood Fill": 20, "flood_fill": 20,
			"Select": 21, "select": 21,
			"1:1": 22, "1to1": 22,
			"1:2": 23, "1to2": 23,
			"1:4": 24, "1to4": 24,
			"Database (F9)": 25, "database": 25,
			"Options": 26,
			"Play Test (F12)": 27, "play_test": 27,
			"Change Title": 28,
			"Open Game Folder": 29
		}
		self.current_tool = "pencil"
		self.current_mode = {
			"current_and_below": False,
			"all_layer": True,
			"dim_others_layer": True,
		}
		self.current_layer = 1
		self.zoom_level = 1.00

	def exec_func(self, func_id, terminal) -> int or None:
		if func_id == 0:
			self.new_project(terminal)
		elif func_id == 1:
			self.open_project(terminal)
		elif func_id == 2: #close project
			pass
		elif func_id == 3: #save project
			pass
		elif func_id == 4:
			return 0
		elif func_id == 5: #undo
			pass
		elif func_id == 6: #cut
			pass
		elif func_id == 7: #copy
			pass
		elif func_id == 8: #paste
			pass
		elif func_id == 9: #delete
			pass
		elif func_id == 10:
			self.current_mode["current_and_below"] = True
			self.current_mode["all_layer"] = False
		elif func_id == 11:
			self.current_mode["current_and_below"] = False
			self.current_mode["all_layer"] = True
		elif func_id == 12:
			if self.current_mode["dim_others_layer"] == True:
				self.current_mode["dim_others_layer"] = False
			else:
				self.current_mode["dim_others_layer"] = True
		elif func_id == 13:
			self.current_layer = 1
		elif func_id == 14:
			self.current_layer = 2
		elif func_id == 15:
			self.current_layer = 3
		elif func_id == 16:
			terminal.command("echo event")
		elif func_id == 17:
			self.current_tool = "pencil"
		elif func_id == 18:
			self.current_tool = "rectangle"
		elif func_id == 19:
			self.current_tool = "eclipse"
		elif func_id == 20:
			self.current_tool = "flood_fill"
		elif func_id == 21:
			self.current_tool = "select"
		elif func_id == 22:
			self.zoom_level = 1.0
		elif func_id == 23:
			self.zoom_level = 0.5
		elif func_id == 24:
			self.zoom_level = 0.25
		elif func_id == 25: #database
			pass
		elif func_id == 26: #options
			pass
		elif func_id == 27: #test
			terminal.command("cd src/start_project && python main.py")
		elif func_id == 28: #change title
			pass
		elif func_id == 29:
			self.open_game_folder(terminal)
		return None

	def mkdir(self, dir_name) -> None:
		makedirs(dir_name, exist_ok=True)

	def project_has_opened(self) -> bool:
		return self.current_project_name != ""

	def get_working_project(self) -> str or None:
		for filename in listdir("working_state"):
			if "workonproject" in filename:
				project_name = filename.split("workonproject_")[1]
				return project_name

	def new_project(self, terminal) -> None:
		self.mkdir("working_state")
		self.mkdir("projects")
		terminal.command("python src/sub_program/new_project.py")

		project_name = self.get_working_project()

		if project_name:
			copy_tree(
				"src/start_project", f"projects/{project_name}"
				)
			self.current_project_name = project_name
			remove(f"working_state/workonproject_{project_name}")

	def open_project(self, terminal) -> None:
		self.mkdir("working_state")
		self.mkdir("projects")
		terminal.command("python src/sub_program/open_project.py")
		
		project_name = self.get_working_project()

		if project_name:
			self.current_project_name = project_name
			remove(f"working_state/workonproject_{project_name}")

	def open_game_folder(self, terminal) -> None:
		path = f"projects/{self.current_project_name}"
		terminal.open_folder(path)

	def get_func_id(self, clicked_menu) -> int:
		return self.func[clicked_menu]

	def update(self, clicked_menu, terminal) -> int or None:
		return_value = None
		if clicked_menu:
			func_id = self.get_func_id(clicked_menu)
			need_project = func_id not in [0, 1, 4]
			if need_project:
				if self.project_has_opened():
					return_value = self.exec_func(func_id, terminal)
			else:
				return_value = self.exec_func(func_id, terminal)
		return return_value