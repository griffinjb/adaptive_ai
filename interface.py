import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class Interface:
	def __init__(self, width, height, args):
		self.display_flags = pygame.FULLSCREEN | pygame.RESIZABLE
		if args.windowed:
			self.display_flags ^= pygame.FULLSCREEN

		self.screen_size = [width, height]
		self.close_requested = False
		self.zoom = 50

		self.last_key = None

		pygame.init()
		self.frame = pygame.Surface(self.screen_size)

		# Initialize Display
		self.screen = pygame.display.set_mode(self.screen_size, self.display_flags)
		pygame.display.set_caption("Adaptive AI Demo")

		# Setup Events
		pygame.event.set_blocked(None)
		pygame.event.set_allowed([
			pygame.KEYDOWN,
			pygame.KEYUP,
			pygame.QUIT,
			pygame.VIDEORESIZE])

	def poll_user_input(self):
		event = pygame.event.poll()

		_type = event.type

		move = 0

		# KEYDOWN
		if _type == pygame.KEYDOWN:
			key = event.key
			move = self.handle_key(key)
			self.last_key = key
		elif _type == pygame.KEYUP:
			self.last_key = None
		# QUIT
		elif _type == pygame.QUIT:
			self.close_requested = True
		# VIDEORESIZE
		elif _type == pygame.VIDEORESIZE:
			self.screen_size = list(event.size)
			self.screen = pygame.display.set_mode(self.screen_size, self.display_flags)
			self.frame = pygame.Surface(self.screen_size)
		elif self.last_key != None:
			move = self.handle_key(self.last_key)

		return move

	def get_move(self,percept=None):
		return(self.poll_user_input())

	def handle_key(self, key):
		move = 0
		# F11 - Toggle Fullscreen
		if key == pygame.K_w:
			move = 2
		elif key == pygame.K_a:
			move = 3
		elif key == pygame.K_s:
			move = 1
		elif key == pygame.K_d:
			move = 4
		elif key == pygame.K_UP:
			zoom = self.zoom + 1
			if zoom <= 100:
				self.zoom = zoom
		elif key == pygame.K_DOWN:
			zoom = self.zoom - 1
			if zoom >= 30:
				self.zoom = zoom
		elif key == pygame.K_F11:
			if (self.screen.get_flags() & pygame.FULLSCREEN):
				self.display_flags ^= pygame.FULLSCREEN
			else:
				self.display_flags |= pygame.FULLSCREEN
			self.screen = pygame.display.set_mode(self.screen_size, self.display_flags)
		# ESC - Quit interface
		elif key == pygame.K_ESCAPE or key == pygame.K_q:
			self.close_requested = True

		return move

	def update(self):
		return self.poll_user_input()

	def render(self, world):
		#self.screen.fill(world.skybox)

		player = world.players[0]
		(px, py) = player.pos()
		self.look_at = (px + player.width() / 2, py + player.height() / 2)

		self.frame.fill(world.skybox)
		# inet-2d (da95dd5): 
		#       30x30: ~35 ms. / ~40 ms.,
		#     500x500: >2 sec.
		# inet-2d (latest):
		#       30x30: ~9.1 ms.
		#     500x500: ~20.5 ms.
		tx1 = px - 25
		if tx1 < 0:
			tx1 = 0
		tx2 = px + 25
		if tx2 >= world.floor.shape[0]:
			tx2 = world.floor.shape[0]
		ty1 = py - 25
		if ty1 < 0:
			ty1 = 0
		ty2 = py + 25
		if ty2 >= world.floor.shape[1]:
			ty2 = world.floor.shape[1]

		for entity in world.floor[tx1:tx2, ty1:ty2].flat:
			self.render_entity(entity)
		for entity in world.entities:
			self.render_entity(entity)

		for player_ in world.players:
			self.render_entity(player_)

		self.render_hud(player)

		self.screen.blit(self.frame, (0, 0))
		pygame.display.flip()

	def render_entity(self, entity):
		if entity == None:
			return

		# Since the game is top-down 2D the rendering is a simple linear transformation: mX + b
		#     m := [x0, y0, x1, y1]' - [camera_x, camera_y, camera_x, camera_y]'
		#     X := [[sx, 0], [0, sy]]
		#     b := [res_w / 2, res_h /2]

		# Translate Origin (m)
		(px, py) = np.subtract(entity.pos(), self.look_at)

		# Perspective Transformation (X)
		sx = self.zoom * px
		sy = self.zoom * py
		ex = sx + self.zoom*entity.width()
		ey = sy + self.zoom*entity.height()

		# Apply Screen Translation (b)
		stx = self.screen_size[0] >> 1
		sty = self.screen_size[1] >> 1
		rec = [ sx + stx, sy + sty, ex - sx, ey - sy ]

		# Apply Culling
		if rec[0] >= self.screen_size[0] or rec[1] >= self.screen_size[1]:
			return 0
		elif rec[0] + rec[2] <= 0 or rec[1] + rec[3] <= 0:
			return 0

		# Apply Clipping
		if rec[0] + rec[2] > self.screen_size[0]:
			rec[2] = self.screen_size[0] -  rec[0]
		if rec[1] + rec[3] > self.screen_size[1]:
			rec[3] = self.screen_size[1] -  rec[1]

		# Render Tile
		pygame.draw.rect(self.frame, entity.color(), rec)

		return 1

	def render_hud(self, player):
		pygame.draw.rect(self.frame, (229,  57,  53), (10, 10, 210, 20))
		if player.health() != 0:
			pygame.draw.rect(self.frame, (0, 230, 118), (10, 10, player.health()/10*210, 20))
		pygame.draw.rect(self.frame, (0, 0, 0), (10, 10, 210, 20), 1)

		pygame.draw.rect(self.frame, (128/4, 216/4, 255/4), (10, 40, 210, 20))
		if player.mana() != 0:
			pygame.draw.rect(self.frame, (3, 155, 229), (10, 40, player.mana()/10.0*210, 20))
		pygame.draw.rect(self.frame, (0, 0, 0), (10, 40, 210, 20), 1)

	def should_close(self):
		return self.close_requested
