#!/usr/bin/python3
import multiprocessing as mp
import pandas as pd
import affichage
import settings
import argparse
import sys
import os
from get_path import getPath
from binpacking_algorithms import *
from time import time
from decimal import *
from re import sub


online_algos = ['next_fit', 'first_fit', 'best_fit', 'harmonic']
#offline_algos = ['next_fit_d', 'first_fit_d', 'best_fit_d', 'harmonic_d']
offline_algos = [algo+'_d' for algo in online_algos]
model_names = online_algos + offline_algos
parser = argparse.ArgumentParser(description='Different algos to solve the binpacking problem.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-l', '--liquid', help='If the items act as liquids (their shape is irrelevant)', action='store_true')
parser.add_argument('-m', '--multi_processing', help='If the program uses multi-processing or not', action='store_true')
parser.add_argument('-p', '--precision', help='The precision to use to test for collision. Is ignored if `--liquid` is set. Smaller is more precise.', type=Decimal, default=Decimal('1'))
parser.add_argument('-d', '--dimension', help='Set the dimension you want to see, -1 for all', type=int, choices=[-1, 1, 2, 3], default=-1)
parser.add_argument('-s', '--show', help='Show a 3D graph of the bins and their contents (only works for 3D)', action='store_true')
parser.add_argument('-M', '--model', help="Model to use for the prediction. If `best` is chosen, the program will automatically select the theoretical best algorithm given: whether it's online or offline, and whether `liquid` is set or not", type=str, choices=model_names+['all', 'best'], default='best')
args = parser.parse_args()


if __name__ == '__main__':
	script_dir = os.path.dirname(os.path.abspath(__file__))
	file_dir = '/../data/Données marchandises.xlsx'
	script_dir, file_dir = getPath(script_dir, file_dir)
	c = getcontext()
	c.prec = 6
	c.traps[FloatOperation] = False
	settings.init()

	data = pd.read_excel(os.path.join(script_dir + file_dir),converters={'Longueur':str,'Largeur':str,'Hauteur':str})
	items = list()
	for index, row in data.iterrows():
		items.append(Item(row[0], row[1], Decimal(row[2]), Decimal(row[3]), Decimal(row[4])))
	settings.contains_liquid = args.liquid
	settings.mlt_proc = args.multi_processing
	settings.precision = args.precision
	models_available = dict()
	for model in model_names:
		ml_name = model.replace('_', ' ').capitalize()
		ml_name = ml_name.replace('Harmonic', 'Harmonic-k')
		ml_name = sub(r' d$', ' decreasing', ml_name)
		models_available[model] = dict()
		models_available[model]['name'] = ml_name
#		if model == 'first_fit_d':
#			models_available[model]['fun'] = first_fit_decreasing
#		else:
		models_available[model]['fun'] = globals()[model.replace('_d', '')]
		models_available[model]['is_offline'] = model in offline_algos
		models_available[model]['is_harmonic'] = 'harmonic' in model
	models_to_use = list()
	if args.model == 'all':
		models_to_use = model_names
	elif args.model == 'best':
		models_to_use.append('best_fit')
		models_to_use.append('first_fit_d')
	else:
		models_to_use.append(args.model)
	use_offline = False
	for m in models_to_use:
		if m in offline_algos:
			use_offline = True
			break
	if use_offline:
		def do_volume(row):
			return Decimal(row['Longueur']) * Decimal(row['Largeur']) * Decimal(row['Hauteur'])
		data['Volume'] = data.apply(do_volume, axis=1)
		data_sorted = data.sort_values(by='Volume', ascending=False)
		items_offline = list()
		for index, row in data_sorted.iterrows():
			items_offline.append(Item(row[0], row[1], Decimal(row[2]), Decimal(row[3]), Decimal(row[4])))
	did_switch = [False, False]
	for model in models_to_use:
		if not did_switch[models_available[model]['is_offline']]:
			print('\033[94m'+('OFFLINE' if models_available[model]['is_offline'] else 'ONLINE')+'\033[m')
			did_switch[models_available[model]['is_offline']] = True
		print('\033[1;4m'+models_available[model]['name']+'\033[m')
		to_use = items_offline.copy() if models_available[model]['is_offline'] else items.copy()
		for i in range(1, 4):
			if args.dimension in (-1, i):
				start = time()
				settings.dimension = i
				settings.is_offline = models_available[model]['is_offline']
				print(f'Dimension {i}')
				if models_available[model]['is_harmonic']:
					ttl_vol = Bin(i, list(), settings.contains_liquid).get_total_volume()
					bins = models_available[model]['fun'](to_use, int(len(items)/(2*i)))
					cleaned_bins = [b for bs in bins if bs[0].items != [] for b in bs]
					bins = cleaned_bins
					#print(f'\033[2m{sum([len(b) for b in cleaned_bins])}\033[m wagons utilisés')
				else:
					bins = models_available[model]['fun'](to_use)
				print(f'\033[3m{len(bins)}\033[m wagons utilisés')
				#print(f'Remaining volume: {sum([b.get_remaining() for b in bins])}')
				print(f'Fait en {time()-start}s')
				if any([True for b in bins if b.get_remaining()<0]):
					print('Breaks physics')
				print()
			if args.show and i == 3 and not args.liquid:
				affichage.plot_bins_on_sheet(bins)
		print()
