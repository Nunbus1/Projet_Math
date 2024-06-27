import pandas as pd
import time
import os
from get_path import getPath
from math import prod
import matplotlib.pyplot as plt

# Charger les données depuis le fichier Excel
chemin_fichier = '/../data/Données marchandises.xlsx' 

# Pour ajuster le chemin d'accès
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir, file_dir = getPath(script_dir, chemin_fichier)
data = pd.read_excel(os.path.join(script_dir + chemin_fichier))

# Définir les dimensions maximales du conteneur (en mètres)
bin_dims = (11.583,)

def can_place_in_bin(item_dims, bin, bin_dims, pos):
    for placed_item in bin:
        if check_overlap(item_dims, placed_item['dimensions'], pos, placed_item['position']):
            return False
    return pos[0] + item_dims[0] <= bin_dims[0]

def check_overlap(dim1, dim2, pos1, pos2):
    x1 = pos1[0]
    x2 = pos2[0]
    lx1 = dim1[0]
    lx2 = dim2[0]
    return not (x1 + lx1 <= x2 or x2 + lx2 <= x1)

def first_fit_decreasing_1d(data, bin_dims):
    bins = []
    for _, item in data.iterrows():
        item_dims = (item['Longueur'],)
        placed = False

        for bin in bins:
            for x in range(int(bin_dims[0] - item_dims[0]) + 1):
                if can_place_in_bin(item_dims, bin, bin_dims, (x,)):
                    bin.append({'dimensions': item_dims, 'position': (x,)})
                    placed = True
                    break
            if placed:
                break
        
        if not placed:
            bins.append([{'dimensions': item_dims, 'position': (0,)}])
    
    total_length = len(bins) * bin_dims[0]
    used_length = sum(item['dimensions'][0] for bin in bins for item in bin)
    unused_length = total_length - used_length
    total_items = sum(len(bin) for bin in bins)
    return bins, len(bins), total_length, used_length, unused_length, total_items

def plot_bins_on_sheet(bins, bin_dims):
    num_bins = len(bins)
    num_cols = 4
    num_rows = (num_bins + num_cols - 1) // num_cols

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(num_cols * 5, num_rows * 5), constrained_layout=True)
    
    colors = plt.cm.tab20.colors
    axs = axs.flatten()
    
    for bin_index, bin in enumerate(bins):
        ax = axs[bin_index]
        for i, item in enumerate(bin):
            color = colors[i % len(colors)]
            plot_item(ax, item['position'], item['dimensions'], color)
        
        ax.set_xlim(0, bin_dims[0])
        ax.set_ylim(0, 1)  # Fixer l'axe y à une unité (dimension 1D)
        ax.set_xlabel('Longueur')
        ax.set_title(f'Wagon {bin_index + 1} - Nombre d\'objets: {len(bin)}')
    
    # Supprimer les sous-graphiques vides
    for j in range(bin_index + 1, len(axs)):
        fig.delaxes(axs[j])
    
    plt.show()

def plot_item(ax, position, dimensions, color):
    x = position[0]
    dx = dimensions[0]
    rect = plt.Rectangle((x, 0), dx, 1, linewidth=1, edgecolor='r', facecolor=color, alpha=0.25)
    ax.add_patch(rect)

start_time = time.time()
bins, num_bins, total_length, used_length, unused_length, total_items = first_fit_decreasing_1d(data, bin_dims)
end_time = time.time()

print(f"Nombre de wagons : {num_bins}")
print(f"Longueur totale : {total_length:.2f} mètres")
print(f"Longueur occupée : {used_length:.2f} mètres")
print(f"Longueur non occupée : {unused_length:.2f} mètres")
print(f"Temps de calcul : {end_time - start_time:.2f} secondes")

print(f"Nombre total de wagons utilisés : {num_bins}")
print(f"Nombre total de conteneurs placés : {total_items}")

plot_bins_on_sheet(bins, bin_dims)
