from classes.Item import Item
from classes.Bin import Bin
from math import floor
from birdseye import eye
from decimal import *
from functools import reduce
import multiprocessing as mp
import settings


# UTILS
def drange(x, y, jump): # From: https://stackoverflow.com/a/7267280
	while x < y:
		yield x
		x += jump

def auto_turn(item): # OPT 1
	return
	dimension, contains_liquid, _, _, _ = settings.get_all()
	if dimension == 1 or contains_liquid:
		return
	esb, egi = list(), list() # Espace, Smallest/Greatest, Bin/Item
	eb = Bin.dims[:dimension].copy()
	ei = item.dims[:dimension].copy()
	for d in range(dimension-1):
		sb = min(eb[:dimension])
		gi = max(ei[:dimension])
		esb.append(sb)
		egi.append(gi)
		eb.remove(sb)
		ei.remove(gi)
	if reduce(lambda x, y: x*y, egi) > reduce(lambda x, y: x*y, esb):
		return
	eb = Bin.dims[:dimension].copy()
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
		return
	missing = list()
	missing.append([m for m in range(3) if m not in g_indexes][0])
	missing.append([m for m in range(3) if m not in s_indexes][0])
	a = item.dims[missing[1]]
	for d in range(len(s_indexes)):
		item.dims[g_indexes[d]] = item.dims[s_indexes[d]]
	item.dims[missing[0]] = a

def try_place(current_bin, item):
	dimension, contains_liquid, mlt_proc, resolution, is_offline = settings.get_all()
	if dimension != 1 and not contains_liquid:
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
#			if dimension-dim+1 == 1: # OPT 2
#				items_test = current_bin.items.copy()
#				while items_test != []:
#					fits, it = current_binn.do_test_gap(items_test, itemm.dims)
#					if not fits:
#						i_start += it.position[0]
#						try:
#							items_test.remove(it)
#						except ValueError:
#							pass
#					else:
#						break
			#for i in range(i_start, int((int(current_binn.dims[dimension-dim]-itemm.dims[dimension-dim])+1)/resolution)):
			for i in drange(i_start, current_binn.dims[dimension-dim]-itemm.dims[dimension-dim]+1, resolution):
				n_pos[-1] = i
				res = travel_axis(current_binn, itemm, dim-1, n_pos)
				if res[0]:
					return res
			return (False,)
		return travel_axis(current_bin, item, dimension, [])
	else:
		return current_bin.can_fit(item, None, True)


# ONLINE
def next_fit(items):
	dimension, contains_liquid, mlt_proc, _, _ = settings.get_all()
	bins = list()
	bin_i = 0
	bins.append(Bin(dimension, list(), contains_liquid))
	for item in items:
		auto_turn(item)
		res = try_place(bins[bin_i], item)
		if res[0]:
			item.set_position(res)
			bins[bin_i].add_item(item)
		else:
			item.set_position((None,[0]*dimension))
			bins.append(Bin(dimension, [item], contains_liquid))
			bin_i += 1
	return bins

def first_fit(items):
	dimension, contains_liquid, mlt_proc, _, _ = settings.get_all()
	def use_result(bins, i, item, result):
		placed = result[0]
		if placed:
			item.set_position(result)
			bins[i].add_item(item)
		return placed

	bins = list()
	bins.append(Bin(dimension, list(), contains_liquid))
	mlt_cond = mlt_proc and dimension != 1
	if mlt_cond:
		batch_size = 4*mp.cpu_count()
		pool = mp.Pool()
	for item in items:
		auto_turn(item)
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
			bins.append(Bin(dimension, [item], contains_liquid))
	if mlt_cond:
		pool.close()
		pool.join()

	return bins

def best_fit(items):
	dimension, contains_liquid, mlt_proc, _, _ = settings.get_all()
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
		auto_turn(item)
		best_bin = None
		best_pos = None
		if mlt_cond:
			i=0
			for result in pool.starmap(try_place, [(b, item) for b in bins], chunksize=4):
				best = use_result(bins, i, best_bin, result)
				if best[0] != False:
					best_bin, best_pos = best
				i += 1
		else:
			for i in range(len(bins)):
				result = try_place(bins[i], item)
				best = use_result(bins, i, best_bin, result)
				if best[0] != False:
					best_bin, best_pos = best
		if best_bin is None:
			item.set_position((None,[0]*dimension))
			new_bin = Bin(dimension, [item], contains_liquid)
			bins.append(new_bin)
		else:
			item.set_position(best_pos)
			best_bin.add_item(item)
	if mlt_cond:
		pool.close()
		pool.join()

	return bins

def harmonic(a, M=10):
	dimension, contains_liquid, mlt_proc, _, _ = settings.get_all()
	m_k = [0 for _ in range(M+1)]
	bins = [[Bin(dimension, list(), contains_liquid)] for k in range(M+1)]
	normalize_bin = Bin(dimension, list(), contains_liquid)
	for i in range(len(a)):
		auto_turn(a[i])
		k = floor(normalize_bin.get_total_volume()/a[i].get_volume(dimension)) # Find k & normalize size
		if k > M: k = M
		res = try_place(bins[k][-1], a[i])
		if res[0]:
			a[i].set_position(res)
			bins[k][-1].add_item(a[i])
		else:
			a[i].set_position((None,[0]*dimension))
			bins[k].append(Bin(dimension, [a[i]], contains_liquid))
	return bins
