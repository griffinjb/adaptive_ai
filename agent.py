import numpy as np
import matplotlib.pyplot as plt
import queue

class agent:

	# percepts (P)

	# actions (A)

	# Map(P->A)

	def __init__(self,NP,NA,B):

		self.NP = NP	# dim of percept space
		self.NA = NA	# dim of action space

		self.i 	= 0		# iteration

		self.B 	= B		# base for keygen
						# N states per dim

		self.feedback = 0 # Training Feedback

		self.training_queue = queue.Queue()

		# so this is tricky, but we've been here before.

		# NP dimensions occupytng 

		# NP dimensional hypercube, w/vertices and 1 edge point

		# N points = B**NP


		self.PDFs = [None for _ in range(self.B**NP)]

		self.js = [0 for _ in range(self.B**NP)]

	def copy(self):
		new_agent = agent(self.NP,self.NA,self.B)

		for i in range(len(self.PDFs)):

			if 'array' in str(type(self.PDFs[i])):
				new_agent.PDFs[i] = self.PDFs[i].copy()

			new_agent.js[i] = self.js[i]

		return(new_agent)

	def tf(self,P):

		# assume P is column 

		t = np.array([self.B**i for i in range(self.NP)])

		return(int(t@P))

	def get_move(self,P):
		m = self.stochastic_map(P)
		if np.random.uniform(0,1) < self.feedback:
			self.PDF_Update(P,m)
		return(m)

	# def linear_map(self,P):

		# This policy estimator uses a set of linear filters.

		# Each filter is applied to the (P)ercept,
		# and gives the probability of an (A)ction

		# W@P = PDF

		# We can normalize P such that it lies on a ball,
		# instead of a hypercube.

		# This cannot be realized with 0-vector, thus the 
		# mean must be shifted to the centroid of the hypercube?

		



	def stochastic_map(self,P):

		# This density estimator and generator.

			# Specifically, conditional density

		# Hash table of Percept Permutations (if discrete)

		# only hold the sums of discrete bins


		return(self.iCDF(np.random.uniform(0,1),P))

	def train(self,P,A):

		self.PDF_Update(P,A)

	# assume P is flattened
	def PDF_Update(self,P,A):

		# Alright fucker.

		# Use CDF**-1 to map uniform to conditional

		# P(A|P)

		# Store an estimate of P(A|P) for each P

		# A is discrete, 5 options, also self.NA

		idx = self.tf(P)

		if not 'array' in str(type(self.PDFs[idx])):
			self.PDFs[idx] = np.zeros(self.NA)

		self.PDFs[idx][A] += 1

		self.js[idx] += 1

	def PDF_Get(self,P):
		i = self.js[self.tf(P)]
		PDF = self.PDFs[self.tf(P)]
		if i:
			return(PDF/i)
		else:
			# return(np.array([.1,.1,.6,.1,.1]))
			return(np.ones(self.NA)/self.NA)

	def CDF(self,x,P):

		PDF = self.PDF_Get(P)

		return(np.sum([step(x-i,PDF[i]) for i in range(self.NA)]))

	# {0<=x<=1}
	def iCDF(self,x,P):

		PDF = self.PDF_Get(P)

		return(np.sum([step(x-np.sum(PDF[:i]),1) for i in range(1,self.NA)]))

def step(x,A):
	if x >= 0:
		return(A)
	if x < 0:
		return(0)

def demo1():

	# Percepts
	P = np.zeros([3,3]).flatten()

	# init agent (num percepts, num actions, base)
	A = agent(9,5,3)

	# Sadly, this leads to 3**9 * 5 parameters.

	# This can be improved in a few ways.

	# Training must generalize!

	# based on similarity?

	# If the environment fits a distribution,
		# some states will be more likely than others.
		# and we won't need all PDF's


	A.PDF_Update(P,1)
	A.PDF_Update(P,1)
	A.PDF_Update(P,1)
	A.PDF_Update(P,2)
	A.PDF_Update(P,0)


	D = np.random.uniform(0,1,10000)

	DT = np.array([A.iCDF(d,P) for d in D])

	plt.hist(DT)

	plt.show()



