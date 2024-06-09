from dataclasses import dataclass
import pygame as pg

@dataclass(slots=True, kw_only=True)
class SideBarMenu:
	rect: object
	visible: bool = False

	def draw(self, display) -> None:
		if self.visible:
			pg.draw.rect(display, pg.Color("grey10"), self.rect)

	def update(self, current_project):
		if current_project:
			self.visible = True
		else:
			self.visible = False