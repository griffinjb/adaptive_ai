from enum import Enum
import numpy as np
from percept import *

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
	_max_health = 10
	_mana = 0
	_max_mana = 10
	_state = EntityState.ALIVE
	controller = None
	percept = None
	PID = 0
	watchers = []

	def __init__(self, pos, cfg, controller=None):
		self.controller = controller
		self.percept = Percept(eval(cfg.get('percept','percept_shapes')))
		self.move_memory_buffer = np.zeros(eval(cfg.get('percept','percept_shapes'))[1])
		self.isHuman = 'Interface' in str(type(controller))
		self.watchers = [0,1,2,3]
		super(Player, self).__init__(pos, EntityType.PLAYER, EntityColor.PLAYER)

	def get_visible_coords(self):

		mods = [[-1,-1],[-1,0],[0,-1],[1,-1],[-1,1],[0,0],[1,0],[0,1],[1,1]]
		return([[self._x+mod[0],self._y+mod[1]] for mod in mods])

	def update_memory(self,new_move):

		self.move_memory_buffer[1:] = self.move_memory_buffer[:-1]
		self.move_memory_buffer[0] = new_move
		self.percept.temporal(self.move_memory_buffer)

	def get_move(self,percept):
		move_idx = self.controller.get_move(self.percept.vector)

		self.update_memory(move_idx)

		if move_idx == 0:
			move = (0,0)
		if move_idx == 1:
			move = (0,1)
		if move_idx == 2:
			move = (0,-1)
		if move_idx == 3:
			move = (-1,0)
		if move_idx == 4:
			move = (1,0)

		return(move)

	def train(self,training_items):
		for training_item in training_items:
			(_,percept,action) = training_item
			if not self.isHuman:
				self.controller.training_queue.append([percept,action])
	
		if not self.isHuman:
			self.controller.train()

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

		# health = np.min(np.max(health,0),self._max_health)

		# Set()
		if health == 0:
			self.state(EntityState.DEAD)
		elif health >= self._max_health:
			health = self._max_health

		self._health = health

		return self._health

	def mana(self, mana = None):
		# Get()
		if mana == None:
			return self._mana

		# Set()
		if mana <= 0:
			mana = 0
		elif mana >= self._max_mana:
			mana = self._max_mana

		self._mana = mana

		return self._mana

	def max_health(self, max_health = None):
		# Get()
		if max_health == None:
			return self._max_health

		# Set()
		self._max_health = max_health

		return self._max_health

	def max_mana(self, max_mana = None):
		# Get()
		if max_mana == None:
			return self._max_mana

		# Set()
		self._max_mana = max_mana

		return self._max_mana

	def state(self, state = None):
		# Get()
		if state == None:
			return self._state

		# Set()
		self._state = state

		return self._state
