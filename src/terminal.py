from subprocess import call
from platform import system

class Terminal:
	def __init__(self):
		self.os = system()

	def command(self, comm):
		call(comm, shell=True)

	def clear(self):
		if self.os == "Linux":
			self.command("clear")
		elif self.os == "Windows":
			self.command("cls")

	def run_project(self):
		self.command("cd src/start_project && python main.py")