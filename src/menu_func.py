from dataclasses import dataclass, field
from os import listdir, makedirs
from distutils.dir_util import copy_tree
from pathlib import Path
from .output_file import write_line_to_file, read_line_from_file
from .load_json import json_loader

@dataclass(slots=True)
class MenuFunc:
	current_project_name: str = ""
	func: dict[str, str] = field(
		default_factory=lambda: ({
			"New project (Ctrl + N)": "self.new_project(terminal, rpgmap)", "new_project": "self.new_project(terminal, rpgmap)",
			"Open project (Ctrl + O)": "self.open_project(terminal, rpgmap)", "open_project": "self.open_project(terminal, rpgmap)",
			"Close project": "self.close_project(rpgmap)",
			"Save Project (Ctrl + S)": "pass", "save_project": "pass",
			"Undo (Ctrl + Z)": "pass", "undo": "pass",
			"Cut (Ctrl + X)": "pass", "cut": "pass",
			"Copy (Ctrl + C)": "pass", "copy": "pass",
			"Paste (Ctrl + V)": "pass", "paste": "pass",
			"Delete (Del)": "pass", "delete": "pass",
			"Current and Below (F2)": "self.change_current_mode((('current_and_below', True), ('all_layer', False)))",
			"All Layers (F3)": "self.change_current_mode((('current_and_below', False), ('all_layer', True)))",
			"Dim Other Layers (F4)": "self.change_current_mode((('dim_others_layer', 'toggle')))",
			"Layer 1 (F5)": "self.current_layer = 1", "layer_1": "self.current_layer = 1",
			"Layer 2 (F6)": "self.current_layer = 2", "layer_2": "self.current_layer = 2",
			"Layer 3 (F7)": "self.current_layer = 3", "layer_3": "self.current_layer = 3",
			"Events (F8)": "pass", "events": "pass",
			"Pencil": "self.current_tool = 'pencil'", "pencil": "self.current_tool = 'pencil'",
			"Rectangle": "self.current_tool = 'rectangle'", "rectangle": "self.current_tool = 'rectangle'",
			"Ellipse": "self.current_tool = 'ellipse'", "ellipse": "self.current_tool = 'ellipse'",
			"Flood Fill": "self.current_tool = 'flood_fill'", "flood_fill": "self.current_tool = 'flood_fill'",
			"Select": "self.current_tool = 'select'", "select": "self.current_tool = 'select'",
			"1:1": "self.zoom_level = 1.0", "1to1": "self.zoom_level = 1.0",
			"1:2": "self.zoom_level = 0.5", "1to2": "self.zoom_level = 0.5",
			"1:4": "self.zoom_level = 0.25", "1to4": "self.zoom_level = 0.25",
			"Database (F9)": "pass", "database": "pass",
			"Options": "pass",
			"Play Test (F12)": "self.play_test(terminal)", "play_test": "self.play_test(terminal)",
			"Change Title": "self.change_title(terminal)",
			"Open Game Folder": "self.open_game_folder(terminal)"
		})
		)
	current_tool: str = "pencil"
	current_mode: dict[str, bool] = field(
		default_factory=lambda: ({
		"current_and_below": False,
		"all_layer": True,
		"dim_others_layer": True,
		})
		)
	current_layer: int = 1
	zoom_level: float = 1.00

	def mkdir(self, dir_name) -> None:
		makedirs(dir_name, exist_ok=True)

	def make_working_dir(self) -> None:
		self.mkdir("working_state")
		self.mkdir("projects")
		state = "working_state/work_on_project"
		Path(state).touch()
		write_line_to_file("", "working_state/work_on_project")
		state = "working_state/last_open_project"
		Path(state).touch()

	def project_has_opened(self) -> bool:
		return self.current_project_name != ""

	def get_working_project(self) -> str or None:
		for filename in listdir("working_state"):
			if "work_on_project" in filename:
				project_name = read_line_from_file("working_state/work_on_project")
				if project_name:
					return project_name
		return None

	def set_project_to_working_state(self, project_name, rpgmap):
		try:
			self.current_project_name = project_name
			write_line_to_file("", "working_state/work_on_project")
			write_line_to_file(project_name, "working_state/last_open_project")
			db = json_loader(f"projects/{project_name}/game_data/db.json")
			rpgmap.load_map_data(db["maps"], project_name)
		except:
			pass

	def new_project(self, terminal, rpgmap) -> None:
		self.make_working_dir()
		terminal.command("python src/sub_program/new_project.py")

		project_name = self.get_working_project()

		if project_name:
			copy_tree(
				"src/start_project", f"projects/{project_name}"
				)
			self.set_project_to_working_state(project_name, rpgmap)

	def open_project(self, terminal, rpgmap) -> None:
		self.make_working_dir()
		terminal.command("python src/sub_program/open_project.py")
		
		project_name = self.get_working_project()

		if project_name:
			self.set_project_to_working_state(project_name, rpgmap)

	def close_project(self, rpgmap) -> None:
		self.current_project_name = ""
		rpgmap.map_data = {}

	def change_current_mode(self, changes) -> None:
		for mode_name, change in changes:
			if change == "toggle":
				self.current_mode[mode_name] = not self.current_mode[mode_name]
			else:
				self.current_mode[mode_name] = change

	def play_test(self, terminal) -> None:
		terminal.command(f"cd projects/{self.current_project_name} && python main.py")

	def change_title(self, terminal) -> None:
		terminal.command("python src/sub_program/change_title.py")

	def open_game_folder(self, terminal) -> None:
		terminal.open_project_folder(self.current_project_name)

	def get_func(self, clicked_menu) -> int:
		return self.func[clicked_menu]

	def update(self, clicked_menu, terminal, rpgmap) -> int or None:
		return_value = None
		if clicked_menu:
			if clicked_menu == "Exit (Ctrl + Q)":
				return 0
			func = self.get_func(clicked_menu)
			need_project = func not in set((
				"self.new_project(terminal, rpgmap)", 
				"self.open_project(terminal, rpgmap)"
				))
			if need_project:
				if self.project_has_opened():
					exec(func)
			else:
				exec(func)
		return return_value