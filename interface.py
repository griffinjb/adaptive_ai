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

		pygame.init()

		# Initialize Display
		self.screen = pygame.display.set_mode(self.screen_size, self.display_flags)
		pygame.display.set_caption("Adaptive AI Demo")

		# Setup Events
		pygame.event.set_blocked(None)
		pygame.event.set_allowed([
			pygame.KEYDOWN,
			pygame.QUIT,
			pygame.VIDEORESIZE])

	def poll_user_input(self):
		event = pygame.event.poll()

		_type = event.type

		dxy = (0, 0)

		# KEYDOWN
		if _type == pygame.KEYDOWN:
			key = event.key

			# F11 - Toggle Fullscreen
			if key == pygame.K_w:
				dxy = (0, -1)
			elif key == pygame.K_a:
				dxy = (-1, 0)
			elif key == pygame.K_s:
				dxy = (0, 1)
			elif key == pygame.K_d:
				dxy = (1, 0)
			elif key == pygame.K_F11:
				if (self.screen.get_flags() & pygame.FULLSCREEN):
					self.display_flags ^= pygame.FULLSCREEN
				else:
					self.display_flags |= pygame.FULLSCREEN
				self.screen = pygame.display.set_mode(self.screen_size, self.display_flags)
			# ESC - Quit interface
			elif key == pygame.K_ESCAPE or key == pygame.K_q:
				self.close_requested = True
		# QUIT
		elif _type == pygame.QUIT:
			self.close_requested = True
		# VIDEORESIZE
		elif _type == pygame.VIDEORESIZE:
			self.screen_size = list(event.size)
			self.screen = pygame.display.set_mode(self.screen_size, self.display_flags)

		return dxy

	def update(self):
		return self.poll_user_input()

	def render(self, world):
		self.screen.fill(world.skybox)

		(px, py) = world.player.pos()
		self.look_at = (px + world.player.width() / 2, py + world.player.height() / 2)

		for entity in world.floor.flat:
			self.render_entity(entity)
		for entity in world.entities:
			self.render_entity(entity)

		self.render_entity(world.player)
		self.render_hud(world.player)

		pygame.display.update()

	def render_entity(self, entity):
		if entity == None:
			return

		# Since the game is top-down 2D the rendering is a simple linear transformation: mX + b
		#     m := [x0, y0, x1, y1]' - [camera_x, camera_y, camera_x, camera_y]'
		#     X := [[sx, 0], [0, sy]]
		#     b := [res_w / 2, res_h /2]

		# Translate Origin (m)
		(ex, ey) = np.subtract(entity.pos(), self.look_at)
		vec1 = [ex, ey]
		vec2 = [ex + entity.width(), ey + entity.height()]

		# Perspective Transformation (X)
		persp = np.matrix([[50, 0], [0, 50]])
		vec1 = vec1*persp
		vec2 = vec2*persp

		# Apply Screen Translation (b)
		screen_trans = [ self.screen_size[0] / 2, self.screen_size[1] / 2]
		rec = [ vec1[0, 0] + screen_trans[0], vec1[0, 1] + screen_trans[1], vec2[0, 0] - vec1[0, 0], vec2[0, 1] - vec1[0, 1] ]

		# Apply Culling
		if rec[0] >= self.screen_size[0] or rec[1] >= self.screen_size[1]:
			return
		elif rec[0] + rec[2] <= 0 or rec[1] + rec[3] <= 0:
			return

		# Apply Clipping
		if rec[0] + rec[2] > self.screen_size[0]:
			rec[2] = self.screen_size[0] -  rec[0]
		if rec[1] + rec[3] > self.screen_size[1]:
			rec[3] = self.screen_size[1] -  rec[1]

		# Render Tile
		pygame.draw.rect(self.screen, entity.color(), rec)

	def render_hud(self, player):
		pygame.draw.rect(self.screen, (229,  57,  53), (10, 10, 210, 20))
		if player.health() != 0:
			pygame.draw.rect(self.screen, (0, 230, 118), (10, 10, player.health()/10*210, 20))
		pygame.draw.rect(self.screen, (0, 0, 0), (10, 10, 210, 20), 1)

		pygame.draw.rect(self.screen, (128/4, 216/4, 255/4), (10, 40, 210, 20))
		if player.mana() != 0:
			pygame.draw.rect(self.screen, (3, 155, 229), (10, 40, player.mana()/10.0*210, 20))
		pygame.draw.rect(self.screen, (0, 0, 0), (10, 40, 210, 20), 1)

	def should_close(self):
		return self.close_requested
