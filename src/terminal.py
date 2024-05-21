try:
	from os import startfile as openfolder
except ImportError:
	pass

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

	def open_folder(self, path) -> None:
		if self.os == "Linux":
			self.command(f"open {path}")
		elif self.os == "Windows":
			openfolder(path)