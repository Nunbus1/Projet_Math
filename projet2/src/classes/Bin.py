from .Item import Item
from .Gap import Gap
from decimal import *
from functools import reduce
from copy import deepcopy
import itertools


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
		g = Gap(self.dimensions)
		g.dim[0] = Bin.dims[0]
		if self.dimensions >= 2: g.dim[1] = Bin.dims[1]
		if self.dimensions == 3: g.dim[2] = Bin.dims[2]
		self.gaps = [g]
		self.selected_gap = g

	def add_item(self, item, with_gap=False):
		if with_gap and self.dimensions != 1 and not self.contains_liquid:
			self.remove_gap(self.selected_gap)
			self.opti3(item)
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
				coll_list = inf_item.get_collisions(self.items, pos, self.dimensions)
				res, _ = self.do_test_gap(coll_list, inf_item.dims)
				return res

	def remove_gap(self, gap):
		self.gaps.remove(gap)

	def is_empty(self):
		return len(self.items) == 0

	def get_remaining(self):
		return self.get_total_volume() - self.get_used_volume()

	def opti3(self, new_item_, pos=None):
		self.gaps = list()
		gaps = list()
		items_done = deepcopy(self.items)
		items_tri = sorted(self.items+[new_item_], key=lambda item: item.dims[0] + item.position[0]) # From: https://stackoverflow.com/a/403426
		for new_item in items_tri:
			for d in range(1, self.dimensions):
				if items_done:
					pseudo_item = deepcopy(new_item)
					max_pos = max([item.position[d-1] + item.dims[d-1] for item in items_done])
					pseudo_item.position[0] = max_pos if max_pos + pseudo_item.position[0]+pseudo_item.dims[0] <= Bin.dims[0] else pseudo_item.position[0] # Test is guardrail
					item_test = pseudo_item
				else:
					item_test = deepcopy(new_item)
				item_test.dims[d] = Decimal('Infinity')
				items_coll = item_test.get_collisions(items_tri, item_test.position, self.dimensions) # items_tri could also be self.items, it's irrelevant
				occupied = sum([item.dims[d] for item in items_coll])
				if occupied <= Bin.dims[d]:
					new_gaps = list()
					find_gap(new_gaps, item_test, items_coll, Decimal('0'), self.dims[d], self.dimensions, d)
					for gap in new_gaps:
						gap.pos[d-1] = item_test.position[d-1]
						gap.dim[d-1] = item_test.dims[d-1]
					gaps.extend(new_gaps)
			items_done.append(new_item)
			t = items_tri[-1]
			if t.position[0] + t.dims[0] <= Bin.dims[0]:
				g = Gap(self.dimensions)
				g.pos[0] = t.position[0] + t.dims[0]
				g.dim[0] = Bin.dims[0] - g.pos[0]
				g.dim[1] = Bin.dims[1]
				if self.dimensions == 3: g.dim[2] = Bin.dims[2]
				if self.dimensions == 3: g.pos[2] = Decimal('0')
				gaps.append(g)
		merge(gaps, items_tri, self.dimensions)
		extend(gaps, items_tri, self.dimensions)
		self.gaps = deepcopy(gaps)

	def __repr__(self):
		return f'<Bin dimensions:{self.dimensions} volume:{self.used_volume}/{self.total_volume} nb_items:{len(self.items)}>'


def find_gap(gaps, item, items_coll, border_min=Decimal('0'), border_max=Decimal('0'), dimension=2, current_d=1): # TODO to n-dimensions (is easy)
	items_coll_prev = [it for it in items_coll if it.position[current_d] < item.position[current_d]]
	items_coll_post = [it for it in items_coll if it.position[current_d] > item.position[current_d]+item.dims[current_d]]
	i_c_p = [items_coll_prev, items_coll_post]
	for i in range(len(i_c_p)):
		if not i_c_p[i]:
			if border_max - border_min > Decimal('0'):
				gap = Gap(dimension)
				gap.pos[current_d] = border_min
				gap.dim[current_d] = border_max - border_min
				gaps.append(gap)
		else:
			if not i:
				i_d_curr = 0
			else:
				i_d_curr = item.dims[current_d]
			if sum([it.dims[current_d] for it in i_c_p[i]]) < item.position[current_d] + i_d_curr: # Gap present
				if i == 0:
					mid_point = item.position[current_d] / 2
					closest_item = sorted([it for it in items_coll], key=lambda it: abs(it.position[current_d] - mid_point))[0]
					find_gap(gaps, closest_item, i_c_p[i], border_min, item.position[current_d], dimension, current_d)
				else:
					mid_point = (Bin.dims[current_d] - (item.position[current_d]+item.dims[current_d])) / 2
					closest_item = sorted([it for it in items_coll], key=lambda it: abs(it.position[current_d] - mid_point))[0]
					find_gap(gaps, closest_item, i_c_p[i], item.position[current_d]+item.dims[current_d], border_max, dimension, current_d)

def merge(gaps, items, dimension):
	for d in range(dimension):
		dropped = set()
		done_looping = False
		gaps_removed = False
		while not done_looping:
			if len(gaps) == 1:
				done_looping = True
			for i in range(len(gaps)):
				gap1 = gaps[i]
				for j in range(i+1, len(gaps)):
					gap2 = gaps[j]
					if gap1.dim[d] == gap2.dim[d] and gap1.pos[d] == gap2.pos[d]: # Can merge
						pseudo_item = Item(-1, 'Pseudo_item', 0, 0, 0)
						pseudo_item.dims[d] = gap1.dim[d]
						pseudo_item.position[d] = gap1.pos[d]
						for not_d in [d_ for d_ in range(dimension) if d_ != d]:
							pseudo_item.position[not_d] = min(gap1.pos[not_d], gap2.pos[not_d])
							pseudo_item.dims[not_d] = max(gap1.pos[not_d]+gap1.dim[not_d], gap2.pos[not_d]+gap2.dim[not_d])-pseudo_item.position[not_d]
						if not pseudo_item.get_collisions(items, pseudo_item.position, dimension): # Can merge :)
							done_looping = False
							gaps_removed = True
							gaps.remove(gap1)
							gaps.remove(gap2)
							dropped.update((gap1, gap2))
							merged_gap = Gap(dimension, pseudo_item.position.copy(), pseudo_item.dims.copy())
							gaps.append(merged_gap)
							break
						else:
							done_looping = True
							gaps_removed = False
					else:
						done_looping = True
						gaps_removed = False
				if gaps_removed:
					break

def extend(gaps, items, dimension):
	for i in range(len(gaps)):
		item_test = Item(i, 'Item_test', 0, 0, 0)
		item_test.position = gaps[i].pos.copy()
		item_test.dims = gaps[i].dim.copy()
		for d in range(dimension):
			item_test.dims[d] = Decimal('Infinity')
			items_coll = item_test.get_collisions(items, item_test.position, dimension)
			if not items_coll:
				item_test.position[d] = 0 # 0 is min of Bin
				item_test.dims[d] = Bin.dims[d]
			else:
				mid_point = (item_test.position[d]+item_test.dims[d]) / 2 # mid_point of item
				closest = sorted([it for it in items_coll], key=lambda it: abs(it.position[d] - mid_point))
				has_below = any([it.position[d]-mid_point<0 for it in closest])
				has_above = any([it.position[d]-mid_point>0 for it in closest])
				is_trapped = has_below and has_above
				is_below = closest[0].position[d]-mid_point < 0
				item_test.position[d] = closest[0].position[d]+closest[0].dims[d] if is_trapped else (closest[0].position[d]+closest[0].dims[d] if is_below else 0)
				item_test.dims[d] = (closest[int(is_trapped)].position[d] if is_trapped else (closest[0].position[d] if not is_below else Bin.dims[d]))-item_test.position[d]
		gaps[i].pos = item_test.position[:dimension].copy()
		gaps[i].dim = item_test.dims[:dimension].copy()
