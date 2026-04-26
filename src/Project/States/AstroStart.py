import glm

from Core.StateTypes import Screen

from System.Renderer import Renderer

from Project.States.AstroMenu import AstroMenu

class AstroStart(Screen):
	def draw(self):
		Renderer.drawText(
			"STARTING ASTROSURFER",
			"basicText",
			"basicFont",
			{
				"colour": glm.vec3(1),
				"alpha": 1,
				"depth": 0,
				"transfMat": glm.scale(
					glm.translate(glm.mat4(), glm.vec3(-1, 1, 0)),
					glm.vec3(4)
				)
			}
		)
		return
	
	def update(self):
		return AstroMenu()
