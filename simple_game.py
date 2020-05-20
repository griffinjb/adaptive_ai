from agent import *
from player import *
from interface import *
import argparse
import sys

# Features:

	# F11 -> Toggle Full Screen
	# ESC -> Exit
	# WASD -> Directional Control

# Bugs:

	# no corner drag window resizing
	# aspect ratio gets warped


class simple_game:

	def __init__(self,resource_density=[.8,.01,.19]):

		parser = argparse.ArgumentParser()
		# --windowed
		parser.add_argument('--windowed',
				action='store_true',
				help='Starts game in windowed mode')
		args = parser.parse_args()

		self.xmin = -5
		self.xmax = 5
		self.ymax = 5
		self.ymin = -5

		self.interface = Interface(args)

		self.resource_density = resource_density 

		self.init_pieces()

		self.init_board()

		self.FPS = 10
		self.capture_FPS = 30

	def init_board(self):

		self.board = {}

		for piece in self.pieces:

			visible_coords = piece.get_visible_coords()

			for coord in visible_coords:

				if coord[0] > self.xmax:
					self.xmax = coord[0]
				if coord[0] < self.xmin:
					self.xmin = coord[0]
				if coord[1] < self.ymin:
					self.ymin = coord[1]
				if coord[1] > self.ymax:
					self.ymax = coord[1]

				if str(coord) not in self.board.keys():

					self.board[str(coord)] = self.new_block()

	def iter(self):

		if self.interface.quit_flag:
			sys.exit()

		for piece in self.pieces:
			P = self.get_percept(piece)
			piece.get_move(P)
			self.get_percept(piece) # Update Visible

		self.train_all()

		time.sleep(1/self.FPS)
		self.show_board()

	def train_all(self):

		players = [piece for piece in self.pieces if piece.isHuman]
		agents = [piece for piece in self.pieces if not piece.isHuman]

		training_data = []
		for p in players:
			while not p.controller.training_queue.empty():
				training_data.append(p.controller.training_queue.get())

		for a in agents:
			for percept,action in training_data:
				a.controller.PDF_Update(percept,action)

	def show_board(self):

		canvas = np.zeros([self.xmax-self.xmin,self.ymax-self.ymin])

		# for k in self.board.keys():
		for piece in self.pieces:

			coords = piece.get_visible_coords()
			for k in coords:
				k = str(k)

				coord = k[1:-1]
				coord = coord.split(',')
				coord = [int(coord[i]) for i in [0,1]]

				canvas[coord[0]-self.xmin,coord[1]-self.ymin] = self.board[k]+1

		self.interface.put_frame(canvas)

		# plt.figure('Game Board')
		# plt.cla()
		# plt.imshow(canvas)
		# plt.show(block=False)
		# plt.pause(.01)



	def init_pieces(self):

		self.pieces = []

		self.init_player()

		self.init_agent()

	def init_agent(self):

		# init agent (num percepts, num actions, base)
		self.pieces += [Piece(agent(9,5,3),[0,0]) for _ in range(10)]

	def init_player(self):
		self.pieces += [Piece(player(self.interface),[0,0])]

	def new_block(self):

		PDF = self.resource_density

		return(np.sum([step(np.random.uniform(0,1)-np.sum(PDF[:i]),1) for i in range(1,len(self.resource_density))]))

	def get_percept(self,piece):

		coords = piece.get_visible_coords()


		P = np.zeros(len(coords))

		i = 0

		for coord in coords:

			if coord[0] > self.xmax-1:
				self.xmax = coord[0]+1
			if coord[0] < self.xmin:
				self.xmin = coord[0]
			if coord[1] < self.ymin:
				self.ymin = coord[1]
			if coord[1] > self.ymax-1:
				self.ymax = coord[1]+1

			if str(coord) in self.board.keys():
				P[i] = self.board[str(coord)]
			else:
				self.board[str(coord)] = self.new_block()
				P[i] = self.board[str(coord)]
			i += 1

		return(P.flatten())

class Piece:

	def __init__(self,controller,location=[0,0]):

		self.location = np.array(location)

		# Controller has "get_move(P)" attribute
		self.controller = controller

		self.isHuman = False
		if 'player' in str(type(controller)):
			self.isHuman = True


	def get_move(self,P):
		move_idx = self.controller.get_move(P)

		# stop, up, down, left, right
		# moves = [[0,0],[-1,0],[1,0],[0,-1],[0,1]]
		moves = [[0,0],[0,-1],[0,1],[-1,0],[1,0]]

		move = np.array(moves[move_idx])

		self.location += move

		return(move)

	def get_visible_coords(self):

		mods = [[-1,-1],[-1,0],[0,-1],[1,-1],[-1,1],[0,0],[1,0],[0,1],[1,1]]

		return([[self.location[0]+mod[0],self.location[1]+mod[1]] for mod in mods])


G = simple_game()

while 1:
	G.iter()



