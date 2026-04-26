from config import *

from System.Engine import Engine

from Core.Props.Transf import Transf
from Core.Props.Timer import Timer
from Core.Props.Scripts import PreScript

from Core.Props.Graphics.Rend import Rend
from Core.Props.Graphics.Text import Text
from Core.Props.Graphics.Model import Model
from Core.Props.Graphics.Camera import Camera
from Core.Props.Graphics.Lights import SpotLight
from Core.Props.Graphics.Lights import Light

from Project.Script.Construct.Asteroid import Asteroid

from Core.Props.Coll import Coll
from Core.Props.Physics.Rigidbody import Rigidbody

def setup(index):
	
	Engine.loadResources("menu")		#load resources for menu
	Engine.loadResources("sample")		#load resources for menu
	
	#create UI elements
	index.createObj(
		"menu_text",
		[
			Transf(glm.vec3(-1, 1, 1), glm.quat(), glm.vec3(2)),
			Rend(True, "basicText", {
				"colour": WHITE, "alpha": 1
			}),
			Text(
				"[MENU]\n\nTITLESCREEN\nPRESS RETURN TO START\nPRESS ESCAPE/DELETE TO CLOSE",
				"fancyFont"
			),
		]
	)
	
	#make a camera with a light
	camerakey = index.createObj(
		"camera",
		[
			Transf(glm.vec3(0, 0, -64), glm.quat(), glm.vec3(0.1)),
			
			Camera(100),
			Light(glm.vec3(0.75, 0.75, 1), 1),
			SpotLight(glmh.zUnit(), glm.vec2(30, 60)),
		]
	)
	
	#add a background
	index.createObj(
		"background",
		[
			Transf(glm.vec3(0, 0, 128), glm.quat(), glm.vec3(1024, 512, 1)),
			
			Rend(True, "unLitTexture", {"tex": "purpleSky", "uvScale": glm.vec2(8, 4)}),
			Model("plane", True)
		]
	)
	
	#create asteroid spawners
	for i in range(0, 360, 45):
		index.createObj(
			"spawner_" + str(i),
			[
				Transf(128 * glm.vec3(
					glm.sin(glm.radians(i)),
					glm.cos(glm.radians(i)),
					0
				), glm.angleAxis(glm.radians(i), glmh.zUnit()), glm.vec3(4)),
				Timer(3, time=random.random()),
				PreScript(spawnAsteroid),
			]
		)
	
	return camerakey

def spawnAsteroid(obj, index):
	transf = obj[Transf]
	if obj[Timer].click:
		Asteroid.construct(
			index,
			obj[Transf].cpos,
			-transf.cpos / 64
		)
	return