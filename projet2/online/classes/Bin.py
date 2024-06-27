from .Item import Item
from decimal import *
from functools import reduce
from copy import deepcopy


class Bin:
	x = Decimal('11.583')
	y = Decimal('2.294')
	z = Decimal('2.569')
	dims = [x, y, z]

	def __init__(self, dimensions, items, contains_liquid=True):
		self.dimensions = dimensions
		self.items = items
		self.contains_liquid = contains_liquid
		self.used_volume = Decimal(sum([reduce(lambda x, y: x*y, item.dims[:self.dimensions]) for item in self.items]))
		self.total_volume = Decimal(reduce(lambda x, y: x*y, self.dims[:self.dimensions]))

	def __repr__(self):
		return f'<Bin dimensions:{self.dimensions} volume:{self.used_volume}/{self.total_volume} nb_items:{len(self.items)}>'

	def add_item(self, item):
		self.items.append(item)
		self.used_volume += item.get_volume(self.dimensions)

	def get_items(self):
		return self.items

	def get_total_volume(self):
		return self.total_volume

	def get_used_volume(self):
		return self.used_volume

	def do_test_gap(self, items, item_dims):
		for it in items:
			if not it.test_gap(self.dims, item_dims, self.dimensions):
				return False, it # Doesn't fit in gap
		return True, None # Fits in gap

	def can_fit(self, new_item, pos=None, overrides_liquid=False, is_infinite=False):
		if self.contains_liquid or overrides_liquid:
			return (self.used_volume + new_item.get_volume(self.dimensions) < self.total_volume,)
		else:
			if not is_infinite:
				for it in self.items:
					if it.overlaps(new_item, pos, self.dimensions):
						return False
				res = True
				for i in range(self.dimensions):
					res = res and pos[i] + new_item.dims[i] <= self.dims[i]
				return res
			else:
				inf_item = deepcopy(new_item)
				inf_item.dims[0] = Decimal('Infinity')
				coll_list = list()
				for it in self.items:
					if it.overlaps(inf_item, pos, self.dimensions):
						coll_list.append(it)
				res, _ = self.do_test_gap(coll_list, inf_item.dims)
				return res

	def is_empty(self):
		return len(self.items) == 0

	def get_remaining(self):
		return self.get_total_volume() - self.get_used_volume()
