from enum import Enum
import numpy as np

class EntityColor:
	# KEY	     R    G    B
	DEFAULT	= (255,   0, 255)
	PLAYER	= (197,  40,  40)
	GRASS	= ( 46, 125,  50)
	LAVA	= (255, 145,   0)
	GOLD	= (255, 234,   0)

class EntityType(Enum):
	BLOCK	= 0,
	GOLD	= 1,
	LAVA	= 2,
	PLAYER	= 3,

class EntityState(Enum):
	ALIVE	= 0,
	DEAD	= 1

class Entity(object):
	def __init__(self, pos, etype, color):
		(self._x, self._y) = pos
		self._etype = etype
		self._color = color
		self._width = 1
		self._height = 1

	def move(self, block):
		(self._x, self._y) = block.pos()

	def pos(self):
		return (self._x, self._y)

	def etype(self, etype = None):
		# Get()
		if etype == None:
			return self._etype

		# Set()
		self._etype = etype

		return self._etype

	def color(self, color = None):
		# Get()
		if color == None:
			return self._color

		# Set()
		self._color = color

		return self._color

	def width(self, width = None):
		# Get()
		if width == None:
			return self._width

		# Set()
		self._width = width

		return self._width

	def height(self, height = None):
		# Get()
		if height == None:
			return self._height

		# Set()
		self._height = height

		return self._height

class Player(Entity):
	_health = 10
	_maxhealth = 10
	_mana = 0
	_maxmana = 10
	_state = EntityState.ALIVE

	def __init__(self, pos):
		super(Player, self).__init__(pos, EntityType.PLAYER, EntityColor.PLAYER)

	def move(self, block):
		if block.etype() == EntityType.GOLD:
			self.mana(self._mana + 1)
			block.etype(EntityType.BLOCK)
			block.color(EntityColor.GRASS)
		elif block.etype() == EntityType.LAVA:
			self.health(self._health - 1)

		super(Player, self).move(block)

	def health(self, health = None):
		# Get()
		if health == None:
			return self._health

		# Set()
		if health <= 0:
			health = 0
			self.state(EntityState.DEAD)
		elif health >= self._maxhealth:
			mana = self._maxmana

		self._health = health

		return self._health

	def mana(self, mana = None):
		# Get()
		if mana == None:
			return self._mana

		# Set()
		if mana <= 0:
			mana = 0
		elif mana >= self._maxmana:
			mana = self._maxmana

		self._mana = mana

		return self._mana

	def state(self, state = None):
		# Get()
		if state == None:
			return self._state

		# Set()
		self._state = state

		return self._state
