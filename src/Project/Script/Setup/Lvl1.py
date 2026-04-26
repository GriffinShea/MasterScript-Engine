from config import *
from System.Controller import Controller
from System.Engine import Engine

from Project.Script.Construct.Arrow import Arrow
from Project.Script.Construct.Spawner import Spawner
from Project.Script.Construct.Astronaut import Astronaut
from Project.Script.Construct.Rocket import Rocket

from Core.Props.Timer import Timer
from Core.Props.Transf import Transf
from Core.Props.Coll import Coll

from Core.Props.Scripts import PreScript, PostScript

from Core.Props.Physics.Rigidbody import Rigidbody
from Core.Props.Physics.Jet import Jet
from Core.Props.Physics.PhysJoint import PhysJoint
from Core.Props.Physics.PosLimit import PosLimit
from Core.Props.Physics.PIDSteer import PIDSteer
from Core.Props.Physics.Attractor import Attractor

from Core.Props.Graphics.Rend import Rend
from Core.Props.Graphics.Model import Model
from Core.Props.Graphics.Sprite import Sprite
from Core.Props.Graphics.Text import Text
from Core.Props.Graphics.Segment import Segment
from Core.Props.Graphics.Camera import Camera
from Core.Props.Graphics.ParticleEffect import ParticleEffect

from Core.Props.Graphics.Lights import Light
from Core.Props.Graphics.Lights import PointLight
from Core.Props.Graphics.Lights import DirLight

from Core.Systems.Physics.rb import rb

def setup(index):
	
	#objective for this level is to grab the rocket with both hands
	index.var.handsOnRocket = 0
	#for the camera logic
	index.var.sinceLastColl = 0
	#these two needed for HUD to display average speed
	index.var.speedHistory = []
	index.var.avgSpeed = ""
	
	#background, light, starting platform
	createScenery(index)

	#create a ragdoll (the player character)
	index.var.astronautkeys = Astronaut.construct(
		index, "ragdoll",
		glm.vec3(0, 20, 0), glm.angleAxis(glm.pi(), glmh.yUnit()), 4,
		True
	)
	
	#add camera fixed to torso, zooms out slowly, zooms in when torso hits asteroid
	camerakey = createCamera(index)

	#create the rocket
	(index.var.rocketkey, righthandlekey, lefthandlekey) = Rocket.construct(index, glm.vec3(0, 500, 0))
	
	#arrow to guide the player towards the rocket
	Arrow.construct(index, camerakey, "guide", 1, index.var.rocketkey)
	
	#add logic to attach rocket to player hands
	index.addProp(index.var.astronautkeys["lefthand"], Attractor(righthandlekey, 1000, 2, 100))
	index.get(index.var.astronautkeys["lefthand"])[Coll].postcollide = attachRocketHandle
	index.addProp(index.var.astronautkeys["righthand"], Attractor(lefthandlekey, 1000, 2, 100))
	index.get(index.var.astronautkeys["righthand"])[Coll].postcollide = attachRocketHandle
	
	#create asteroid spawners
	for i in range(-6, 7, 1):
		Spawner.construct(index, "lvl1_spawner", glm.vec3(i*16, -128, 0), glm.quat(), 1)
	
	#create three text objs for HUD
	(index.var.fpsText, index.var.infoText, index.var.centerText) = createHUD(index)
	
	return camerakey

def createScenery(index):
	#add a light
	index.createObj(
		"sun",
		[
			Transf(
				glm.vec3(0, 0, 0),
				glm.angleAxis(45, -glmh.xUnit()),
				glm.vec3()
			),
			Light(glm.vec3(0.75, 0.75, 1), 1),
			DirLight(1000, 100),
		]
	)
	#background
	index.createObj(
		"background",
		[
			Transf(glm.vec3(0, 1500, 16), glm.quat(), glm.vec3(2048, 4096, 1)),
			Rend(True, "unLitTexture", {"tex": "purpleSky", "uvScale": glm.vec2(17, 33)}),
			Model("plane", False)
		]
	)
	#platform (static)
	index.createObj(
		"platform",
		[
			Transf(glm.vec3(0, -10, 0), glm.quat(), glm.vec3(10)),
			Coll(COLLBOX, COLLTERRAIN),
			Rend(True, "texture", {"tex": "play4keeps", "uvScale": glm.vec2(1)}),
			Model("cube", True)
		]
	)
	return

def createCamera(index):
	camerakey = index.createObj(
		index.var.astronautkeys["torso"]+"_camera",
		[
			Transf(glm.vec3(0, 0, -32), glm.quat(), glm.vec3(0.1)),
			Camera(100),
			PostScript(fixCameraPos),
			Light(glm.vec3(1, 1, 0.8), 1/3),
			PointLight(),
		]
	)
	index.get(index.var.astronautkeys["torso"])[Coll].postcollide = resetTimer
	return camerakey
def fixCameraPos(obj, index):
	torso = index.get(index.var.astronautkeys["torso"])
	obj[Transf].setRpos(glm.vec3(
		torso[Transf].cpos.x,
		torso[Transf].cpos.y,
		max(-20 - index.var.sinceLastColl * 8, -60)
	))
	index.var.sinceLastColl = index.var.sinceLastColl + Engine.dTime
	return
def resetTimer(index, collision):
	if "asteroid" in collision[1]:
		index.var.sinceLastColl = 0
	return
	
def createHUD(index):
	fps = index.createObj(
		"fps_text",
		[
			Transf(glm.vec3(0.75, 1, 1), glm.quat(), glm.vec3(1)),
			Rend(True, "basicText", {
				"colour": RED, "alpha": 1
			}),
			Text("FPS: ", "fancyFont"),
			PostScript(fpsPostScript)
		]
	)
	info = index.createObj(
		"info_text",
		[
			Transf(glm.vec3(-1, -0.75, 1), glm.quat(), glm.vec3(1)),
			Rend(True, "basicText", {
				"colour": WHITE, "alpha": 1
			}),
			Text("DISTANCE TO SPACE SHIP: \nSPEED: ", "fancyFont"),
			PostScript(infoTextScript)
		]
	)
	center = index.createObj(
		"congrats_text",
		[
			Transf(glm.vec3(-0.5, 0, 1), glm.quat(), glm.vec3(2, 4, 2)),
			Rend(False, "basicText", {
				"colour": WHITE, "alpha": 1
			}),
			Text("CONGRADULATIONS!!!", "fancyFont")
		]
	)
	return (fps, info, center)
def fpsPostScript(obj, index):
	obj[Text].string = "FPS: " + str(Engine.getAverageFrameRate())
	return
def infoTextScript(obj, index):
	distance = round(glm.distance(
		index.get(index.var.astronautkeys["torso"])[Transf].cpos,
		index.get(index.var.rocketkey)[Transf].cpos
	))
	vel = glm.length(rb.calcVel(
		index.get(index.var.astronautkeys["torso"])[Rigidbody],
		index.get(index.var.astronautkeys["torso"])[Transf]
	))
	vel = 0 if glm.isnan(vel) else vel
	index.var.speedHistory.append(vel)
	if len(index.var.speedHistory) == 10:
		index.var.avgSpeed = str(round(sum(index.var.speedHistory) / 10))
		index.var.speedHistory = []
	obj[Text].string = "DISTANCE TO SPACE SHIP: "+str(distance)+"m\nSPEED: "+index.var.avgSpeed+"m/s"
	return
	
def attachRocketHandle(index, collision):
	hand = index.get(collision[0])
	if collision[1] == hand[Attractor].targetkey:
		#attach the hand to the rocket with a PhysJoint
		handleTransf = index.get(collision[1])[Transf]
		_ = index.createObj(
			"joint_" +collision[0]+"rocket",
			[PhysJoint(
				collision[0], "rocket",
				glm.vec3(0, -hand[Transf].scale.y / 2, 0), handleTransf.rpos,
				glm.angleAxis(glm.pi()*7/8, glmh.xUnit()), freedom=glm.vec3(30)
			)]
		)
		
		#turn off this collision function and increment counter
		hand[Attractor].power = 0
		hand[Coll].postcollide = None
		index.var.handsOnRocket = index.var.handsOnRocket + 1
		
		#turn off rocket gravity and turn on rocket
		if index.var.handsOnRocket == 2:
			print("attach rocket!")
			rocket = index.get("rocket")
			rocket[Jet].force = index.get("rocket")[Rigidbody].mass * 20
			index.var.rocketSteer = index.createObj(
				"rocketSteerer",
				[
					Transf(glm.vec3(), glm.quat(), glm.vec3(1)),
					Rend(True, "solidUnlitColour", {"colour": glm.vec3(1, 0, 0)}),
					Model("sphere", False),
					PreScript(rocketSteererUpdate),
				]
			)
			index.addProp("rocket", PIDSteer("rocketSteerer", 0.6, 0, 0.125, 100))
			index.addProp("rocket", Timer(0.0625))
			index.addProp("rocket", PreScript(makeEmission))
			
			
			for key in index.var.astronautkeys.values():
				index.get(key)[Rigidbody].suffersGravity = False
			
			index.var.swapTimer = 0
		
	return
	
def makeEmission(obj, index):
	if obj[Timer].click:
		transf = obj[Transf]
		index.createObj(
			"rocketEmission",
			[
				Transf(transf.cpos + -glmh.yBasis(transf.cori) * 3, transf.cori, glm.vec3(1)),
				Timer(2, deleteOnCycle=True),
				Rend(True, "rocketEmission", {"time": None}),
				ParticleEffect(8, pointSize=4)
			]
		)
	return
	
def rocketSteererUpdate(obj, index):
	rocketTransf = index.get("rocket")[Transf]
	obj[Transf].setRpos(glm.vec3(
		rocketTransf.cpos.x + 32 * ((Controller.checkKey("DIR_E")>0)-(Controller.checkKey("DIR_W")>0)),
		rocketTransf.cpos.y + 32 * ((Controller.checkKey("DIR_N")>0)-(Controller.checkKey("DIR_S")>0)),
		rocketTransf.cpos.z
	))
	
	return
	