from config import *

from Core.Props.Transf import Transf
from Core.Props.Coll import Coll

from Core.Props.Physics.Rigidbody import Rigidbody
from Core.Props.Physics.PosLimit import PosLimit
from Core.Props.Physics.Jet import Jet

from Core.Props.Scripts import PreScript

from Core.Props.Graphics.Rend import Rend
from Core.Props.Graphics.Model import Model

class Rocket:
	@classmethod
	def construct(cls, index, pos):
		rocketkey = index.createObj(
			"rocket",
			[
				Transf(pos, glm.quat(), glm.vec3(2, 6, 2)),
				Coll(COLLCYLINDER, COLLRIGIDBODY),
				Rigidbody(60000, 0, glm.pi()/16, 0.3, suffersGravity=False),
				Jet(glm.vec3(0, 1, 0), 0),
				
				PosLimit(None, None, glm.vec2(-3, 3)),
				
				Rend(True, "texture", {"tex": "play4keeps", "uvScale": glm.vec2(8)}),
				Model("cylinder", True),
			]
		)
		rightkey = index.createObj(
			"rocket_right_handle",
			[
				Transf(
					glm.vec3(1, 0, -1),
					glm.normalize(
						glm.angleAxis(glm.pi()/4, glmh.yUnit())
						* glm.angleAxis(glm.pi()/2, glmh.zUnit())
					),
					glm.vec3(0.25, 1, 0.25),
					parent=index.get(rocketkey)[Transf]
				),
				Coll(COLLCYLINDER, COLLGHOST),
				
				Rend(True, "texture", {"tex": "tesseract", "uvScale": glm.vec2(1)}),
				Model("cylinder", True)
			]
		)
		leftkey = index.createObj(
			"rocket_left_handle",
			[
				Transf(
					glm.vec3(-1, 0, -1),
					glm.normalize(
						glm.angleAxis(-glm.pi()/4, glmh.yUnit())
						* glm.angleAxis(-glm.pi()/2, glmh.zUnit())
					),
					glm.vec3(0.25, 1, 0.25),
					parent=index.get(rocketkey)[Transf]
				),
				Coll(COLLCYLINDER, COLLGHOST),
				
				Rend(True, "texture", {"tex": "tesseract", "uvScale": glm.vec2(1)}),
				Model("cylinder", True)
			]
		)
		index.createObj(
			"rocket_tip",
			[
				Transf(
					glm.vec3(0, 4, 0), glm.quat(), glm.vec3(1, 1, 1),
					parent=index.get(rocketkey)[Transf]
				),
				
				Rend(True, "unLitTexture", {"tex": "eyeball", "uvScale": glm.vec2(1)}),
				Model("pyr", False)
			]
		)
		
		return (rocketkey, rightkey, leftkey)
	