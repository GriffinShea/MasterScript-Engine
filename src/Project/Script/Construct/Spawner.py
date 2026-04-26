from config import *

from Core.Props.Transf import Transf
from Core.Props.Timer import Timer
from Core.Props.Scripts import PreScript

from Project.Script.Construct.Asteroid import Asteroid

class Spawner:
	@classmethod
	def construct(cls, index, key, pos, ori, velocity):
		return index.createObj(key, [
			Transf(pos, ori, glm.vec3()),
			Timer(4, time=random.random()),
			PreScript(cls.spawnerPreScriptClosure(glm.vec2(pos.x, pos.y), velocity))
		])
	@classmethod
	def spawnerPreScriptClosure(cls, offsetXY, velocity):
		return lambda o, i: cls.spawnerPreScript(o, i, offsetXY, velocity)
	@staticmethod
	def spawnerPreScript(obj, index, offsetXY, velocity):
		#move spawner to follow player
		torsoTransf = index.get(index.var.astronautkeys["torso"])[Transf]
		obj[Transf].setRpos(glm.vec3(
			torsoTransf.cpos.x + offsetXY.x,
			torsoTransf.cpos.y + offsetXY.y,
			0
		))
		#on timer, throw an asteroid
		if obj[Timer].click:
			transf = obj[Transf]
			Asteroid.construct(
				index,
				obj[Transf].cpos,
				transf.cori * velocity * glm.vec3(
					(random.random() - 0.5),
					(8+random.random()*16)/12,
					(random.random() - 0.5)
				)
			)
		return
	
	