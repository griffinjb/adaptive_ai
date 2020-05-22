from agent import *
from player import *
from interface import *
from board import *
import argparse
import sys
import argparse

# Features:

	# F11 -> Toggle Full Screen
	# ESC -> Exit
	# WASD -> Directional Control

# Bugs:

	# no corner drag window resizing
	# aspect ratio gets warped

# Needs Improvement:

	# hardcoded -> player copy agent

	# standardize class capitalization

		# Class - for name of class
		# class - for instantiation

class simple_game:

	def __init__(self):

		parser = argparse.ArgumentParser()
		# --windowed
		parser.add_argument('--windowed',
				action='store_true',
				help='Starts game in windowed mode')
		args = parser.parse_args()


		# Percept config
		# shape of board vision per agent
		self.env_percept_shape = [3,3]
		# number of recent moves in percept
		self.move_memory = 1
		self.N_env_states 	= 3
		self.N_spatial_percepts	= np.prod(self.env_percept_shape)
		self.N_percepts 	= self.N_spatial_percepts + self.move_memory
		self.N_actions		= 5
		self.P_bases		= [self.N_env_states for _ in range(self.N_spatial_percepts)]+[self.N_actions for _ in range(self.move_memory)]

		self.FPS = 10
		self.capture_FPS = 30

		self.interface = Interface(args)

		# Neutral, Bad, Good
		self.resource_density = [.6,.2,.2]
		# self.resource_density = [0,0,1]


		self.init_pieces()

		self.init_board()


	def init_board(self):

		self.board = Board(self.resource_density)

		for piece in self.pieces:

			visible_coords = piece.get_visible_coords()

			for coord in visible_coords:

				self.board.set(coord)

	def iter(self):

		if self.interface.quit_flag:
			sys.exit()

		if self.interface.score_flag:
			self.show_score()
			self.interface.score_flag = False

		for piece in self.pieces:
			if not piece.isDead:
				P = self.get_percept(piece)
				piece.get_move(P,self.board)
				self.get_percept(piece) # Update Visible

		self.gen_clones()
		self.train_all()
		time.sleep(1/self.FPS)
		self.show_board()

	def gen_clones(self):

		for piece in self.pieces:

			if piece.MANA >= 5:
				piece.MANA -= 5
				self.pieces += [piece.copy()]


	def show_score(self):
		for line in self.get_score():
			print(line)

	def get_score(self):

		lines = []
		lines.append('Scores:')
		for piece in self.pieces:
			if piece.isHuman:
				PType = 'Human: '
			else:
				PType = 'AI:    '
			lines.append(PType+
				'HP: '+str(piece.HP)+
				'   MANA: '+str(piece.MANA))

		return(lines)

	def train_all(self):

		players = [piece for piece in self.pieces if piece.isHuman and not piece.isDead]
		agents = [piece for piece in self.pieces if not piece.isHuman and not piece.isDead]

		training_data = []
		for p in players:
			while not p.controller.training_queue.empty():
				training_data.append(p.controller.training_queue.get())

		for a in agents+players:
			for percept,action in training_data:
				a.controller.train(percept,action)

	def show_board(self):

		canvas = self.board.get_canvas()

		for piece in self.pieces:

			if not piece.isDead:

				coords = piece.get_visible_coords()
				for k in coords:
					k = str(k)

					coord = k[1:-1]
					coord = coord.split(',')
					coord = [int(coord[i]) for i in [0,1]]

					canvas[coord[0]-self.board.xmin,coord[1]-self.board.ymin] = self.board.at(coord)+1

		self.interface.put_frame(canvas)
		self.interface.textbox.put(self.get_score())


	def init_pieces(self):

		self.pieces = []

		self.init_player()

		# self.init_agent()

	def init_agent(self):

		# init agent (num percepts, num actions, bases)
		self.pieces += [Piece(agent(self.N_percepts,self.N_actions,self.P_bases),[0,0],self.move_memory) for _ in range(10)]

	def init_player(self):
		self.pieces += [Piece(player(self.interface,self.N_percepts,self.N_actions,self.P_bases),[0,0],self.move_memory)]

	def get_percept(self,piece):

		coords = piece.get_visible_coords()

		# Spatial Percept
		SP = np.zeros(len(coords))

		i = 0

		for coord in coords:

			self.board.set(coord)

			SP[i] = self.board.at(coord)

			i += 1

		# Temporal Percept
		TP = piece.move_memory_buffer

		P = np.hstack([SP,TP])

		return(P)

class Piece:

	def __init__(self,
				controller,
				location=[0,0],
				move_memory=0
				):

		self.location = np.array(location)

		self.HP = 10

		self.MANA = 0

		self.isDead = False

		self.move_memory_buffer = np.zeros(move_memory)

		# Controller has "get_move(P)" attribute
		self.controller = controller

		self.isHuman = False
		if 'player' in str(type(controller)):
			self.isHuman = True

		self.score = 0

	def copy(self):

		new_agent = Piece(self.controller.copy(),self.location,self.move_memory_buffer.shape[0])
		new_agent.MANA = self.MANA
		new_agent.HP = self.HP
		return(new_agent)

	def get_move(self,P,board):

		move_idx = self.controller.get_move(P)

		if self.isHuman:
			if self.controller.kill_flag:
				self.isDead = True

		# stop, up, down, left, right
		moves = [[0,0],[0,-1],[0,1],[-1,0],[1,0]]

		move = np.array(moves[move_idx])

		self.location += move

		stepping_on = board.at(self.location)

		if stepping_on == 1:
			self.HP -= 1
			board.set(self.location,0)
			if self.HP == 0:
				self.isDead = True

		if stepping_on == 2:
			self.MANA += 1
			board.set(self.location,0)

		self.move_memory_buffer[1:] = self.move_memory_buffer[:-1]
		self.move_memory_buffer[0] = move_idx

		return(move)

	def get_visible_coords(self):

		mods = [[-1,-1],[-1,0],[0,-1],[1,-1],[-1,1],[0,0],[1,0],[0,1],[1,1]]

		return([[self.location[0]+mod[0],self.location[1]+mod[1]] for mod in mods])


if __name__ == '__main__':

	G = simple_game()

	while 1:
		G.iter()



