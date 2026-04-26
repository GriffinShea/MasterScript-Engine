import random
from System.Engine import Engine
from Project.States.Start import Start

#===================================================================================================
#
#	v1.01
#
#	>Controller, Renderer, and ResourceManager all moved to "System"
#	>a new class called Engine controls the game loop and the clock
#	>implemented resource_files/[filename].rsc for Engine.load() and
#		Engine.unload() (which use ResourceManager)
#
#	>Game and Session replaced with GameManager and uses states
#	>four types of states (Core.StateTypes):
#		>Lossy --> for when you need a new canvas/index/camerakey
#		>Lossless --> retains the canvas/index/camerakey from the last state
#		>Screen --> no index, manual draw with Renderer
#		>Container --> combines Screen and holds another state internally (think pause menu)
#
#	>game state variables (objectives, flags, important keys) now have a place in index.var
#	>added Text props (type of Rend): a text box drawn after the gbuffer render
#	>added PosLimit prop (limits position to a set range)
#	
#	>reorganization of project code:
#		>Project
#			>States
#				>Start
#				>MainMenu
#				>Pause
#				>etc...
#			>Script
#				>Setup
#					>Level1
#					>Level2
#					>etc...
#				>Construct
#					>Rocket
#					>Astronaut
#					>etc...
#	
#	>several other minor changes to engine and sample project (astrosurfer)
#
#	========================================================================================
#
#	REVISIT:
#	
#	$need to double check checkCollision implementation of GJKSM
#	$need to double check implementation of lights especially DirLight and SpotLight which shadow
#
#	$need to finalize file organization
#	$should split up config file
#
#	$"glmh.zUnit() * self[Transf].scale.x" --> "glmh.vecZ(self[Transf].scale.x)"
#
#	$optimize Transf ?
#	$need to check BoxCollider.castRay's (use of scale)
#
#	$cylinders with locked orientation do not like inclines
#	$rigidbody physics needs some work basically i would like collision manifolds instead of just
#		points and/or repeat collision detection and resolution until objects settle, maybe use
#		parallelism and increment timesteps???
#		(continuous detection would also be a nice addition)
#
#===================================================================================================

def main():
	#seed random number generator with your favourite number (or system time)
	random.seed(1250)#random.seed(time.time())
	
	#run the game with MasterScript
	Engine.run(Start)
	
	return

if __name__ == "__main__":
	main()

exit()
