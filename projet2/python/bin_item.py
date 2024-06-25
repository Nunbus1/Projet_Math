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
	#box = fcl.Box(x, y, z)

	def __init__(self, dimensions, items=list(), bb=list()):
		self.dimensions = dimensions
		self.items = items
		self.is_open = True
		self.dims = [self.x]
		if dimensions >= 2: self.dims.append(self.y)
		if dimensions >= 3: self.dims.append(self.z)

	def __repr__(self):
		return f"<Bin dimensions:{self.dimensions} is_open:{self.is_open}>"

	def add_item(self, item):
		self.items.append(item)

	def get_items(self):
		return self.items

	def can_fit(self, new_item):
		#t= (sum([reduce(lambda x, y: x*y, item.dims) for item in self.items]) + reduce(lambda x, y: x*y, new_item.dims), reduce(lambda x, y: x*y, self.dims))
		if self.dimensions == 1:
			t2= (sum([item.x for item in self.items]) + new_item.x, self.x)
#			if t != t2:
#				print(self.dims)
#				print(self.items)
#				print(t, t2)
			return t2[0] < t2[1]
		elif self.dimensions == 2:
			t2= (sum([item.x * item.y for item in self.items]) + new_item.x*new_item.y, self.x*self.y)
#			if t != t2:
#				print(t, t2)
			return t2[0] < t2[1]
		elif self.dimensions == 3:
			t2= (sum([item.x * item.y * item.z for item in self.items]) + new_item.x*new_item.y*new_item.z, self.x*self.y*self.z)
#			if t != t2:
#				print(t, t2)
			return t2[0] < t2[1]
		else:
			return "ERROR"

	def is_empty(self):
		return len(self.items) == 0
