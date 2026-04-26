from config import *
from System.Controller import Controller

from Core.StateTypes import Container

from Project.States.Quit import Quit
from Project.States.AstroPause import AstroPause
import Project.States.AstroStart#to avoid circular import

class AstroGame(Container):
	def update(self):
		#delete --> close
		if Controller.handleKey("QUIT", DOWN):
			return Quit()
		#escape --> pause menu
		if Controller.handleKey("EXIT", DOWN):
			return AstroPause(self.containedState)
		
		newState = self.containedState.update()
		if newState != self.containedState:
			return AstroGame(newState)
		
		return self
	