from config import *
from Core.Props.BaseProp import BaseProp

@attr.define
class Text(BaseProp):
	string: str
	font: str
	