from config import *

from Core.Props.Transf import Transf
from Core.Props.Coll import Coll
from Core.Props.Physics.Rigidbody import Rigidbody
from Core.Props.Physics.PosLimit import PosLimit
from Core.Props.Physics.PhysJoint import PhysJoint

from Core.Props.Graphics.Rend import Rend
from Core.Props.Graphics.Model import Model

from Core.Props.Graphics.Lights import Light
from Core.Props.Graphics.Lights import SpotLight
from Core.Props.Graphics.Lights import PointLight

class Astronaut:
	BASEMASS = 10
	PHI = glm.pi()/16
	MEW = 0.3
	
	@classmethod
	def construct(cls, index, key, pos, ori, scale, suffersGravity):
		keys = {}
		keys["torso"] = index.createObj(
			key+"_torso",
			[
				Transf(pos, ori, scale * glm.vec3(0.3, 0.24, 0.3)),
				Coll(COLLCAPSULE, COLLRIGIDBODY),
				Rigidbody(77 * scale * cls.BASEMASS, 0, cls.PHI, cls.MEW, suffersGravity=suffersGravity),
				PosLimit(None, None, glm.vec2(-3, 3))
			]
		)
		_ = cls.makeModelSon(
			index, keys["torso"],
			glm.vec3(0, -0.85, 0),
			scale, "astronauta_torso"
		)
		
		keys["head"] = cls.makeAndJointPart(
			index, keys["torso"], key+"_head", scale, 12.6, COLLSPHERE, glm.vec3(0.25),
			glm.vec3(0, 0.275, 0), glm.vec3(0, -0.125, 0),
			glm.quat(), glm.vec3(70, 90, 30), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["head"],
			glm.vec3(0, -1.225, 0),
			scale, "astronauta_reloded_head"
		)
		index.get(keys["head"])[Coll].ignoreKeys.add(keys["torso"])
		lightkey = index.createObj(
			key+"_spotlight",
			[
				Transf(
					glm.vec3(0, 0, 5), glm.quat(), glm.vec3(0.25),
					parent=index.get(keys["head"])[Transf]
				),
				Light(glm.vec3(1, 1, 0.25), 1/2),
				#PointLight(),
				SpotLight(glmh.zUnit(), glm.vec2(30, 90)),
			]
		)
		
		#arms
		keys["leftarm"] = cls.makeAndJointPart(
			index, keys["torso"], key+"_leftarm", scale, 4.3, COLLCAPSULE, glm.vec3(0.1, 0.15, 0.1),
			glm.vec3(0.125, 0.2, -0.05), glm.vec3(0, 0.2, 0),
			glm.normalize(glm.angleAxis(glm.pi()/2, glmh.zUnit()) * glm.angleAxis(-glm.pi()/3, glmh.xUnit())),
			glm.vec3(90, 22.5, 90), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["leftarm"],
			glm.vec3(-1, -0.1, 0.05),
			scale, "astronauta_reloded_leftarm"
		)
		index.get(keys["leftarm"])[Coll].ignoreKeys.add(keys["torso"])
		
		keys["lefthand"] = cls.makeAndJointPart(
			index, keys["leftarm"], key+"_lefthand", scale, 3.4, COLLCAPSULE, glm.vec3(0.1, 0.15, 0.1),
			glm.vec3(0, -0.125, 0), glm.vec3(0, 0.125, 0),
			glm.angleAxis(-5*glm.pi()/12, glmh.xUnit()), glm.vec3(75, 0, 0), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["lefthand"],
			glm.vec3(-1, 0.15, 0.05),
			scale, "astronauta_reloded_lefthand"
		)
		index.get(keys["lefthand"])[Coll].ignoreKeys.add(keys["leftarm"])
		
		keys["rightarm"] = cls.makeAndJointPart(
			index, keys["torso"], key+"_rightarm", scale, 4.3, COLLCAPSULE, glm.vec3(0.1, 0.15, 0.1),
			glm.vec3(-0.125, 0.2, -0.05), glm.vec3(0, 0.2, 0),
			glm.normalize(glm.angleAxis(-glm.pi()/2, glmh.zUnit()) * glm.angleAxis(-glm.pi()/3, glmh.xUnit())),
			glm.vec3(90, 22.5, 90), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["rightarm"],
			glm.vec3(1, -0.1, 0.05),
			scale, "astronauta_reloded_rightarm"
		)
		index.get(keys["rightarm"])[Coll].ignoreKeys.add(keys["torso"])
		
		keys["righthand"] = cls.makeAndJointPart(
			index, keys["rightarm"], key+"_righthand", scale, 3.4, COLLCAPSULE, glm.vec3(0.1, 0.15, 0.1),
			glm.vec3(0, -0.125, 0), glm.vec3(0, 0.125, 0),
			glm.angleAxis(-5*glm.pi()/12, glmh.xUnit()), glm.vec3(75, 0, 0), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["righthand"],
			glm.vec3(1, 0.15, 0.05),
			scale, "astronauta_reloded_righthand"
		)
		index.get(keys["righthand"])[Coll].ignoreKeys.add(keys["rightarm"])
		
		#legs
		keys["leftleg"] = cls.makeAndJointPart(
			index, keys["torso"], key+"_leftleg", scale, 15.5, COLLCAPSULE, glm.vec3(0.15, 0.125, 0.15),
			glm.vec3(0.08, -0.2, 0), glm.vec3(0, 0.2125, 0),
			glm.normalize(glm.angleAxis(-glm.pi()/6, glmh.xUnit()) * glm.angleAxis(glm.pi()/6, glmh.zUnit())),
			glm.vec3(90, 75, 45), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["leftleg"],
			glm.vec3(-0.1, -0.45, 0),
			scale, "astronauta_reloded_leftleg"
		)
		index.get(keys["leftleg"])[Coll].ignoreKeys.add(keys["torso"])
		keys["leftfoot"] = cls.makeAndJointPart(
			index, keys["leftleg"], key+"_leftfoot", scale, 9.4, COLLCAPSULE, glm.vec3(0.15, 0.15, 0.15),
			glm.vec3(0, -0.125, 0), glm.vec3(0, 0.15, 0),
			glm.angleAxis(4*glm.pi()/12, glmh.xUnit()), glm.vec3(60, 0, 0), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["leftfoot"],
			glm.vec3(-0.1, -0.175, 0),
			scale, "astronauta_reloded_leftfoot"
		)
		index.get(keys["leftfoot"])[Coll].ignoreKeys.add(keys["leftleg"])
		
		keys["rightleg"] = cls.makeAndJointPart(
			index, keys["torso"], key+"_rightleg", scale, 15.5, COLLCAPSULE, glm.vec3(0.15, 0.125, 0.15),
			glm.vec3(-0.08, -0.2, 0), glm.vec3(0, 0.2125, 0),
			glm.normalize(glm.angleAxis(-glm.pi()/6, glmh.xUnit()) * glm.angleAxis(-glm.pi()/6, glmh.zUnit())),
			glm.vec3(90, 75, 60), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["rightleg"],
			glm.vec3(0.1, -0.45, 0),
			scale, "astronauta_reloded_rightleg"
		)
		index.get(keys["rightleg"])[Coll].ignoreKeys.add(keys["torso"])
		keys["rightfoot"] = cls.makeAndJointPart(
			index, keys["rightleg"], key+"_rightfoot", scale, 9.4, COLLCAPSULE, glm.vec3(0.15, 0.15, 0.15),
			glm.vec3(0, -0.125, 0), glm.vec3(0, 0.15, 0),
			glm.angleAxis(4*glm.pi()/12, glmh.xUnit()), glm.vec3(60, 0, 0), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["rightfoot"],
			glm.vec3(0.1, -0.175, 0),
			scale, "astronauta_reloded_rightfoot"
		)
		index.get(keys["rightfoot"])[Coll].ignoreKeys.add(keys["rightleg"])
		
		return keys
	
	@classmethod
	def makeAndJointPart(
		cls, index, dadkey, sonkey, scale, massMod, shape, size,
		dadOffset, sonOffset, jointOri, freedom, suffersGravity
	):
		dadTransf = index.get(dadkey)[Transf]
		jointPos = dadTransf.cpos + dadTransf.cori * dadOffset * scale
		sonkey = index.createObj(
			sonkey,
			[
				Transf(
					jointPos - glm.normalize(dadTransf.cori * jointOri) * sonOffset * scale,
					glm.normalize(dadTransf.cori * jointOri),
					scale * size
				),
				Coll(shape, COLLRIGIDBODY),
				Rigidbody(
					massMod * scale * cls.BASEMASS,
					0, cls.PHI, cls.MEW,
					suffersGravity=suffersGravity
				)
			]
		)
		_ = index.createObj(
			"joint_"+dadkey+"_"+sonkey,
			[PhysJoint(
				dadkey, sonkey,
				dadOffset * scale, sonOffset * scale,
				jointOri, freedom=freedom
			)]
		)
		return sonkey
	
	@classmethod
	def makeModelSon(cls, index, dadkey, pos, scale, mesh):
		sonkey = index.createObj(
			dadkey+"_model",
			[
				Transf(
					pos * scale, glm.quat(), glm.vec3(scale),
					parent=index.get(dadkey)[Transf]
				),
				Rend(True, "texture", {"tex": "multpaleta", "uvScale": glm.vec2(1)}),
				Model(mesh, False)
			]
		)
		return sonkey
		
	
	