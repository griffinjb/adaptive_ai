import numpy as np 
from linear import *
from bayes import *
import queue

class Agent:


	def __init__(self,cfg,optimizer='bayes'):
		optimizers = {
				'linear':Linear(cfg),
				'bayes':Bayes(cfg)
				}

		self.brain = optimizers[optimizer]

		self.training_queue = []

	def train(self,spawn_process=False):

		if spawn_process:

			a = ''

		else:

			while self.training_queue:
				item = self.training_queue.pop()
				# print(item)
				self.brain.train(item[0],item[1])

	def get_move(self,percept):

		move = self.brain.predict(percept)
		return(move)

