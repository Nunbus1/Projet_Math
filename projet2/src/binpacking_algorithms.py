from classes.Item import Item
from classes.Gap import Gap
from classes.Bin import Bin
from copy import deepcopy
from math import floor
from birdseye import eye
from decimal import *
from functools import reduce
import multiprocessing as mp
import itertools
import settings


# UTILS
def drange(x, y, jump): # From: https://stackoverflow.com/a/7267280
	while x < y:
		yield x
		x += jump

def auto_turn(item, gap=None): # OPT 1
	dimension, contains_liquid, _, _, _, opti = settings.get_all()
	if (1 not in opti and gap != None) and (3 not in opti and gap == None):
		return False
	if dimension == 1 or contains_liquid:
		return False
	esb, egi = list(), list() # Espace, Smallest/Greatest, Bin/Item
	if not gap:
		eb = Bin.dims[:dimension].copy()
	else:
		eb = gap.dim[:dimension].copy()
	ei = item.dims[:dimension].copy()
	for d in range(dimension-1):
		if not gap:
			sb = min(eb[:dimension])
		else:
			sb = max(eb[:dimension])
		gi = max(ei[:dimension])
		esb.append(sb)
		egi.append(gi)
		eb.remove(sb)
		ei.remove(gi)
	if reduce(lambda x, y: x*y, egi) > reduce(lambda x, y: x*y, esb):
		return False
	if not gap:
		eb = Bin.dims[:dimension].copy()
	else:
		eb = gap.dim[:dimension].copy()
	ei = item.dims[:dimension].copy()
	s_indexes, g_indexes = list(), list()
	for d in range(dimension-1):
		s_indexes.append(eb.index(esb[d]))
		g_indexes.append(ei.index(egi[d]))
		eb[s_indexes[-1]] = Decimal('Infinity')
		ei[g_indexes[-1]] = Decimal('Infinity')
	s_indexes.sort()
	g_indexes.sort()
	if s_indexes == g_indexes: # Colinéaires
		return True
	missing = list()
	missing.append([m for m in range(3) if m not in g_indexes][0])
	missing.append([m for m in range(3) if m not in s_indexes][0])
	a = item.dims[missing[1]]
	for d in range(len(s_indexes)):
		item.dims[g_indexes[d]] = item.dims[s_indexes[d]]
	item.dims[missing[0]] = a
	return True

def try_place(current_bin, item):
	dimension, contains_liquid, mlt_proc, resolution, is_offline, opti = settings.get_all()
	if dimension != 1 and not contains_liquid:
		if 3 in opti:
			gaps = current_bin.gaps
			sorted_gaps = sorted([gap for gap in current_bin.gaps], key=lambda gap: gap.get_volume())
			for gap in sorted_gaps:
				pseudo_item = deepcopy(item)
				if gap.get_volume() >= pseudo_item.get_volume(dimension):
					res = auto_turn(pseudo_item, gap)
					if res:
						can_fit = current_bin.can_fit(pseudo_item, gap.pos, False, True)
						if can_fit and all([gap.dim[i] >= pseudo_item.dims[i] for i in range(dimension)]):
							current_bin.selected_gap = gap
							return (True, gap.pos, pseudo_item.dims)
			return (False,)
		else:
			def travel_axis(current_binn, itemm, dim, pos):
				if dim == 0:
					if current_binn.can_fit(itemm, pos):
						if not is_offline:
							if current_binn.can_fit(itemm, pos, False, True):
								return (True, pos)
							else:
								return (False,)
						return (True, pos)
					else:
						return (False,)
				n_pos = pos.copy()
				n_pos.append(0)
				i_start = Decimal('0')
				if 2 in opti:
					if dimension-dim+1 == 1: # OPT 2
						items_test = current_bin.items.copy()
						while items_test != []:
							fits, it = current_binn.do_test_gap(items_test, itemm.dims)
							if not fits:
								i_start += it.position[0]
								try:
									items_test.remove(it)
								except ValueError:
									pass
							else:
								break
				for i in drange(i_start, current_binn.dims[dimension-dim]-itemm.dims[dimension-dim]+1, resolution):
					n_pos[-1] = i
					res = travel_axis(current_binn, itemm, dim-1, n_pos)
					if res[0]:
						return res
				return (False,)
			pseudo_item = deepcopy(item)
			cut_dim = pseudo_item.dims[:dimension]
			for dims in itertools.permutations(cut_dim):
				dims = list(dims)
				pseudo_item.dims = dims
				if dimension == 2: pseudo_item.dims.append(item.dims[2])
				res = travel_axis(current_bin, pseudo_item, dimension, [])
				if res[0]:
					return (res[0], res[1], dims)
			return (res[0], None, None)
	else:
		return current_bin.can_fit(item, None, True)


# Algorithmes
def next_fit(items):
	dimension, contains_liquid, mlt_proc, _, _, opti = settings.get_all()
	bins = list()
	bin_i = 0
	bins.append(Bin(dimension, list(), contains_liquid))
	with_gap = 3 in opti
	for item in items:
		if 1 in opti: auto_turn(item)
		res = try_place(bins[bin_i], item)
		if res[0]:
			item.set_position(res)
			item.set_dims(res)
			bins[bin_i].add_item(item, with_gap)
		else:
			item.set_position((None,[0]*dimension))
			bins.append(Bin(dimension, list(), contains_liquid))
			bins[-1].add_item(item, with_gap)
			bin_i += 1
	return bins

def first_fit(items):
	dimension, contains_liquid, mlt_proc, _, _, opti = settings.get_all()
	with_gap = 3 in opti
	def use_result(bins, i, item, result):
		placed = result[0]
		if placed:
			item.set_position(result)
			item.set_dims(result)
			bins[i].add_item(item, with_gap)
		return placed

	bins = list()
	bins.append(Bin(dimension, list(), contains_liquid))
	mlt_cond = mlt_proc and dimension != 1
	if mlt_cond:
		batch_size = 4*mp.cpu_count()
		pool = mp.Pool()
	for item in items:
		if 1 in opti: auto_turn(item)
		placed = False
		if mlt_cond:
			i=0
			for result in pool.starmap(try_place, [(b, item) for b in bins], chunksize=4):
				placed = use_result(bins, i, item, result)
				i += 1
				if placed:
					break
		else:
			i=0
			for b in bins:
				result = try_place(b, item)
				placed = use_result(bins, i, item, result)
				i += 1
				if placed:
					break
		if not placed:
			item.set_position((None,[0]*dimension))
			bins.append(Bin(dimension, list(), contains_liquid))
			bins[-1].add_item(item, with_gap)
	if mlt_cond:
		pool.close()
		pool.join()

	return bins

def best_fit(items):
	dimension, contains_liquid, mlt_proc, _, _, opti = settings.get_all()
	with_gap = 3 in opti
	def use_result(bins, i, best_bin, result):
		if result[0] and (best_bin is None or bins[i].get_used_volume() < best_bin.get_used_volume()):
			return bins[i], result
		else:
			return (False,)

	bins = list()
	bins.append(Bin(dimension, list(), contains_liquid))
	mlt_cond = mlt_proc and dimension != 1
	if mlt_cond:
		batch_size = 4*mp.cpu_count()
		pool = mp.Pool()
	for item in items:
		if 1 in opti: auto_turn(item)
		best_bin = None
		best_res = None
		if mlt_cond:
			i=0
			for result in pool.starmap(try_place, [(b, item) for b in bins], chunksize=4):
				best = use_result(bins, i, best_bin, result)
				if best[0] != False:
					best_bin, best_res = best
				i += 1
		else:
			for i in range(len(bins)):
				result = try_place(bins[i], item)
				best = use_result(bins, i, best_bin, result)
				if best[0] != False:
					best_bin, best_res = best
		if best_bin is None:
			item.set_position((None,[0]*dimension))
			new_bin = Bin(dimension, list(), contains_liquid)
			new_bin.add_item(item, with_gap)
			bins.append(new_bin)
		else:
			item.set_position(best_res)
			item.set_dims(best_res)
			best_bin.add_item(item, with_gap)
	if mlt_cond:
		pool.close()
		pool.join()

	return bins

def harmonic(a, M=10):
	dimension, contains_liquid, mlt_proc, _, _, opti = settings.get_all()
	with_gap = 3 in opti
	m_k = [0 for _ in range(M+1)]
	bins = [[Bin(dimension, list(), contains_liquid)] for k in range(M+1)]
	normalize_bin = Bin(dimension, list(), contains_liquid)
	for i in range(len(a)):
		if 1 in opti: auto_turn(a[i])
		k = floor(normalize_bin.get_total_volume()/a[i].get_volume(dimension)) # Find k & normalize size
		if k > M: k = M
		res = try_place(bins[k][-1], a[i])
		if res[0]:
			a[i].set_position(res)
			a[i].set_dims(res)
			bins[k][-1].add_item(a[i], with_gap)
		else:
			a[i].set_position((None,[0]*dimension))
			bins[k].append(Bin(dimension, list(), contains_liquid))
			bins[k][-1].add_item(a[i], with_gap)
	return bins
