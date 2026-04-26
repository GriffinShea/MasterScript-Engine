from config import *
from System.Engine import Engine
from Project.Script.Construct.Spawner import Spawner
from Core.Systems.Physics.rb import rb

from Core.Props.Transf import Transf
from Core.Props.Scripts import PostScript
from Core.Props.Graphics.Text import Text
from Core.Props.Physics.Rigidbody import Rigidbody

def setup(index):
	
	objsToDelete = index.findObjs("spawner") + index.findObjs("arrow")
	for obj in objsToDelete:
		obj[Transf].delete = True
	for i in range(-4, 5, 1):
		Spawner.construct(
			index,
			"lvl2_spawner", 
			glm.vec3(i*20, 200, 0),
			glm.angleAxis(glm.radians(180), glmh.zUnit()),
			1
		)
	
	index.var.playerCrash = False
	print(index.get(index.var.rocketkey).propsToStr())
	print(vars(index.var))
	
	infoText = index.get(index.var.infoText)
	infoText[Text].string = "SURVIVE!!!\nSPEED: "
	print(infoText[Text].string)
	infoText[PostScript].run = infoTextScript
	index.var.survivalTime = 0
	
	return

def infoTextScript(obj, index):
	index.var.survivalTime = index.var.survivalTime + Engine.dTime
	vel = glm.length(rb.calcVel(
		index.get(index.var.astronautkeys["torso"])[Rigidbody],
		index.get(index.var.astronautkeys["torso"])[Transf]
	))
	vel = 0 if glm.isnan(vel) else vel
	index.var.speedHistory.append(vel)
	if len(index.var.speedHistory) == 10:
		index.var.avgSpeed = str(round(sum(index.var.speedHistory) / 10))
		index.var.speedHistory = []
	
	obj[Text].string = "SURVIVAL TIME: "+str(int(index.var.survivalTime*100)/100)+"s\nSPEED: "+index.var.avgSpeed+"m/s"
	return