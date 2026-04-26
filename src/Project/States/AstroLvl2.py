from config import *
from System.Controller import Controller
from System.Engine import Engine

from Core.StateTypes import Lossless
from Core.MasterScript import MasterScript

from Project.Script.Setup.Lvl2 import setup

from Core.Props.Transf import Transf

from Project.States.Quit import Quit
from Project.States.AstroPause import AstroPause
import Project.States.AstroStart#to avoid circular import

class AstroLvl2(Lossless):
	def __init__(self, prevState):
		setup(prevState.index)
		super().__init__(prevState)
		return
	
	def update(self):
		#handle controls, then run simulator, then check objectives
		self.handleControls()
		MasterScript.run(self.index, Engine.dTime)
		
		#if two the player has both hands on the rocket and 3 seconds have elapsed, go to level 2
		if self.index.var.playerCrash:
			return Project.States.AstroStart.AstroStart()#to avoid circular import
			
		return self
	
	def handleControls(self):
		rocketTransf = self.index.get(self.index.var.rocketkey)[Transf]
		self.index.get(self.index.var.rocketSteer)[Transf].setRpos(glm.vec3(
			rocketTransf.cpos.x+32*((Controller.checkKey("DIR_E")>0)-(Controller.checkKey("DIR_W")>0)),
			rocketTransf.cpos.y+32*((Controller.checkKey("DIR_N")>0)-(Controller.checkKey("DIR_S")>0)),
			rocketTransf.cpos.z
		))
		return
	