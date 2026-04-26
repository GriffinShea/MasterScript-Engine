from config import *
from System.Controller import Controller
from System.Engine import Engine
from System.Renderer import Renderer

from Core.StateTypes import Container

from Project.States.Quit import Quit
import Project.States.AstroGame#to avoid circular import
import Project.States.AstroStart#to avoid circular import

class AstroPause(Container):
	def draw(self):
		#draw the paused game
		super().draw()
		
		#blur screen
		Renderer.drawFrameEffect("normalizeColour", {})
		Renderer.drawFrameEffect("fullBlurFrame", {})
		
		#render pause controls
		Renderer.drawText(
			"[PAUSE]\n\nPAUSESCREEN\nRETURN --> MAIN MENU\nESCAPE --> RESUME\nDELETE --> CLOSE",
			"basicText",
			"fancyFont",
			{
				"colour": WHITE,
				"alpha": 1,
				"depth": 0,
				"transfMat": glm.scale(
					glm.translate(glm.mat4(), glm.vec3(-1, 1, 0)),
					glm.vec3(2)
				)
			}
		)
		return
	
	def update(self):
		#delete --> close
		if Controller.handleKey("QUIT", DOWN):
			return Quit()
		#return --> back to main menu
		if Controller.handleKey("ENTER", DOWN):
			Engine.unloadResources("sample")
			return Project.States.AstroStart.AstroStart()#to avoid circular import
		#escape --> back to game
		if Controller.handleKey("EXIT", DOWN):
			return Project.States.AstroGame.AstroGame(self.containedState)#to avoid circular import
			
		#no input --> stay in pause
		return self