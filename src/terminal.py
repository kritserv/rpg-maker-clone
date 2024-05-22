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

	def open_folder(self, current_project) -> None:
		if self.os == "Linux":
			try:
				self.command(f"open projects/{current_project}")
			except:
				try:
					self.command(f"xdg-open projects/{current_project}")
				except:
					raise OSError("I don't know what command you used to open your file manager. :)")
		elif self.os == "Windows":
			openfolder(f"projects\\{current_project}")