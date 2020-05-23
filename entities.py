from enum import Enum

class EntityColor:
	# KEY	     R    G    B
	DEFAULT	= (255,   0, 255)
	PLAYER	= ( 98,  24,  48)
	FLOOR	= (  6,  78, 102)
	LAVA	= (255, 131,  36)
	GOLD	= (255, 210,  48)

class EntityType(Enum):
	BLOCK = 0,
	PLAYER = 1,

class Entity(object):
	def __init__(self, x, y, etype, color):
		self.x = x
		self.y = y
		self.type = etype
		self.color = color
		self.width = 1
		self.height = 1

class Player(Entity):
	def __init__(self, x, y):
		super(Player, self).__init__(x, y, EntityType.PLAYER, EntityColor.PLAYER)
