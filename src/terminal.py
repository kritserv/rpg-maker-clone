try:
	from os import startfile as file_explorer
except ImportError:
	pass

from subprocess import call
from platform import system
from os import makedirs

class Terminal:
	def __init__(self):
		self.os = system()

	def command(self, comm) -> None:
		call(f"{comm}", shell=True)

	def open_folder(self, path) -> None:
		if self.os == "Linux":
			self.command(f"xdg-open {path}")

		elif self.os == "Windows":
			path = path.replace("/", "\\")
			file_explorer(path)

	def open_project_folder(self, current_project) -> None:
		path = f"projects/{current_project}"
		self.open_folder(path)