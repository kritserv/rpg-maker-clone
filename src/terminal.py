from subprocess import call
from platform import system

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

	def run_project(self) -> None:
		self.command("cd src/start_project && python main.py")