from System.Controller import Controller
from Core.StateTypes import Container
from Project.States.Quit import Quit

class GameManager:
	def __init__(self, StartState):
		self.state = StartState()
		return
	
	def swapState(self, newState):
		if self.state != newState:
			if isinstance(newState, Container):
				print("GameState switch:", type(self.state), "-->", type(newState), "(", type(newState.containedState), ")")
			else:
				print("GameState switch:", type(self.state), "-->", type(newState))
		
		self.state = newState
		return
	
	def draw(self):
		self.state.draw()
		return
	
	def updateState(self):
		#handle current state and swap to new state
		self.swapState(self.state.update())
		
		#check for close window
		if Controller.handleClose():
			self.swapState(Quit())
		
		return
	