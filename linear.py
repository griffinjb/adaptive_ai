import numpy as np 
from math_utils import *


class Linear:

	def __init__(self,cfg):
		self.NA = int(cfg.get('action','num_actions'))
		bases = eval(cfg.get('percept','bases'))
		shapes = eval(cfg.get('percept','percept_shapes'))
		JDF_shape = []
		for base,shape in zip(bases,shapes):
			if base:
				JDF_shape += [base for i in range(np.prod(shape))]

		self.JDF = np.zeros(JDF_shape+[self.NA])
		self.NP = len(self.JDF.shape[:-1])
		self.W = np.zeros([self.NA,self.NP])
		self.percepts = []
		self.actions = []

	def fit(self,percept,action):

		# Constrained opt.

		# argmin_W { WP - A } , WP on convex hull of A-basis
									  # cross polytope, bipyramid

		# L1(WP) = 1 , A_i > for all i

		# So it is really a non-negativity constraint,
		# and a single hyperplane constraint

		# The hyperplane is orthogonal to [1,1,...,1]
		# and intersects [1,0,...,0]

		# percept is constrained to discrete hyper-rectangle

		# The degree of the percept graph is equal to 
		# the dimension of the percept X 2 at most

		# First, offline. 
		# Build JDF
		# Store (percept,action)
		# Learn JDF_percept via least squares


		self.JDF[tuple(np.array(percept+[action]).astype('int'))] += 1

		self.percepts.append(percept)

		self.actions.append(action)



		# Least squares

		R_inv_percept = np.linalg.pinv(autocorrelation_matrix(np.array(self.percepts)))

		densities = []
		for P in self.percepts:
			densities.append(self.JDF[tuple(np.array(P).astype('int'))])
		densities = np.array(densities)


		for i in range(self.NA):

			density_i = densities[:,i]

			cross_percept_action_density = cross_correlation(np.array(self.percepts),density_i)

			w = R_inv_percept @ cross_percept_action_density

			self.W[i,:] = w


			# cross_percept_action_density = cross_correlation(np.array(percepts),np.array(actions))

			# w = R_inv_percept @ cross_percept_action

		# Now, convert to online iterative approximation

	def predict(self,percept):

		percept += 1

		predicted_density = self.W@percept[:,None]

		D = predicted_density / np.sum(predicted_density)

		return(iCDF(np.random.uniform(0,1),D))




