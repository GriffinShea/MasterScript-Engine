from config import *

from Core.StateTypes import Lossless
from Core.Painter import Painter

from System.Renderer import Renderer

from Project.States.AstroLvl2 import AstroLvl2

class Astro1T2(Lossless):
	def draw(self):
		super().draw()
		
		Renderer.drawText(
			"[LOADING LEVEL 2]",
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
		return AstroLvl2(self)
	