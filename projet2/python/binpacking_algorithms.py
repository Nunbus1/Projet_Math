#!/usr/bin/python3
from bin_item import Item, Bin
from decimal import *


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

#def harmonic_k():
	

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
