
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

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

		# so this is tricky, but we've been here before.

		# NP dimensions occupytng 

		# NP dimensional hypercube, w/vertices and 1 edge point

		# N points = B**NP


		self.PDFs = [None for _ in range(self.B**NP)]

		self.js = [0 for _ in range(self.B**NP)]


	def tf(self,P):

		# assume P is column 

		t = np.array([self.B**i for i in range(self.NP)])

		return(int(t@P))

	def get_move(self,P):
		return(self.stochastic_map(P))

	def stochastic_map(self,P):

		# This density estimator and generator.

			# Specifically, conditional density

		# Hash table of Percept Permutations (if discrete)

		# only hold the sums of discrete bins


		return(self.iCDF(np.random.uniform(0,1),P))



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



