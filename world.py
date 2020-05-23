import numpy as np

from entities import *

def worldgenerator(densities, width, height):
	floor = np.empty([width, height], dtype=object)
	for x in range(width):
		for y in range(width):
			val = np.sum([step(np.random.uniform(0, 1) - np.sum(densities[:i]), 1) for i in range(1, len(densities))])

			color = EntityColor.FLOOR
			if val == 1:
				color = EntityColor.LAVA
			elif val == 2:
				color = EntityColor.GOLD

			floor[x, y] = Entity(x, y, EntityType.BLOCK, color)

	return floor

# TODO: Move this somewhere else
def step(x, A):
	if x >= 0:
		return A
	else:
		return 0

class World:
	def __init__(self, width, height):
		self.floor = worldgenerator([0.8, 0.1, 0.1], width, height)
		self.entities = np.empty(0, dtype=object)
		self.skybox = (135, 206, 250)

	def spawn(self, entity):
		if entity.type == EntityType.PLAYER:
			self.player = entity
		else:
			self.add_entity(entity)

	def add_entity(self, entity):
		self.entities = np.append(self.entities, entity)

	def block_at(self, x, y):
		(h, w) = self.floor.shape
		if x < 0 or x >= w or y < 0 or y >= h:
			return None
		else:
			return self.floor[x, y]

	def move(self, entity, dxy):
		if dxy == (0, 0):
			return

		_x = entity.x + dxy[0]
		_y = entity.y + dxy[1]

		# World Boundary
		block = self.block_at(_x, _y)
		if block == None:
			return

		self.player.x = _x
		self.player.y = _y
