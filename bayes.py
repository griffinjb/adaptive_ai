import numpy as np 
from math_utils import *

class Bayes:

	def __init__(self,cfg):
		a = ''
		self.NA = int(cfg.get('action','num_actions'))
		bases = eval(cfg.get('percept','bases'))
		shapes = eval(cfg.get('percept','percept_shapes'))

		# We table giving:

		#	P(P|A)
		# 	[NA,NP,PB]

		# dirichlet prior
		# JDF_shape = []
		# for base,shape in zip(bases,shapes):
			# if base:
				# JDF_shape += [base for i in range(np.prod(shape))]

		self.NP = sum([np.prod(shape) for shape in shapes])
		# self.NP = sum(JDF_shape)
		self.PP_PA = np.ones([self.NA,self.NP,max(bases)])

	def train(self,percept,action):

		for i in range(len(percept)):
			self.PP_PA[int(action),i,int(percept[i])] += 1
			# self.PP_PA[int(action),i,:] /= np.sum(self.PP_PA[int(action),i,:])

	def get_action_marginal(self):
		return(np.sum(np.sum(self.PP_PA,axis=1),axis=1))

	def get_percept_marginal(self):
		return(np.sum(self.PP_PA,axis=0))

	def predict(self,percept):

		# ln ( P(A) / P(!A) ) + sum { ln ( P(p_i | A) / P(p_i | !A) ) }

		A_values = []

		# for each action
		for i in range(self.NA):
			PA = self.get_action_marginal()
			# ln ( P(A) / P(!A) )
			prior = np.log(PA[i] / (sum(PA) - PA[i]))

			# sum { ln ( P(p_i | A) / P(p_i | !A) ) }

			marg_A = self.PP_PA[i].copy()
			mA_norm = np.sum(marg_A,axis=1)
			for k in range(marg_A.shape[0]):
				marg_A[k,:] /= mA_norm[k]

			marg_notA = np.sum(self.PP_PA,axis=0) - self.PP_PA[i]
			mnA_norm = np.sum(marg_notA,axis=1)
			for k in range(marg_notA.shape[0]):
				marg_notA[k,:] /= mnA_norm[k]

			ratio = 0
			for j in range(self.NP):

				ratio += np.log(marg_A[j,int(percept[j])]/marg_notA[j,int(percept[j])])

			A_values.append(prior+ratio)

		# if False not in (A_values[0] == A_values):
		# return(np.random.randint(0,self.NA))
		PDF = np.exp(A_values)
		PDF /= np.sum(PDF)
		return(iCDF(np.random.uniform(0,1),PDF))














