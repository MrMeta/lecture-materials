import pygame
from random import shuffle
"""Contains the Maze class which is the array-represented maze."""


class Maze:
	def __init__(self, rows=30, cols=40):
		self.rows = rows
		self.cols = cols
		self.keep_going = 1

		self.maze = {}
		for y in range(rows):
			for x in range(cols):
				cell = {'south': 1, 'east': 1, 'visited': 0}
				self.maze[(x, y)] = cell

	def generate(self, stack=[]):
		"""Generates a random maze using a magical simple recursive function."""

		if not self.keep_going:
			return

		self.check_finished()

		# if the stack is empty, add the start cell
		if len(stack) == 0:
			stack.append(self.maze[(0, 0)])

		# set current cell to last cell
		curr_cell = stack[-1]

		# get neighbors and shuffle 'em up a bit
		neighbors = self.get_neighbors(curr_cell)
		shuffle(neighbors)

		for neighbor in neighbors:
			if neighbor['visited'] == 0:
				neighbor['visited'] = 1
				stack.append(neighbor)
				self.knock_wall(curr_cell, neighbor)

				self.generate(stack)

	def get_coords(self, cell):
		# grabs coords of a given cell
		coords = (-1, -1)
		for k in self.maze:
			if self.maze[k] is cell:
				coords = (k[0], k[1])
				break
		return coords

	def get_neighbors(self, cell):
		# obvious
		neighbors = []

		(x, y) = self.get_coords(cell)
		if (x, y) == (-1, -1):
			return neighbors

		north = (x, y-1)
		south = (x, y+1)
		east = (x+1, y)
		west = (x-1, y)
		
		if north in self.maze:
			neighbors.append(self.maze[north])
		if south in self.maze:
			neighbors.append(self.maze[south])
		if east in self.maze:
			neighbors.append(self.maze[east])
		if west in self.maze:
			neighbors.append(self.maze[west])

		return neighbors

	def knock_wall(self, cell, neighbor):
		# knocks down wall between cell and neighbor.
		xc, yc = self.get_coords(cell)
		xn, yn = self.get_coords(neighbor)

		# Which neighbor?
		if xc == xn and yc == yn + 1:
			# neighbor's above, knock out south wall of neighbor
			neighbor['south'] = 0
		elif xc == xn and yc == yn - 1:
			# neighbor's below, knock out south wall of cell
			cell['south'] = 0
		elif xc == xn + 1 and yc == yn:
			# neighbor's left, knock out east wall of neighbor
			neighbor['east'] = 0
		elif xc == xn - 1 and yc == yn:
			# neighbor's right, knock down east wall of cell
			cell['east'] = 0

	def check_finished(self):
		# Checks if we're done generating
		done = 1
		for k in self.maze:
			if self.maze[k]['visited'] == 0:
				done = 0
				break
		if done:
			self.keep_going = 0


def draw_maze(screen, maze):
	screen.fill((255, 255, 255))
	size = pygame.display.get_surface().get_size()
	cell_width = size[0] / maze.cols
	cell_height = size[1] / maze.rows

	for y in range(maze.rows):
		for x in range(maze.cols):
			if maze.maze[(x, y)]['south']:  # draw south wall
				pygame.draw.line(screen, (0, 0, 0),
								(x * cell_width, y * cell_height + cell_height),
								(x * cell_width + cell_width, y * cell_height + cell_height))
			if maze.maze[(x, y)]['east']:  # draw east wall
				pygame.draw.line(screen, (0, 0, 0),
								(x * cell_width + cell_width, y * cell_height),
								(x * cell_width + cell_width, y * cell_height + cell_height))
	# Screen border
	pygame.draw.rect(screen, (0, 0, 0), (0, 0, size[0], size[1]), 1)
