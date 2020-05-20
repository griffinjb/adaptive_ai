# Hey Spenny, here is the zeroth part of the quest

# Get python 3 installed. I use 3.6.5

# I use 'pip' as my package manager. This lets me
# easily install libraries.

# What OS are you on? This may impact your coding setup.

# If you like IDE's, or want a lot of the build environment
# to be handled for you, I recommend installing Anaconda/Spyder.

# Personally, I use a command terminal and run code with:

# 	python -i file.py

		# -i leaves the python interpreter open after it runs.

# 	python -m pdb file.py
	
	# This opens the debugger.

	# 'b 30' will put breakpoint at line 30, so you can inspect variables.

	# 'n' goes to next line

	# 'c' continues the code till next breakpoint

	# while in debug, preface python commands with '!'
		# otherwise, it will try to run debugger 'b,n,c' commands

		# you can also type 'interact' to enter interactive mode

		# typing 'dir()' will print names of the environment variables
		# in your current scope.


# I use sublime text, but atom is just as good.

# Deliverable:

# Run the following script with no errors:

# Use: 'python s0.py'

import numpy as np # For arrays and linear algebra

import matplotlib.pyplot as plt # for plotting

import pygame # has a lot of game utilities

pygame.init()
window_size = (420,420)
screen_color = (150,20,30)

screen = pygame.display.set_mode(window_size)
screen.fill(screen_color)
pygame.display.flip()


data = np.linspace(0,100,1000)

sin_data = np.sin(data)

plt.plot(sin_data)
plt.show()

# let me know what you see




