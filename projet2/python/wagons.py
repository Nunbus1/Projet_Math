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

	data = pd.read_excel(os.path.join(script_dir + file_dir))
	items = list()
	for index, row in data.iterrows():
		items.append(Item(row[0], row[1], row[2], row[3], row[4]))
		#res = next_fit(bins[bin_i], it)
		#if res:
	for i in range(1, 4):
		start = time.time()
		bins = next_fit(items, i)
		print(len(bins))
		#for b in bins:
		#	print(b.get_items())
		print(i, time.time()-start)
	#print(data.head())
	#print(bins)
	#print([x for x in bins if x.is_open == True])
