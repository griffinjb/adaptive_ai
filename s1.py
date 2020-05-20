# Ok doot, here' is round 1

# To get used to the idea of a physics engine
# we can simulate a simple kinematic system

# comments are just guidelines. If you can do it beter, do.

# 2d Orbital Sim.

# Use numpy for array operations.
import numpy as np # 'as' designates a nickname

# for plotting
import matplotlib.pyplot as plt 

# Consider a set of point masses
	# objects with mass but no volume

# What do we need to describe this system?
	# Velocity, Forces 

# Since the particles are accelerating, velocity is changing.

# However, we can approximate using constant velocity 
	# for small time steps.

# Ex. 
	# let P denote position
	# let V denote velocity
	# let P_0 denote position at time 0, etc.
	# let dt denote timestep size

	# P_1 = P_0 + V_0 * dt
	# P_2 = P_1 + V_1 * dt
	# etc.

		# think... how can we apply this 
		# same reasoning to compute new velocity
		# using acceleration? (hint: this is calculus)

# Now all we need is to compute V_0, V_1, ... V_N

	# We need acceleration for this (A)

		# We need net-forces for this (F)

			# We can compute this using position & mass

##############################################################
# Demo Function
##############################################################

# Find the equation for force of gravitation 
# Make a function to compute this force

# Here is an example:

# Let pointN be the (x,y) coordinates
# We want to return the force acting on point 1
# This is a vector! return Direction and magnitude.
def force_of_gravitation(point1,point2,mass1,mass2):
	
	# Force_gravity 
	# Fg = mass1*mass2*constant / (distance(point1,point2)**2)	

	# Let 'constant' = 1

	# This is euclidean norm, or l2 norm.
	# As the crow flies, distance metric
	# '**' designates squared
	# np.sqrt is sqare root
	distance = np.sqrt(np.sum((point1-point2)**2))  # same as np.linalg.norm()

	distance_squared = distance**2 # see a simplification here?

	Force_gravity = mass1*mass2 / distance_squared

	# We need a vector pointing from point1 to point2
	direction = point2-point1 # verify that this is correct

	# The direction needs to have unit length, divide by length
	direction = direction / np.linalg.norm(direction)

	# Now make the magnitude the force of graviy:
	Force_Vector = Force_gravity * direction

	return(Force_Vector)

	# Try to picture what this means in your head
	# Like with a 2d graph.


##############################################################
# First DIY
##############################################################


# Make a variable holding the number of particles.
	# use this to size the arrays

# Make an array containing the initial positions

	# shape must be: [N_particle rows, 2 columns (one for x,one for y)]
	
	# l = [1,2,3] makes a list
	# a = np.array(l) makes it into an array
	# a[0] will return 1
	# a[-1] will return 3

	# why an array? 

		# l + l = [1,2,3,1,2,3]		concatenates
		# a + a = [2,4,6]			elementwise addition

		# many other reasons, u will see

	# to make a 2d array:
		# a = np.array([[1,2],[3,4]])
		# a[row, column]
		# a[0,0] = 1
		# a[1,1] = 4
		# a[:,0] gives all rows, column 0 (called slicing)
		# a[0,:] gives all cols, row 0


	# Play with these things in the interpreter! 
		# Often times you can answer a question by 
		# just trying to do it in a command window.


# Make an array containing the initial velocities


# Make an empty array of 0's to hold the accelerations.


# Make empty array of forces. 


# Function to compute sum of forces of every particle
# on every other particle. 

	# hint: use nested loops


# Function to compute acceleration from forces
# is given above. Populate Acceleration array.


# Update velocity array using acceleration array
# Hint: use a timestep, like the position from velocity earlier.


# Update Position from velocity


# Display your position array using a scatterplot


# wrap the force, acceleration, and velocity updates in a while loop


# supply position array
def live_plot(XY_coords):
	while 1:
		plt.scatter(XY_coords[:,0],XY_coords[:,1]) 	# X_coords and Y_coords are an array or list.

		plt.show(block=False) 			# Plots to screen
										# block = False (usually it pauses, this keeps going)

		plt.pause(.01)					# needs time to render

# Don't forget, indentation controls loops and conditionals!





# glgl lmk if u have questions!
