#!/usr/bin/python3

import pandas as pd
import time
import sys
import os
from get_path import getPath
from binpacking_algorithms import *
from decimal import *


# Online -> Modified Harmonic 2 best bins | Refined Harmonic best time


if __name__ == "__main__":
	script_dir = os.path.dirname(os.path.abspath(__file__))
	file_dir = "/../data/Données marchandises.xlsx"
	script_dir, file_dir = getPath(script_dir, file_dir)
	getcontext().prec = 6

	data = pd.read_excel(os.path.join(script_dir + file_dir),converters={"Longueur":str,"Largeur":str,"Hauteur":str})
	items = list()
	for index, row in data.iterrows():
		items.append(Item(row[0], row[1], Decimal(row[2]), Decimal(row[3]), Decimal(row[4])))
		#res = next_fit(bins[bin_i], it)
		#if res:
	print("Next fit")
	for i in range(1, 4):
		start = time.time()
		bins = next_fit(items, i)
		print(len(bins))
		print(i, time.time()-start)
#	print("Harmonic-k")
#	for i in range(1, 4):
#		start = time.time()
#		bins = harmonic_k(items, 50, i)
#		cleaned_bins = [b for b in bins if b[0].items != []]
#		print(len(bins), len(cleaned_bins))
#		for k in range(len(cleaned_bins)):
#			print(k+1, len(cleaned_bins[k]))
#			for b in cleaned_bins[k]:
#				print(b.items)
#		print(i, time.time()-start)
#		print()
	"""
	print("Best fit") # Is broken
	for i in range(1, 4):
		start = time.time()
		bins = best_fit(items, i)
		print(len(bins))
		print(i, time.time()-start)"""
	#print(data.head())
	#print(bins)
	#print([x for x in bins if x.is_open == True])
