from simple_game import *


class Board:

	def __init__(self,
				resource_density
				):

		self.resource_density = resource_density

		self.lookup_table = {}

		self.xmin = -5
		self.xmax = 5
		self.ymax = 5
		self.ymin = -5


	def get_canvas(self):
		return(np.zeros([self.xmax-self.xmin,self.ymax-self.ymin]))

	def set(self,coord,val=None):

		key = str(list(coord))

		if key not in self.lookup_table.keys():

			if not val:
				self.lookup_table[key] = self.new_block(coord)

			if coord[0] > self.xmax-1:
				self.xmax = coord[0]+1
			if coord[0] < self.xmin:
				self.xmin = coord[0]
			if coord[1] < self.ymin:
				self.ymin = coord[1]
			if coord[1] > self.ymax-1:
				self.ymax = coord[1]+1

		if val != None:
			self.lookup_table[key] = val

	def new_block(self,coord):

		PDF = self.resource_density

		val = np.sum([step(np.random.uniform(0,1)-np.sum(PDF[:i]),1) for i in range(1,len(self.resource_density))])
		if val == 1:
			val = 0

		if coord[0]%2 and val == 0:
			val = 1

		return(val)

	def at(self,location):
		key = str(list(location))
		val = self.lookup_table[key]
		return(val)


