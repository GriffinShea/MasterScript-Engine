from config import *

from Core.StateTypes import Lossy
from Core.Index import Index
from Core.Canvas import Canvas

from System.Controller import Controller
from System.Engine import Engine

from Core.MasterScript import MasterScript

from Core.Props.Transf import Transf
from Core.Props.Graphics.Rend import Rend

from Project.Script.Setup.Lvl1 import setup

from Project.States.Quit import Quit
from Project.States.AstroPause import AstroPause
from Project.States.Astro1T2 import Astro1T2

class AstroLvl1(Lossy):
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
		#delete --> close
		if Controller.handleKey("QUIT", DOWN):
			return Quit()
		#escape --> pause menu
		if Controller.handleKey("EXIT", DOWN):
			return AstroPause(self)
		
		#handle controls, then run simulator, then check objectives
		self.handleControls()
		MasterScript.run(self.index, Engine.dTime)
		
		#if two the player has both hands on the rocket and 3 seconds have elapsed, go to level 2
		if self.checkObjective():
			return Astro1T2(self)
			
		return self

	def handleControls(self):
		if self.index.var.handsOnRocket < 2:
			ragdollTorso = self.index.get(self.index.var.astronautkeys["torso"])
			self.index.var.sinceLastColl = self.index.var.sinceLastColl + Engine.dTime
			ragdollTorso[Transf].setRpos(glm.vec3(
				ragdollTorso[Transf].cpos.x + Engine.dTime * (
					(Controller.checkKey("DIR_E") > 0) - (Controller.checkKey("DIR_W") > 0)
				),
				ragdollTorso[Transf].cpos.y,
				ragdollTorso[Transf].cpos.z
			))
		return

	def checkObjective(self):
		if self.index.var.handsOnRocket == 2:
			self.index.get(self.index.var.centerText)[Rend].visible = True
			self.index.var.swapTimer = self.index.var.swapTimer + Engine.dTime
			if self.index.var.swapTimer > 3:
				self.index.get(self.index.var.centerText)[Rend].visible = False
				return True
		return False
	
