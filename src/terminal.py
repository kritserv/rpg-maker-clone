from subprocess import call
from platform import system
from os import makedirs
from distutils.dir_util import copy_tree

class Terminal:
	def __init__(self):
		self.os = system()

	def command(self, comm) -> None:
		call(comm, shell=True)

	def clear(self) -> None:
		if self.os == "Linux":
			self.command("clear")
		elif self.os == "Windows":
			self.command("cls")

	def create_project_from_start_project(self, project_name) -> None:
		makedirs("projects", exist_ok=True)
		copy_tree("src/start_project", f"projects/{project_name}")

	def run_project(self) -> None:
		self.command("cd src/start_project && python main.py")