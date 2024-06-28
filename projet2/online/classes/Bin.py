from .Item import Item
from .Gap import Gap
from decimal import *
from functools import reduce
from copy import deepcopy
from birdseye import eye
#from future_builtins import filter
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
		if self.dimensions == 2: g.dim[1] = Bin.dims[1]
		if self.dimensions == 3: g.dim[2] = Bin.dims[2]
		self.gaps = [g]
		self.selected_gap = g

	def __repr__(self):
		return f'<Bin dimensions:{self.dimensions} volume:{self.used_volume}/{self.total_volume} nb_items:{len(self.items)}>'

	def add_item(self, item, with_gap=False):
		if with_gap:
			self.remove_gap(self.selected_gap)
		if with_gap:
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
#				coll_list = list()
#				for it in self.items:
#					if it.overlaps(inf_item, pos, self.dimensions):
#						coll_list.append(it)
				res, _ = self.do_test_gap(coll_list, inf_item.dims)
				return res

	def remove_gap(self, gap):
#		print(self.gaps)
		self.gaps.remove(gap)
#		print(self.gaps)

	def is_empty(self):
		return len(self.items) == 0

	def get_remaining(self):
		return self.get_total_volume() - self.get_used_volume()

#	@eye
	def opti3(self, new_item, pos=None):
		if not self.items:
			g = Gap(self.dimensions)
			g.dim[0] = Bin.dims[0]
			g.dim[1] = Bin.dims[1]
			if self.dimensions == 3: g.dim[2] = Bin.dims[2]
			self.gaps = [g]
			return
		gaps = deepcopy(self.gaps)
		items_done = deepcopy(self.items)
		items_tri = sorted(self.items, key=lambda item: item.dims[0] + item.position[0]) # From: https://stackoverflow.com/a/403426
#		print(self.items[0].position)
#		for new_item in items_tri:
		for d in range(1, self.dimensions):
			if items_done:
				pseudo_item = deepcopy(new_item)
#					if pos:
#						pseudo_item.position = pos
				max_pos = max([item.position[d-1] + item.dims[d-1] for item in items_done])
				pseudo_item.position[0] = max_pos if max_pos + pseudo_item.position[0]+pseudo_item.dims[0] <= Bin.dims[0] else pseudo_item.position[0] # Test is guardrail
#				pseudo_item.position[d-1] = max_pos
				item_test = pseudo_item
			else:
				item_test = deepcopy(new_item)
#					if pos:
#						item_test.position = pos
			item_test.dims[d] = Decimal('Infinity')
#				print(item_test.position)
			items_coll = item_test.get_collisions(items_tri, item_test.position, self.dimensions) # items_tri could also be self.items, it's irrelevant
			occupied = sum([item.dims[d] for item in items_coll])
			if occupied <= Bin.dims[d]:
				new_gaps = list()
				find_gap(new_gaps, item_test, items_coll, Decimal('0'), self.dims[d], self.dimensions, d)
				for gap in new_gaps:
					gap.pos[d-1] = item_test.position[d-1] # y value might be changed in merge, can't remember
					gap.dim[d-1] = item_test.dims[d-1]
#				print(new_gaps)
				gaps.extend(new_gaps)
#					for g in gaps:
#						print(g)
#					print(toto)
			#else:
			#	return # No more space :(
		items_done.append(new_item)
		t = items_tri[-1]
#		print(gaps)
#		print(self.gaps)
#		print(self.selected_gap)
#		print(toto)
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


# TODO: move to somewhere smart
#@eye
def find_gap(gaps, item, items_coll, border_min=Decimal('0'), border_max=Decimal('0'), dimension=2, current_d=1): # TODO to n-dimensions (is easy)
	items_coll_prev = [it for it in items_coll if it.position[current_d] < item.position[current_d]]
	items_coll_post = [it for it in items_coll if it.position[current_d] > item.position[current_d]+item.dims[current_d]]
	i_c_p = [items_coll_prev, items_coll_post]
#	print(i_c_p)
	for i in range(len(i_c_p)):
#		print('?', i_c_p[i])
		if not i_c_p[i]:
#			print(border_min, border_max)
			#if border_max - border_min >= Decimal('0.01'): # Precision max for items
			if border_max - border_min > Decimal('0'):
				gap = Gap(dimension)
				gap.pos[current_d] = border_min
				gap.dim[current_d] = border_max - border_min
				gaps.append(gap)
#				print(1, gap)
#				print(2, gaps)
		else:
#			print(sum([it.dims[current_d] for it in i_c_p[i]]))
#			print(item.position[current_d])
#			print(i, item.dims[current_d])
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
#	print(gaps)

#@eye
def merge(gaps, items, dimension):
	for d in range(dimension):
		dropped = set()
		#for gap1, gap2 in filter(dropped.isdisjoint, itertools.combinations(gaps, 2)): # Combinations: https://stackoverflow.com/a/16603357 | Filter: https://stackoverflow.com/a/39240343
		done_looping = False
		gaps_removed = False
		while not done_looping:
		#for gap1, gap2 in itertools.combinations(gaps, 2): # Combinations: https://stackoverflow.com/a/16603357
#			print(gaps)
#			print(len(gaps))
			if len(gaps) == 1:
				done_looping = True
			for i in range(len(gaps)):
#				print('i', i)
#				print('len', len(gaps))
				gap1 = gaps[i]
	#			print(i)
				for j in range(i+1, len(gaps)):
					gap2 = gaps[j]
#					print(j)
	#				print('in1')
					if gap1.dim[d] == gap2.dim[d] and gap1.pos[d] == gap2.pos[d]: # Can merge
	#					print('in2')
						pseudo_item = Item(-1, 'Pseudo_item', 0, 0, 0)
						pseudo_item.dims[d] = gap1.dim[d]
						pseudo_item.position[d] = gap1.pos[d]
						for not_d in [d_ for d_ in range(dimension) if d_ != d]:
			#					print('Gap1', gap1.pos)
			#					print('Gap2', gap2.pos)
			#					print('ps.pos', pseudo_item.position)
			#					print('Not_d', not_d)
		#					print(gap1.pos)
		#					print(gap2.pos)
		#					print(not_d)
							pseudo_item.position[not_d] = min(gap1.pos[not_d], gap2.pos[not_d])
							#pseudo_item.dims[not_d] = max(gap1.pos[not_d]+gap1.dim[not_d], gap2.pos[not_d]+gap2.dim[not_d])-pseudo_item.position[not_d]
							pseudo_item.dims[not_d] = max(gap1.pos[not_d]+gap1.dim[not_d], gap2.pos[not_d]+gap2.dim[not_d])-pseudo_item.position[not_d]
						if not pseudo_item.get_collisions(items, pseudo_item.position, dimension): # Can merge :)
							done_looping = False
							gaps_removed = True
							gaps.remove(gap1) # does break `combinations`
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

@eye
def extend(gaps, items, dimension):
	for i in range(len(gaps)):
		item_test = Item(-1, 'Item_test', 0, 0, 0)
		item_test.position = gaps[i].pos.copy()
		item_test.dims = gaps[i].dim.copy()
		print('GGGGGGGGGGGGG', gaps[i])
		for d in range(dimension):
			item_test.dims[d] = Decimal('Infinity')
			items_coll = item_test.get_collisions(items, item_test.position, dimension)
			if not items_coll:
				item_test.position[d] = 0 # 0 is min of Bin
				item_test.dims[d] = Bin.dims[d]
			else:
				mid_point = (item_test.position[d]+item_test.dims[d]) / 2 # mid_point of item
				closest = sorted([it for it in items_coll], key=lambda it: abs(it.position[1] - mid_point))
				is_trapped = len(closest) >= 2
				is_below = closest[0].position[d]-mid_point < 0
				print(closest)
				print(is_below)
#				item_test.position[d] = min(closest[0].position[d], closest[1].position[d])
#				item_test.dims[d] = max(closest[0].position[d]+closest[0].dims[d], closest[1].pos[not_d]+closest[1].dim[not_d])-item_test.pos[not_d]
				item_test.position[d] = closest[0].position[d]+closest[0].dims[d] if is_trapped else (closest[0].position[d]+closest[0].dims[d] if is_below else 0)
				item_test.dims[d] = (closest[int(is_trapped)].position[d] if is_trapped else (closest[0].position[d] if not is_below else Bin.dims[d]))-item_test.position[d]
				print('item_test', item_test)
		gaps[i].pos = item_test.position[:dimension].copy()
		gaps[i].dim = item_test.dims[:dimension].copy()
