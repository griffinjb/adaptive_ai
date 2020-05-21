import numpy as np
import threading
import queue
import pygame
from agent import *


class player:

	def __init__(self,interface):

		self.interface = interface

		self.training_queue = queue.Queue()

		self.watcher = agent(9,5,3) # fix hardcode

	def get_move(self,P):
		m = self.interface.get_move(P)
		self.training_queue.put([P,m])
		return(m)

	def copy(self):
		new_agent = self.watcher.copy()
		return(new_agent)		

	def train(self,P,A):
		self.watcher.train(P,A)


def demoUI():
	
	P = player()

	import time

	while 1:

		print(P.get_move())
		time.sleep(.1)














