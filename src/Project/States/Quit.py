import glm
from System.Renderer import Renderer
from Core.StateTypes import Screen

class Quit(Screen):
	def draw(self):
		Renderer.drawText(
			"CLOSING ENGINE",
			"basicText",
			"fancyFont",
			{
				"colour": glm.vec3(1),
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
		return None
