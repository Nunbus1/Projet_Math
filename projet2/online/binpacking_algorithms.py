#!/usr/bin/python3
from bin_item import Item, Bin
from decimal import *
from math import floor
from birdseye import eye


def next_fit(elements, dimension=1):
	bins = list()
	bin_i = 0
	bins.append(Bin(dimension, list()))
	for element in elements:
		if bins[bin_i].can_fit(element):
			bins[bin_i].add_item(element)
		else:
			bins.append(Bin(dimension, [element]))
			bin_i += 1
	return bins

def best_fit(items, dimension=1): # Is broken
	bins_ = list()
	bins_.append(Bin(dimension, list()))
	for item in items:
		best_bin = None
		for b in bins_:
			if b.can_fit(item) and (best_bin is None or b.get_used_volume() < best_bin.get_used_volume()):
				best_bin = b
		if best_bin is None:
			new_bin = Bin(dimension, list())
			new_bin.add_item(item)
			bins_.append(new_bin)
		else:
			best_bin.add_item(item)

	return bins_

def harmonic_k(a, M=10, dimension=1): # Is broken
	m_k = [0 for _ in range(M+1)]
	bins = [[Bin(dimension, list())] for k in range(M+1)]
	normalize_bin = Bin(dimension, list())
	for i in range(len(a)):
		k = floor(normalize_bin.get_total_volume()/a[i].get_volume(dimension)) # Find k & normalize size
		if 1<=k and k<M:
			if bins[k][-1].can_fit(a[i]):
				bins[k][-1].add_item(a[i])
			else:
				bins[k].append(Bin(dimension, list()))
				bins[k][-1].add_item(a[i])
		else:
			if bins[M][-1].can_fit(a[i]):
				bins[M][-1].add_item(a[i])
			else:
				bins[M].append(Bin(dimension, list()))
				bins[M][-1].add_item(a[i])
	return bins

def try_place(current_bin, item, dimension=1):
	if dimension != 1:
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
		return (current_bin.can_fit(item, None, True),)

def first_fit_decreasing(data, dimension=1):
	def do_volume(row):
		return Decimal(row['Longueur']) * Decimal(row['Largeur']) * Decimal(row['Hauteur'])

	data["Volume"] = data.apply(do_volume, axis=1)
	data_sorted = data.sort_values(by="Volume", ascending=False)
	items = list()
	for index, row in data_sorted.iterrows():
		items.append(Item(row[0], row[1], Decimal(row[2]), Decimal(row[3]), Decimal(row[4])))
	bins = list()
	bins.append(Bin(dimension, list(), False))
	for item in items:
		placed = False
		for b in bins:
			res = try_place(b, item, dimension)
			placed = res[0]
			if placed:
				item.set_position(res[1])
				b.add_item(item)
				break
		if not placed:
			bins.append(Bin(dimension, list(), False))
			item.set_position([0, 0, 0])
			bins[-1].add_item(item)
	ret_data = list()
	ret_data.append(("Total V", len(bins) * bins[0].total_volume))
	ret_data.append(("Used V", sum([b.used_volume for b in bins])))
	ret_data.append(("Nombre wagons utilisés", len(bins))) # num_bins
	ret_data.append(("Total items", sum([len(b.items) for b in bins]))) # total_items

	return ret_data, bins
