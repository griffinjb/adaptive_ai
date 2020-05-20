import numpy as np 
import threading
import queue
import pygame
import matplotlib.pyplot as plt
import time
# from cv2 import resize, INTER_NEAREST

# Handles Issue where pygame display and capture
# must run from same thread.

# Is process

# can handle requests via Q for:

	# Screen update

	# User Input

# Bugs:

	# no fullscreen
	# no corner drag resizing
	# aspect ratio gets warped


class Interface:

	def __init__(self):

		self.move = queue.Queue()
		self.render = queue.Queue()

		self.I = threading.Thread(target=self.main_thread,daemon=True)
		self.I.start()

		self.screen_size = [800,800]

		self.quit_flag = False

	def main_thread(self):

		pygame.init()
		self.screen = pygame.display.set_mode(self.screen_size,pygame.RESIZABLE)
		pygame.event.set_blocked(None)
		pygame.event.set_allowed([
								pygame.KEYDOWN,
								pygame.QUIT,
								pygame.VIDEORESIZE
								])


		while 1:

			# If screen update, render
			self.show_board()

			self.poll_user_input()

	def poll_user_input(self):

		event = pygame.event.poll()

		if event.type == pygame.KEYDOWN:
			if event.unicode == 'w':
				self.move.put(1)
			if event.unicode == 'a':
				self.move.put(3)
			if event.unicode == 's':
				self.move.put(2)
			if event.unicode == 'd':
				self.move.put(4)

		if event.type == pygame.VIDEORESIZE:
			self.screen_size = list(event.size)
			self.screen = pygame.display.set_mode(event.size,pygame.RESIZABLE)

		if event.type == pygame.QUIT:
			self.quit_flag = True

	def get_move(self,P):

		if not self.move.empty():
			return(self.move.get())
		else:
			return(0)


	def put_frame(self,frame):

		self.render.put(frame)


	def show_board(self):

		if not self.render.empty():

			canvas = self.render.get()
			# canvas = resize(canvas,tuple(self.screen_size),interpolation=INTER_NEAREST)

			RGB_canvas = np.zeros([canvas.shape[0],canvas.shape[1],3])

			# Colors of squares, rgb
			# [background, floor, lava, gold]
			colors = [[0,0,0],[6,78,102],[255,131,36],[255,210,48]]

			for i in range(canvas.shape[0]):
				for j in range(canvas.shape[1]):
					a = ''
					RGB_canvas[i,j,:] = np.array(colors[int(canvas[i,j])])

			RGB_surface = pygame.surfarray.make_surface(RGB_canvas)
			RGB_surface = pygame.transform.scale(RGB_surface,tuple(self.screen_size))


			self.screen.blit(RGB_surface,(0,0))
			pygame.display.update()





			# plt.figure('Game Board')
			# plt.cla()
			# plt.imshow(canvas)
			# plt.show(block=False)
			# plt.pause(.01)



