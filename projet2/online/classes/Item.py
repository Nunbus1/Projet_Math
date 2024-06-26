#!/usr/bin/python3
from decimal import *
from functools import reduce


class Item:
	def __init__(self, numero, nom, x, y, z):
		self.numero = numero
		self.nom = nom
		self.x = x
		self.y = y
		self.z = z
		self.dims = (x, y, z)
		self.position = [None, None, None]

	def set_position(self, position):
		self.position = position

	def get_volume(self, dim_cut):
		return Decimal(reduce(lambda x, y: x*y, self.dims[:dim_cut]))

	def get_position(self):
		return self.position

	def overlaps(self, item, pos, dimension):
		res = False
		for i in range(dimension):
			res = res or (pos[i] + item.dims[i] <= self.position[i] or self.position[i] + self.dims[i] <= pos[i])
		return not res

	def __repr__(self):
		return f"<Item[{self.numero}] '{self.nom}' ({self.x}, {self.y}, {self.z})>"
