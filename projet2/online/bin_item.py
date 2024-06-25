#!/usr/bin/python3
from decimal import *
from functools import reduce
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
	dims = (x, y, z)
	#box = fcl.Box(x, y, z)

	def __init__(self, dimensions, items=list(), bb=list()):
		self.dimensions = dimensions
		self.items = items
		self.is_open = True
		self.used_volume = Decimal(sum([reduce(lambda x, y: x*y, item.dims[:self.dimensions]) for item in self.items]))
		self.total_volume = Decimal(reduce(lambda x, y: x*y, self.dims[:self.dimensions]))

	def __repr__(self):
		return f"<Bin dimensions:{self.dimensions} is_open:{self.is_open}>"

	def add_item(self, item):
		self.items.append(item)
		self.used_volume += Decimal(reduce(lambda x, y: x*y, item.dims[:self.dimensions]))

	def get_items(self):
		return self.items

	def get_total_volume(self):
		return self.total_volume

	def get_used_volume(self):
		return self.used_volume

	def can_fit(self, new_item):
		return self.get_used_volume() + Decimal(reduce(lambda x, y: x*y, new_item.dims[:self.dimensions])) < self.get_total_volume()

	def is_empty(self):
		return len(self.items) == 0

	def get_remaining(self):
		return self.get_total_volume() - self.get_used_volume()
