import numpy as np

from entities import *

def worldgenerator(densities, width, height):
	floor = np.empty([width, height], dtype=object)
	for x in range(width):
		for y in range(height):
			val = np.sum([step(np.random.uniform(0, 1) - np.sum(densities[:i]), 1) for i in range(1, len(densities))])

			color = EntityColor.GRASS
			etype = EntityType.BLOCK
			if val == 1:
				color = EntityColor.LAVA
				etype = EntityType.LAVA
			elif val == 2:
				color = EntityColor.GOLD
				etype = EntityType.GOLD

			floor[x, y] = Entity((x, y), etype, color)

	floor[2, 0].color(EntityColor.LAVA)

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
		self.skybox = (135/8, 206/8, 250/8)

	def spawn(self, entity):
		if entity.etype() == EntityType.PLAYER:
			self.player = entity
		else:
			self.add_entity(entity)

	def add_entity(self, entity):
		self.entities = np.append(self.entities, entity)

	def get_block(self, pos):
		(w, h) = self.floor.shape
		(x, y) = pos
		if x < 0 or x >= w or y < 0 or y >= h:
			return None
		else:
			return self.floor[x, y]

	def set_block(self, x, y, entity):
		(h, w) = self.floor.shape
		if x < 0 or x >= w or y < 0 or y >= h:
			return None
		else:
			self.floor[x, y] = entity

	def move(self, entity, dxy):
		if dxy == (0, 0):
			return

		new_pos = np.add(entity.pos(), dxy)

		# Process Entity Movement
		block = self.get_block(new_pos)
		if block == None:
			return

		entity.move(block)
