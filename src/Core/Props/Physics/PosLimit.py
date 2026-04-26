from config import *
from Core.Props.BaseProp import BaseProp

@attr.define
class PosLimit(BaseProp):
	xLimit: glm.vec2 = attr.field(default=None)
	yLimit: glm.vec2 = attr.field(default=None)
	zLimit: glm.vec2 = attr.field(default=None)
	