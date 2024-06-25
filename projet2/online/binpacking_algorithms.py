#!/usr/bin/python3
from bin_item import Item, Bin
from decimal import *
from math import floor


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
