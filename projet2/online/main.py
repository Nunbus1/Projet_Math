#!/usr/bin/python3
import multiprocessing as mp
import pandas as pd
import settings
import argparse
import time
import sys
import os
from get_path import getPath
from binpacking_algorithms import *
from decimal import *


parser = argparse.ArgumentParser(description="Different algos to solve the binpacking problem.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-l", "--liquid", help="If the items act as liquids (their shape is irrelevant)", action="store_true")
parser.add_argument("-m", "--multi_processing", help="If the program uses multi-processing or not", action="store_true")
#parser.add_argument("line_type", help="online, offline, all", type=str)
#parser.add_argument("model", help="Model to use for the prediction", type=str)
args = parser.parse_args()


if __name__ == "__main__":
	script_dir = os.path.dirname(os.path.abspath(__file__))
	file_dir = "/../data/Données marchandises.xlsx"
	script_dir, file_dir = getPath(script_dir, file_dir)
	getcontext().prec = 6
	settings.init()

	data = pd.read_excel(os.path.join(script_dir + file_dir),converters={"Longueur":str,"Largeur":str,"Hauteur":str})
	items = list()
	for index, row in data.iterrows():
		items.append(Item(row[0], row[1], Decimal(row[2]), Decimal(row[3]), Decimal(row[4])))
	settings.contains_liquid = args.liquid
	settings.mlt_thread = args.multi_processing
	print("Next fit")
	for i in range(1, 4):
		start = time.time()
		settings.dimension = i
		bins = next_fit(items)
		print(len(bins))
		print(i, time.time()-start)
	print("\nBest fit")
	for i in range(1, 4):
		start = time.time()
		settings.dimension = i
		bins = best_fit(items)
		print(len(bins))
		print(i, time.time()-start)
	print("\nHarmonic-k")
	for i in range(1, 4):
		start = time.time()
		settings.dimension = i
		ttl_vol = Bin(i, list(), settings.contains_liquid).get_total_volume()
		bins = harmonic_k(items, int(len(items)/(2*i)))
		cleaned_bins = [b for b in bins if b[0].items != []]
		print(
			sum([len(b) for b in bins]),
			sum([len(b) for b in cleaned_bins])
		)
		print(i, time.time()-start)
	# TODO: test w/collisions & test if item position is by reference
	print("\n Offline")
	for i in range(1, 4):
		start = time.time()
		settings.dimension = i
		ret_data, bins = first_fit_decreasing(data)
		print(ret_data[3])
		print(i, time.time()-start)
