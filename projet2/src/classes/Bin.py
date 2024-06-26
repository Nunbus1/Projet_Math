#!/usr/bin/python3
from .Item import Item
from decimal import *
from functools import reduce


class Bin:
	x = Decimal("11.583")
	y = Decimal("2.294")
	z = Decimal("2.569")
	dims = (x, y, z)

	def __init__(self, dimensions, items, contains_liquid=True):
		self.dimensions = dimensions
		self.items = items
		self.contains_liquid = contains_liquid
		self.used_volume = Decimal(sum([reduce(lambda x, y: x*y, item.dims[:self.dimensions]) for item in self.items]))
		self.total_volume = Decimal(reduce(lambda x, y: x*y, self.dims[:self.dimensions]))

	def __repr__(self):
		return f"<Bin dimensions:{self.dimensions} volume:{self.used_volume}/{self.total_volume} nb_items:{len(self.items)}>"

	def add_item(self, item):
		self.items.append(item)
		self.used_volume += item.get_volume(self.dimensions)

	def get_items(self):
		return self.items

	def get_total_volume(self):
		return self.total_volume

	def get_used_volume(self):
		return self.used_volume

	def can_fit(self, new_item, pos=None, overrides_liquid=False):
		if self.contains_liquid or overrides_liquid:
			return (self.used_volume + new_item.get_volume(self.dimensions) < self.total_volume,)
		else:
			for it in self.items:
				if it.overlaps(new_item, pos, self.dimensions):
					return False
			res = True
			for i in range(self.dimensions):
				res = res and pos[i] + new_item.dims[i] <= self.dims[i]
			return res

	def is_empty(self):
		return len(self.items) == 0

	def get_remaining(self):
		return self.get_total_volume() - self.get_used_volume()
