#!/usr/bin/python3
import multiprocessing as mp
import pandas as pd
import affichage
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
parser.add_argument("-p", "--precision", help="The precision to use to test for collision. Is ignored if `--liquid` is set. Default: 1", type=Decimal, default=Decimal("1"))
parser.add_argument("-d", "--dimension", help="Set the dimension you want to see, -1 for all (1, 2, 3, [-1])", type=int, default=-1)
parser.add_argument("-s", "--show", help="Show a 3D graph of the bins (only works for 3D)", action="store_true")
parser.add_argument("--model", help="Model to use for the prediction. Default: all", type=str, choices=["next_fit", "best_fit", "harmonic", "first_fit_d", "all"], default="all")
args = parser.parse_args()


if __name__ == "__main__":
	script_dir = os.path.dirname(os.path.abspath(__file__))
	file_dir = "/../data/Données marchandises.xlsx"
	script_dir, file_dir = getPath(script_dir, file_dir)
	c = getcontext()
	c.prec = 6
	c.traps[FloatOperation] = False
	settings.init()

	data = pd.read_excel(os.path.join(script_dir + file_dir),converters={"Longueur":str,"Largeur":str,"Hauteur":str})
	items = list()
	for index, row in data.iterrows():
		items.append(Item(row[0], row[1], Decimal(row[2]), Decimal(row[3]), Decimal(row[4])))
	settings.contains_liquid = args.liquid
	settings.mlt_proc = args.multi_processing
	settings.precision = args.precision
	if args.model == "next_fit" or args.model == "all":
		print("Next fit")
		for i in range(1, 4):
			if args.dimension == -1 or args.dimension == i:
				start = time.time()
				settings.dimension = i
				bins = next_fit(items)
				print(len(bins))
				print(i, time.time()-start)
		if args.show:
			affichage.plot_bins_on_sheet(bins)
	if args.model == "best_fit" or args.model == "all":
		print("Best fit")
		for i in range(1, 4):
			if args.dimension == -1 or args.dimension == i:
				start = time.time()
				settings.dimension = i
				bins = best_fit(items)
				print(len(bins))
				print(i, time.time()-start)
		if args.show:
			affichage.plot_bins_on_sheet(bins)
	if args.model == "harmonic" or args.model == "all":
		print("Harmonic-k")
		for i in range(1, 4):
			if args.dimension == -1 or args.dimension == i:
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
		if args.show:
			affichage.plot_bins_on_sheet(bins)
	if args.model == "first_fit_d" or args.model == "all":
		print("First fit decreasing")
		for i in range(1, 4):
			if args.dimension == -1 or args.dimension == i:
				start = time.time()
				settings.dimension = i
				ret_data, bins = first_fit_decreasing(data)
				print(ret_data[3])
				print(i, time.time()-start)
		if args.show:
			affichage.plot_bins_on_sheet(bins)
