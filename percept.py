import numpy as np 

# Abstraction layer for environmental perceptions

class Percept:


	def __init__(self,
				move_memory=1,
				env_percept_shape=[3,3]
				):

		# number of recent moves in percept
		self.move_memory = move_memory

		# shape of board vision per agent
		self.env_percept_shape = env_percept_shape


	def get_percept(self,board,piece):

		coords = piece.get_visible_coords()

		P = np.zeros(len(coords))

		i = 0

		for coord in coords:

			if str(coord) in self.board.keys():
				P[i] = self.board[str(coord)]
			else:
				self.board[str(coord)] = self.new_block(coord)
				P[i] = self.board[str(coord)]
			i += 1

		return(P.flatten())		

