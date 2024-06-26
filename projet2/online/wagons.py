#!/usr/bin/python3
import pandas as pd
import time
import sys
import os
from get_path import getPath
from binpacking_algorithms import *
from decimal import *


if __name__ == "__main__":
	script_dir = os.path.dirname(os.path.abspath(__file__))
	file_dir = "/../data/Données marchandises.xlsx"
	script_dir, file_dir = getPath(script_dir, file_dir)
	getcontext().prec = 6

	data = pd.read_excel(os.path.join(script_dir + file_dir),converters={"Longueur":str,"Largeur":str,"Hauteur":str})
	items = list()
	for index, row in data.iterrows():
		items.append(Item(row[0], row[1], Decimal(row[2]), Decimal(row[3]), Decimal(row[4])))
	print("Next fit")
	for i in range(1, 4):
		start = time.time()
		bins = next_fit(items, i, False)
		print(len(bins))
		print(i, time.time()-start)
	print("\nBest fit")
	for i in range(1, 4):
		start = time.time()
		bins = best_fit(items, i, False)
		print(len(bins))
		print(i, time.time()-start)
	print("\nHarmonic-k")
	for i in range(1, 4):
		start = time.time()
		ttl_vol = Bin(i, list(), False).get_total_volume()
		print("TTL_vol", ttl_vol)
		bins = harmonic_k(items, int(len(items)/(2*i)), i)
		cleaned_bins = [b for b in bins if b[0].items != []]
		print(
			sum([len(b) for b in bins]),
			sum([len(b) for b in cleaned_bins])
		)
		print(i, time.time()-start)
	# TODO: test w/collisions & test if item position is by reference
	ret_data, bins = first_fit_decreasing(data, 3, False)
	for r in ret_data:
		print(r)
