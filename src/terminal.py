from dataclasses import dataclass
from platform import system
try:
	from os import startfile as file_explorer
except ImportError:
	pass
from subprocess import call
from os import makedirs

@dataclass(slots=True, frozen=True, kw_only=True)
class Terminal:
	os: str = system()
	venv_dir_exist: bool

	def command(self, comm, need_venv=False) -> None:
		if need_venv and self.venv_dir_exist:
			if self.os == "Linux":
				comm = "source venv/bin/activate &&" + comm
			elif self.os == "Windows":
				comm = "venv\\Scripts\\activate.bat &&" + comm
		try:
			call(f"{comm}", shell=True)
		except Exception as e:
			print(e.message)

	def open_folder(self, path) -> None:
		if self.os == "Linux":
			self.command(f"xdg-open {path}")

		elif self.os == "Windows":
			path = path.replace("/", "\\")
			file_explorer(path)

	def open_project_folder(self, current_project) -> None:
		path = f"projects/{current_project}"
		self.open_folder(path)