from interface import *
from world import *
from agent import *
import argparse
import configparser
import sys
import time

class Client:
	def __init__(self, cfg):
		parser = argparse.ArgumentParser()
		# --windowed
		parser.add_argument('--windowed', action='store_true', help='Starts game in windowed mode')
		args = parser.parse_args()

		world_width = int(cfg.get('world', 'width'))
		world_height = int(cfg.get('world', 'height'))

		screen_width = int(cfg.get('video', 'width'))
		screen_height = int(cfg.get('video', 'height'))

		self.FPS = int(cfg.get('video', 'fps'))

		self.close_requested = False

		self.world = World(world_width, world_height)

		self.interface = Interface(screen_width, screen_height, args)
		
		# Init Player
		self.world.spawn(Player(
							(int(world_width/2),int(world_height/2)),
							cfg,
							self.interface
							))

		# Init Agents
		self.world.spawn(Player(
							(int(world_width/2), int(world_height/2)),
							cfg,
							Agent(cfg)
							))



	def update(self):
		# dxy = self.interface.update()
		# self.world.move(self.world.player, dxy)

		# for player in self.world.players:
		# 	percept = self.world.get_percept(player)
		# 	dxy = player.get_move(percept)
		# 	self.world.move(player,dxy)

		self.world.perceive()
		self.world.react()
		self.world.learn()
		return

	def render(self):
		self.interface.render(self.world)
		return

	def close(self):
		return

	def should_close(self):
		return self.close_requested or self.interface.should_close()

if __name__ == '__main__':
	cfg = configparser.ConfigParser()
	cfg.read('./config')

	client = Client(cfg)

	t = 0
	last_time = time.time()

	while client.should_close() == False:
		dt = time.time() - last_time
		t = t + dt

		if t >= (1.0 / client.FPS):
			client.update()
			client.render()
			t = 0

		last_time = time.time()

	client.close()
