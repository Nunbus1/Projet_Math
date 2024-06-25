#!/usr/bin/python3
from decimal import *
import numpy as np
#import fcl

class Item:
	def __init__(self, numero, nom, x, y=None, z=None):
		self.numero = numero
		self.nom = nom
		self.x = x
		self.y = y
		self.z = z
		self.dims = [x]
		if y != None: self.dims.append(y)
		if z != None: self.dims.append(z)

	def __repr__(self):
		return f"<Item[{self.numero}] '{self.nom}' ({self.x}, {self.y}, {self.z})>"

class Bin:
	x = Decimal("11.583")
	y = Decimal("2.294")
	z = Decimal("2.569")
	#box = fcl.Box(x, y, z)

	def __init__(self, dimensions, items=list(), bb=list()):
		self.dimensions = dimensions
		self.items = items
		self.items_bb = bb
		self.is_open = True

	def __repr__(self):
		return f"<Bin dimensions:{self.dimensions} is_open:{self.is_open}>"

	def add_item(self, item):
		self.items.append(item)

	def get_items(self):
		return self.items

	def can_fit(self, new_item):
		return sum([sum(item.dims) for item in self.items]) + sum(new_item.dims) < product
#		if self.dimensions == 1:
#			return sum([item.x for item in self.items]) + new_item.x < self.x
#		elif self.dimensions == 2:
#			return sum([item.x * item.y for item in self.items]) + new_item.x*new_item.y < self.x*self.y
#		elif self.dimensions == 3:
#			return sum([item.x * item.y * item.z for item in self.items]) + new_item.x*new_item.y*new_item.z < self.x*self.y*self.z
#		else:
#			return "ERROR"

	def is_empty(self):
		return len(self.items) == 0

	def remaining_space(self):
		return
