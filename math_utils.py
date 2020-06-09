import numpy as np 

def step(x, A):
	if x >= 0:
		return A
	else:
		return 0

def autocorrelation_matrix(X):

	R = np.zeros([X.shape[1],X.shape[1]])

	for x in X:

		R += x[:,None]@x[None,:]

	R /= X.shape[0]

	return(R)

def cross_correlation(X,Y):

	# X is Matrix [N observations, N percepts]

	# Y is Vector [N observations,1]

	# We want E[x * y]

		# [N percepts, 1]

	P = np.zeros(X.shape[1])

	for i in range(Y.shape[0]):

		P += X[i,:] * Y[i]

	P /= X.shape[0]

	return(P)

def CDF(x,PDF):

	return(np.sum([step(x-i,PDF[i]) for i in range(self.NA)]))

# {0<=x<=1}
def iCDF(x,PDF):

	return(np.sum([step(x-np.sum(PDF[:i]),1) for i in range(1,len(PDF))]))

def l_to_c(l):
	return(tuple(np.array(P).astype('int')))
	