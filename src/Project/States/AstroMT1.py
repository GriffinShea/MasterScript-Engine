from config import *

from Core.StateTypes import Screen

from System.Renderer import Renderer

from Project.States.AstroLvl1 import AstroLvl1

class AstroMT1(Screen):
	def draw(self):
		Renderer.drawText(
			"[LOADING LEVEL 1]",
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
		return AstroLvl1()
	