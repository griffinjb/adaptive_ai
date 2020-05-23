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

		self.look_at = np.multiply(50, [world.player.x + world.player.width/2.0, world.player.y + world.player.height/2.0])

		for entity in world.floor.flatten():
			if not entity:
				continue
			self.render_entity(entity)
		for entity in world.entities:
			if not entity:
				continue
			self.render_entity(entity)

		self.render_entity(world.player)

		pygame.display.update()

	def render_entity(self, entity):
		vec1 = [entity.x, entity.y]
		vec2 = [entity.x + entity.width, entity.y + entity.height]

		# Perspective Transformation
		persp = np.matrix([[50, 0], [0, 50]])

		vec1 = vec1*persp
		vec2 = vec2*persp

		# Apply Screen Translation
		res = [self.look_at[0] - self.screen_size[0]/2 - 1, self.look_at[1] - self.screen_size[1]/2 - 1]
		rec = [ vec1[0, 0] - res[0], vec1[0, 1] - res[1], vec2[0, 0] - vec1[0, 0], vec2[0, 1] - vec1[0, 1] ]

		# Apply Clipping
		if rec[0] + rec[2] >= self.screen_size[0]:
			rec[2] = self.screen_size[0] - 1 - rec[0]
		if rec[1] + rec[3] >= self.screen_size[1]:
			rec[3] = self.screen_size[1] - 1 - rec[1]

		# Render Tile
		pygame.draw.rect(self.screen, entity.color, rec)

	def should_close(self):
		return self.close_requested
