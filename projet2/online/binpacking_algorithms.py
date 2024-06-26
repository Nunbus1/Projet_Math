#!/usr/bin/python3
from bin_item import Item, Bin
from decimal import *
from math import floor
from birdseye import eye


def next_fit(items, dimension=1, contains_liquid=True):
	bins = list()
	bin_i = 0
	bins.append(Bin(dimension, list(), contains_liquid))
	for item in items:
		res = try_place(bins[bin_i], item, dimension, contains_liquid)
		if res[0]:
			if (not contains_liquid) and dimension > 1: item.set_position(res[1])
			bins[bin_i].add_item(item)
		else:
			if (not contains_liquid) and dimension > 1: item.set_position([0]*dimension)
			bins.append(Bin(dimension, [item], contains_liquid))
			bin_i += 1
	return bins

def best_fit(items, dimension=1, contains_liquid=True): # Is broken
	bins_ = list()
	bins_.append(Bin(dimension, list(), contains_liquid))
	for item in items:
		best_bin = None
		best_pos = None
		for b in bins_:
			res = try_place(b, item, dimension, contains_liquid)
			if res[0] and (best_bin is None or b.get_used_volume() < best_bin.get_used_volume()):
				best_bin = b
				if (not contains_liquid) and dimension > 1: best_pos = res[1]
		if best_bin is None:
			if (not contains_liquid) and dimension > 1: item.set_position([0]*dimension)
			new_bin = Bin(dimension, [item], contains_liquid)
			bins_.append(new_bin)
		else:
			if (not contains_liquid) and dimension > 1: item.set_position(best_pos)
			best_bin.add_item(item)

	return bins_

def harmonic_k(a, M=10, dimension=1, contains_liquid=True): # Is broken
	m_k = [0 for _ in range(M+1)]
	bins = [[Bin(dimension, list(), contains_liquid)] for k in range(M+1)]
	normalize_bin = Bin(dimension, list(), contains_liquid)
	for i in range(len(a)):
		k = floor(normalize_bin.get_total_volume()/a[i].get_volume(dimension)) # Find k & normalize size
		if 1<=k and k<M:
			res = try_place(bins[k][-1], a[i], dimension, contains_liquid)
			if res[0]:
				if (not contains_liquid) and dimension > 1: a[i].set_position(res[1])
				bins[k][-1].add_item(a[i])
			else:
				if (not contains_liquid) and dimension > 1: a[i].set_position([0]*dimension)
				bins[k].append(Bin(dimension, [a[i]], contains_liquid))
		else:
			res = try_place(bins[M][-1], a[i], dimension, contains_liquid)
			if res[0]:
				if (not contains_liquid) and dimension > 1: a[i].set_position(res[1])
				bins[M][-1].add_item(a[i])
			else:
				if (not contains_liquid) and dimension > 1: a[i].set_position([0]*dimension)
				bins[M].append(Bin(dimension, [a[i]], contains_liquid))
	return bins

def try_place(current_bin, item, dimension=1, contains_liquid=True):
	if dimension != 1 and not contains_liquid:
		def travel_axis(current_binn, itemm, dim, pos):
			if dim == 0:
				if current_binn.can_fit(itemm, pos):
					return (True, pos)
				else:
					return (False,)
			n_pos = pos.copy()
			n_pos.append(0)
			for i in range(int(current_binn.dims[dimension-dim]-itemm.dims[dimension-dim]) +1):
				n_pos[-1] = i
				res = travel_axis(current_binn, itemm, dim-1, n_pos)
				if res[0]:
					return res
			return (False,)
		return travel_axis(current_bin, item, dimension, [])
	else:
		return current_bin.can_fit(item, None, True)

def first_fit_decreasing(data, dimension=1, contains_liquid=True):
	def do_volume(row):
		return Decimal(row['Longueur']) * Decimal(row['Largeur']) * Decimal(row['Hauteur'])

	data["Volume"] = data.apply(do_volume, axis=1)
	data_sorted = data.sort_values(by="Volume", ascending=False)
	items = list()
	for index, row in data_sorted.iterrows():
		items.append(Item(row[0], row[1], Decimal(row[2]), Decimal(row[3]), Decimal(row[4])))
	bins = list()
	bins.append(Bin(dimension, list(), contains_liquid))
	for item in items:
		placed = False
		for b in bins:
			res = try_place(b, item, dimension, contains_liquid)
			placed = res[0]
			if placed:
				if (not contains_liquid) and dimension > 1: item.set_position(res[1])
				b.add_item(item)
				break
		if not placed:
			if (not contains_liquid) and dimension > 1: item.set_position([0]*dimension)
			bins.append(Bin(dimension, [item], contains_liquid))
	ret_data = list()
	ret_data.append(("Total V", len(bins) * bins[0].total_volume))
	ret_data.append(("Used V", sum([b.used_volume for b in bins])))
	ret_data.append(("Nombre wagons utilisés", len(bins))) # num_bins
	ret_data.append(("Total items", sum([len(b.items) for b in bins]))) # total_items

	return ret_data, bins
