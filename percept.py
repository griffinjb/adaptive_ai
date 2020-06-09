import numpy as np

class Percept:

	def __init__(self,shapes,bases=None):

		self.shapes = shapes # shapes of percepts

		# flattened percept, sum product shapes
		self.vector = np.zeros(np.sum([np.prod(shape) for shape in shapes if shape]))

		self.bases = bases # lengths of set(percept)


	# Spatial Percept - Contains LOS environmental information
	def spatial(self,percept=None):
		if not percept is None:
			self.vector[:np.prod(self.shapes[0])] = percept.flatten()
		else:
			return(self.vector[:np.prod(self.shapes[0])])


	# Temporal Percept - Buffer of move history
	def temporal(self,percept=None):
		if not percept is None:
			self.vector[np.prod(self.shapes[0]):np.prod(self.shapes[1])] = percept.flatten()
		else:
			return(self.vector[np.prod(self.shapes[0]):np.prod(self.shapes[1])])

	# Status Percept - Health and Mana Levels
	def status(self,percept=None):
		if not percept is None:
			self.vector[np.prod(self.shapes[1]):np.prod(self.shapes[2])] = percept.flatten()
		else:
			return(self.vector[np.prod(self.shapes[1]):np.prod(self.shapes[2])])

	# Communication Percept - Agent <-> information transfer (may be too hard)
	def communication(self,percept=None):
		if not percept is None:
			self.vector[np.prod(self.shapes[2]):np.prod(self.shapes[3])] = percept.flatten()
		else:
			return(self.vector[np.prod(self.shapes[2]):np.prod(self.shapes[3])])













