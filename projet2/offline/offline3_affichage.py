import pandas as pd
import time
from math import prod
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from get_path import getPath

# Charger le fichier Excel
chemin_fichier = '/../data/Données marchandises.xlsx' 

#Pour ajuster le chemin d'accès
script_dir = os.path.dirname(os.path.abspath(__file__))

script_dir, file_dir = getPath(script_dir, chemin_fichier)

data = pd.read_excel(os.path.join(script_dir + chemin_fichier))
# Définir les dimensions maximales du conteneur (en mètres)
bin_dims = (11.583, 2.294, 2.569)

def calculate_volume(row):
    return row['Longueur'] * row['Largeur'] * row['Hauteur']

def can_place_in_bin(item, bin, bin_dims):
    bin_volume = sum(prod(existing_item) for existing_item in bin)
    return bin_volume + prod(item) <= prod(bin_dims)

def first_fit_decreasing_3d(data, bin_dims):
    # Convertir les dimensions en mètres et calculer le volume
    data['Volume'] = data.apply(calculate_volume, axis=1)
    data_sorted = data.sort_values(by='Volume', ascending=False)
    
    bins = []
    bin_coords = []  # Coordonnées des objets dans les conteneurs
    for _, item in data_sorted.iterrows():
        item_dims = (item['Longueur'], item['Largeur'], item['Hauteur'])
        placed = False

        for i, bin in enumerate(bins):
            if can_place_in_bin(item_dims, bin, bin_dims):
                bin.append(item_dims)
                bin_coords[i].append((0, 0, 0))  # Ajouter les coordonnées appropriées
                placed = True
                break
        
        if not placed:
            bins.append([item_dims])
            bin_coords.append([(0, 0, 0)])  # Initialiser avec l'origine pour le premier objet
    
    total_volume = len(bins) * prod(bin_dims)
    used_volume = sum(prod(item) for bin in bins for item in bin)
    unused_volume = total_volume - used_volume
    return len(bins), total_volume, used_volume, unused_volume, bins, bin_coords

def plot_bins(bins, bin_coords, bin_dims):
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'orange', 'purple', 'brown', 'pink']
    
    for b_idx, bin in enumerate(bins):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        color = colors[b_idx % len(colors)]
        
        for item_idx, item in enumerate(bin):
            x, y, z = bin_coords[b_idx][item_idx]
            dx, dy, dz = item
            ax.bar3d(x, y, z, dx, dy, dz, color=color, alpha=0.6)
        
        ax.set_title(f"Wagon {b_idx + 1}")
        ax.set_xlabel('Longueur')
        ax.set_ylabel('Largeur')
        ax.set_zlabel('Hauteur')
        plt.show()

start_time = time.time()
num_bins, total_volume, used_volume, unused_volume, bins, bin_coords = first_fit_decreasing_3d(data, bin_dims)
end_time = time.time()

print(f"Nombre de conteneurs : {num_bins}")
print(f"Volume total : {total_volume:.2f} mètres cubes")
print(f"Volume occupé : {used_volume:.2f} mètres cubes")
print(f"Volume non occupé : {unused_volume:.2f} mètres cubes")
print(f"Temps de calcul : {end_time - start_time:.2f} secondes")

plot_bins(bins, bin_coords, bin_dims)
