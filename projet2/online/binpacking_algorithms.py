#!/usr/bin/python3
from bin_item import Item, Bin
from decimal import *
from math import floor


def next_fit(elements, dimension=1):
	bins = list()
	bin_i = 0
	bins.append(Bin(dimension))
	for element in elements:
		if bins[bin_i].can_fit(element):
			bins[bin_i].add_item(element)
		else:
			bins.append(Bin(dimension, [element]))
			bin_i += 1
	return bins

def best_fit(items, dimension=1):
	bins = list()
	bins.append(Bin(dimension))
	for item in items:
		best_bin = None
		for bin_ in bins:
			if bin_.get_remaining() > 0 and (best_bin is None or bin_.get_used_volume() < best_bin.get_used_volume()):
				best_bin = bin_
		if best_bin is None:
			new_bin = Bin(dimension)
			#new_bin.size += item
			new_bin.add_item(item)
			bins.append(new_bin)
		else:
			#best_bin.size += item
			best_bin.add_item(item)

	return bins

#def harmonic_k(items, k, dimension=1):
#	#bins = [[] for _ in range(k)]
#	bins = list()
#	bins.append(Bin(dimension))
#	for item in items:
#		if item < 1 / (k - 1):  # I_1-item
#			j = 1
#		elif item < 1 / (k - 2):  # I_2-items
#			j = 2
#		elif item < 1 / (k - 3):  # I_3-items
#			j = 3
#		else:  # I_k-item
#			j = k
#
#		for bin.items in bins[j-1]:
#			if bin + item <= 1:
#				break
#		else:
#			bins[j-1].append(item)
#	return [len(bin) for bin in bins]

def harmonic_k(a, M=10, dimension=1):
	m_k = [0 for _ in range(M+1)]
	bins = [[Bin(dimension)] for k in range(M+1)]
	normalize_bin = Bin(dimension)
	for i in range(len(a)):
		k = floor(normalize_bin.get_total_volume()/a[i].get_volume(dimension)) # Find k & normalize size
		if 1<=k and k<M:
			if bins[k][-1].can_fit(a[i]):
				bins[k].add_item(a[i])
			else:
				bins[k].append(Bin(dimension))
				bins[k][-1].add_item(a[i])
		else:
			if bins[M][-1].can_fit(a[i]):
				bins[M][-1].add_item(a[i])
			else:
				bins[M].append(Bin(dimension))
				bins[M][-1].add_item(a[i])
	return bins

def refined_harmonic(elements, dimension=1): # https://en.wikipedia.org/wiki/Harmonic_bin_packing#Refined-Harmonic_(RH)
	# i/(j+1), 1/j
	bins = list()
	bin_i = 0
	bins.append(Bin(dimension))
	N_a = N_b = N_ab = N_bb = N_bp = N_c = 0

def get_size_class(item_size):
	item_size = Decimal(item_size)
	if item_size <= Decimal("1/3"):
		return "S"
	elif item_size <= Decimal("1/2"):
		return "M"
	elif item_size <= Decimal("2/3"):
		return "L"
	else:
		return "XL"

#def pack_item(ai, rl):
#	size_class = get_size_class(ai)
#	if sys.version_info[:3] >= (3, 10): # https://stackoverflow.com/a/1093331
#		match size_class:
#			case "XL":
#				# new XL-bin
#			case "M":
#				# in M-bin with Next Fit
#			case "L":
#			case "S":
#			case _:
#				print("ERROR")
#	else:
#		if size_class == "XL":
#		elif size_class == "M":
#		elif size_class == "L"
