from subprocess import call
from platform import system
from os import makedirs

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