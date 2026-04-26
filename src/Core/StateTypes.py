import System.Engine
from Core.Painter import Painter

class Lossy:
	def __init__(self, canvas, index, camerakey):
		self.canvas = canvas
		self.index = index
		self.camerakey = camerakey
		System.Engine.Engine.resetClock()
		return
	
	def draw(self):
		Painter.paint(self)
		return
	
	def update(self):
		print("WARNING: update method for", type(self), "must be defined.")
		return
	
class Lossless(Lossy):
	def __init__(self, prevState):
		super().__init__(prevState.canvas, prevState.index, prevState.camerakey)
		return
	
class Screen(Lossy):
	def __init__(self):
		super().__init__(None, None, None)
		return
	
	def draw(self):
		print("WARNING: draw method for", type(self), "must be defined.")
		return

class Container(Screen):
	def __init__(self, containedState):
		super().__init__()
		self.containedState = containedState
		return
	
	def draw(self):
		self.containedState.draw()
		return
		