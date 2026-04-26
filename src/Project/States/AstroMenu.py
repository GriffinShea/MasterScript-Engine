from config import *

from Core.StateTypes import Lossy
from Core.Canvas import Canvas
from Core.Index import Index
from Core.MasterScript import MasterScript

from System.Controller import Controller
from System.Engine import Engine

from Project.States.Quit import Quit
from Project.States.AstroGame import AstroGame
from Project.States.AstroMT1 import AstroMT1

from Project.Script.Setup.Menu import setup

class AstroMenu(Lossy):
	def __init__(self):
		canvas = Canvas(
			glm.vec3(0.55, 0.65, 0.75) / 8,
			glm.vec3(0.01),
			glm.vec2(0, 1)
		)
		index = Index()
		camerakey = setup(index)
		super().__init__(canvas, index, camerakey)
		
		return
	
	def update(self):
		#return --> start level 1
		if Controller.handleKey("ENTER", DOWN):
			return AstroGame(AstroMT1())
			#return AstroMT1()
		
		#escape --> quit
		if Controller.handleKey("EXIT", DOWN) or Controller.handleKey("QUIT", DOWN):
			return Quit()
		
		#no action --> stay in menu
		MasterScript.run(self.index, Engine.dTime)
		return self
	
