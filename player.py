import numpy as np 
import threading
import queue
import pygame





class player:

	def __init__(self,interface):

		self.interface = interface

		self.training_queue = queue.Queue()


	def get_move(self,P):
		m = self.interface.get_move(P)
		self.training_queue.put([P,m])
		return(m)

	# def capture_user_input(self):

		# pygame.init()
		# screen = pygame.display.set_mode([1,1])

		# # for event in pygame.event.get():
		# while 1:
		# 	event = pygame.event.wait()
		# 	# event = pygame.event.poll()

		# 	if event.type == pygame.KEYDOWN:
		# 		if event.unicode == 'w':
		# 			self.move.put(1)
		# 		if event.unicode == 'a':
		# 			self.move.put(3)
		# 		if event.unicode == 's':
		# 			self.move.put(2)
		# 		if event.unicode == 'd':
		# 			self.move.put(4)

		# 	if event.type == pygame.QUIT:
		# 		raise SystemExit


def demoUI():
	
	P = player()

	import time

	while 1:

		print(P.get_move())
		time.sleep(.1)














