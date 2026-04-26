import pygame
import OpenGL.GL as gl
import glmh

from config import *
from System.Renderer import Renderer
from System.ResourceManager import ResourceManager
from System.Controller import Controller

from Core.GameManager import GameManager

class Engine:
	clock = None
	lTime = 0
	dTime = 0
	
	@classmethod
	def run(cls, StartState):
		Renderer.init()
		cls.clock = pygame.time.Clock()
		cls.lTime = pygame.time.get_ticks()
		
		ResourceManager.generateBasicMeshes()
		ResourceManager.loadResources("engine")
		
		gameManager = GameManager(StartState)
		print("\nStarting game loop...")
		print("================================================================\n")
		while gameManager.state:
			gameManager.draw()
			cls.resetClock()
			Renderer.flipDisplay()
			Controller.pollInput()
			gameManager.updateState()
		print("\n================================================================")
		print("Game loop exit.")
		
		return
	
	@classmethod
	def getAverageFrameRate(cls):
		return int(cls.clock.get_fps() * 100) / 100
	
	@classmethod
	def resetClock(cls):
		cTime = pygame.time.get_ticks()
		cls.dTime = (cTime - cls.lTime + glmh.LOW_FLOAT_CONSTANT) / 1000
		cls.lTime = cTime
		if LIMIT_FRAME_RATE:
			cls.clock.tick(FRAME_RATE)
		else:
			cls.clock.tick()
		return
	
	@staticmethod
	def loadResources(rscFile):
		ResourceManager.loadResources(rscFile)
		return
	
	@staticmethod
	def unloadResources(rscFile):
		ResourceManager.unloadResources(rscFile)
		return
	