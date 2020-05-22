import numpy as np
import threading
import queue
import pygame
from agent import *


class player:

	def __init__(self,
				interface,
				N_percepts,
				N_actions,
				P_bases
				):

		self.interface = interface

		self.training_queue = queue.Queue()

		self.watcher = agent(N_percepts,N_actions,P_bases)

		self.kill_flag = False

	def get_move(self,P):
		m = self.interface.get_move(P)
		if m == -1:
			self.kill_flag = True
			return(0)
		else:
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














