import pandas as pd
import time
import os
from get_path import getPath
from math import prod
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Charger les données depuis le fichier Excel
chemin_fichier = '/../data/Données marchandises.xlsx' 

# Pour ajuster le chemin d'accès
script_dir = os.path.dirname(os.path.abspath(__file__))

script_dir, file_dir = getPath(script_dir, chemin_fichier)

data = pd.read_excel(os.path.join(script_dir + chemin_fichier))
# Définir les dimensions maximales du conteneur (en mètres)
bin_dims = (11.583, 2.294, 2.569)

def calculate_volume(row):
    return row['Longueur'] * row['Largeur'] * row['Hauteur']

def can_place_in_bin(item_dims, bin, bin_dims, pos):
    for placed_item in bin:
        if check_overlap(item_dims, placed_item['dimensions'], pos, placed_item['position']):
            return False
    return pos[0] + item_dims[0] <= bin_dims[0] and pos[1] + item_dims[1] <= bin_dims[1] and pos[2] + item_dims[2] <= bin_dims[2]

def check_overlap(dim1, dim2, pos1, pos2):
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    lx1, ly1, lz1 = dim1
    lx2, ly2, lz2 = dim2
    return not (x1 + lx1 <= x2 or x2 + lx2 <= x1 or
                y1 + ly1 <= y2 or y2 + ly2 <= y1 or
                z1 + lz1 <= z2 or z2 + lz2 <= z1)

def first_fit_decreasing_3d(data, bin_dims):
    data['Volume'] = data.apply(calculate_volume, axis=1)
    data_sorted = data.sort_values(by='Volume', ascending=False)
    
    bins = []
    for _, item in data_sorted.iterrows():
        item_dims = (item['Longueur'], item['Largeur'], item['Hauteur'])
        placed = False

        for bin in bins:
            for x in range(int(bin_dims[0] - item_dims[0]) + 1):
                for y in range(int(bin_dims[1] - item_dims[1]) + 1):
                    for z in range(int(bin_dims[2] - item_dims[2]) + 1):
                        if can_place_in_bin(item_dims, bin, bin_dims, (x, y, z)):
                            bin.append({'dimensions': item_dims, 'position': (x, y, z)})
                            placed = True
                            break
                    if placed:
                        break
                if placed:
                    break
            if placed:
                break
        
        if not placed:
            bins.append([{'dimensions': item_dims, 'position': (0, 0, 0)}])
    
    total_volume = len(bins) * prod(bin_dims)
    used_volume = sum(prod(item['dimensions']) for bin in bins for item in bin)
    unused_volume = total_volume - used_volume
    total_items = sum(len(bin) for bin in bins)
    return bins, len(bins), total_volume, used_volume, unused_volume, total_items

def plot_bins_on_sheet(bins, bin_dims):
    num_bins = len(bins)
    num_cols = 4
    num_rows = (num_bins + num_cols - 1) // num_cols

    fig = plt.figure(figsize=(num_cols * 5, num_rows * 5))
    
    for bin_index, bin in enumerate(bins):
        ax = fig.add_subplot(num_rows, num_cols, bin_index + 1, projection='3d')
        colors = plt.cm.tab20.colors
        color_idx = 0
        
        for item in bin:
            color = colors[color_idx % len(colors)]
            plot_item(ax, item['position'], item['dimensions'], color)
            color_idx += 1
        
        ax.set_xlim(0, bin_dims[0])
        ax.set_ylim(0, bin_dims[1])
        ax.set_zlim(0, bin_dims[2])
        
        ax.set_xlabel('Longueur')
        ax.set_ylabel('Largeur')
        ax.set_zlabel('Hauteur')
        ax.set_title(f'Wagon {bin_index + 1} - Nombre d\'objets: {len(bin)}')
    
    plt.tight_layout()
    plt.show()

def plot_item(ax, position, dimensions, color):
    x, y, z = position
    dx, dy, dz = dimensions
    vertices = [
        [x, y, z],
        [x + dx, y, z],
        [x + dx, y + dy, z],
        [x, y + dy, z],
        [x, y, z + dz],
        [x + dx, y, z + dz],
        [x + dx, y + dy, z + dz],
        [x, y + dy, z + dz]
    ]
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[4], vertices[7], vertices[3], vertices[0]]
    ]
    poly3d = Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='r', alpha=.25)
    ax.add_collection3d(poly3d)

start_time = time.time()
bins, num_bins, total_volume, used_volume, unused_volume, total_items = first_fit_decreasing_3d(data, bin_dims)
end_time = time.time()

print(f"Nombre de wagons : {num_bins}")
print(f"Volume total : {total_volume:.2f} mètres cubes")
print(f"Volume occupé : {used_volume:.2f} mètres cubes")
print(f"Volume non occupé : {unused_volume:.2f} mètres cubes")
print(f"Temps de calcul : {end_time - start_time:.2f} secondes")
print(f"Nombre total de wagons utilisés : {num_bins}")
print(f"Nombre total de conteneurs placés : {total_items}")

# Afficher le nombre total de conteneurs (wagons) et le nombre total d'objets
for i, bin in enumerate(bins):
    print(f"Wagon {i + 1} - Nombre d'objets : {len(bin)}")

# Visualiser chaque conteneur sur une feuille avec plusieurs sous-graphiques
plot_bins_on_sheet(bins, bin_dims)
