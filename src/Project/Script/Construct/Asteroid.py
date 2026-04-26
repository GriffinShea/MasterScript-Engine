from config import *

from Core.Props.Transf import Transf
from Core.Props.Coll import Coll
from Core.Props.Field import Field
from Core.Props.Physics.Rigidbody import Rigidbody
from Core.Props.Physics.PosLimit import PosLimit
from Core.Props.Timer import Timer
from Core.Props.Scripts import PreScript, PostScript

from Core.Props.Graphics.Rend import Rend
from Core.Props.Graphics.Model import Model
from Core.Props.Graphics.ParticleEffect import ParticleEffect

from Core.Systems.Physics.rb import rb

class Asteroid:
	@classmethod
	def construct(cls, index, pos, iniVel):
		texture = [
			"die",
			"eyeball",
			"tesseract",
			"dolphinWireframe",
			"play4keeps",
			"swimcity",
			"purpleWall",
			"stoneWall"
		][random.randint(0, 7)]
		shape = random.randint(0, 2)
		size = 10+random.random()*10
		mesh = [
			"asteroid1", "asteroid2", "asteroid3", "asteroid4", "asteroid5"
		][random.randint(0, 4)]
		mass = size*3000
		
		key = index.createObj(
			"asteroid",
			[
				Transf(pos, glm.quat(), glm.vec3(size)),
				Coll(
					[COLLSPHERE, COLLSPHERE, COLLSPHERE][shape],
					COLLRIGIDBODY, tags=set(["grappleable"])
				),
				Rigidbody(
					mass, 0.5, 3*glm.pi()/8, 0.8,
					iniVel=iniVel,
					iniWel=glmh.rotVecToQuat(glmh.randVec3()/16),
					suffersGravity=False
				),
				PosLimit(None, None, glm.vec2(-3, 3)),
				Timer(iniVel.y * 4, deleteOnCycle=True),
				
				Rend(True, "texture", {"tex": texture, "uvScale": glm.vec2(1)}),
				Model(
					["sphere", "sphere", "sphere"][shape]
				, True),
				
			]
		)
		index.addProp(key, PreScript(cls.explodeOnTimerClick))
		return
	@classmethod
	def explodeOnTimerClick(cls, obj, index):
		if obj[Timer].click:
			transf = obj[Transf]
			index.createObj(
				"explosion",
				[
					Transf(transf.cpos, transf.cori, 4 * transf.scale),
					Coll(COLLSPHERE, COLLGHOST),
					Field(),
					PostScript(cls.explosionEventClosure(obj[Rigidbody].mass)),
					
					Timer(2, deleteOnCycle=True),
					Rend(True, "explosion", {"time": None}),
					ParticleEffect(int(obj[Rigidbody].mass / 500), pointSize=2),
				]
			)
		return
	@classmethod
	def explosionEventClosure(cls, p):
		return lambda o, i: cls.explosionEvent(o, i, p)
	@staticmethod
	def explosionEvent(obj, index, power):
		for key in obj[Field].keys:
			other = index.get(key)
			if (
				Rigidbody in other
			):
				body = other[Rigidbody]
				delta = other[Transf].cpos - obj[Transf].cpos
				distance = glm.length(delta)
				norm = glm.normalize(delta)
				radius = obj[Transf].scale.x * 2	#i.e. sphere radius
				force = power * (1 - pow(distance / radius, 2))
				impulse = force * norm
				rb.applyImpulse(body, other[Transf], impulse, other[Transf].cpos)
		
		index.deleteProp(obj.key, PostScript)
		
		return
	