from agent import *
from player import *
from interface import *
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

class simple_game:

	def __init__(self,resource_density=[.6,.2,.2]):

		parser = argparse.ArgumentParser()
		# --windowed
		parser.add_argument('--windowed',
				action='store_true',
				help='Starts game in windowed mode')
		args = parser.parse_args()

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

		canvas = np.zeros([self.xmax-self.xmin,self.ymax-self.ymin])

		# for k in self.board.keys():
		for piece in self.pieces:

			if not piece.isDead:

				coords = piece.get_visible_coords()
				for k in coords:
					k = str(k)

					coord = k[1:-1]
					coord = coord.split(',')
					coord = [int(coord[i]) for i in [0,1]]

					canvas[coord[0]-self.xmin,coord[1]-self.ymin] = self.board[k]+1

		self.interface.put_frame(canvas)
		self.interface.textbox.put(self.get_score())


	def init_pieces(self):

		self.pieces = []

		self.init_player()

		# self.init_agent()

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

		self.HP = 10

		self.MANA = 0

		self.isDead = False


		# Controller has "get_move(P)" attribute
		self.controller = controller

		self.isHuman = False
		if 'player' in str(type(controller)):
			self.isHuman = True

		self.score = 0

	def copy(self):

		new_agent = Piece(self.controller.copy(),self.location)
		new_agent.MANA = self.MANA
		new_agent.HP = self.HP
		return(new_agent)

	def get_move(self,P,board):
		move_idx = self.controller.get_move(P)

		# stop, up, down, left, right
		# moves = [[0,0],[-1,0],[1,0],[0,-1],[0,1]]
		moves = [[0,0],[0,-1],[0,1],[-1,0],[1,0]]

		move = np.array(moves[move_idx])

		self.location += move

		key = str(list(self.location))		
		stepping_on = board[key]

		if stepping_on == 1:
			self.HP -= 1
			board[key] = 0
			if self.HP == 0:
				self.isDead = True

		if stepping_on == 2:
			self.MANA += 1
			board[key] = 0

		return(move)

	def get_visible_coords(self):

		mods = [[-1,-1],[-1,0],[0,-1],[1,-1],[-1,1],[0,0],[1,0],[0,1],[1,1]]

		return([[self.location[0]+mod[0],self.location[1]+mod[1]] for mod in mods])


G = simple_game()

while 1:
	G.iter()



