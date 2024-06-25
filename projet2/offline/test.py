import pandas as pd
import time
import os
from math import prod
from get_path import getPath
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import binpacking
import numpy as np

# Charger les données depuis le fichier Excel
chemin_fichier = '/../data/Données marchandises.xlsx' 

# Pour ajuster le chemin d'accès
script_dir = os.path.dirname(os.path.abspath(__file__))

script_dir, file_dir = getPath(script_dir, chemin_fichier)

data = pd.read_excel(os.path.join(script_dir + chemin_fichier))

items = [

("Tubes acier", 10, 1, 0.5),
("Tubes acier", 9, 2, 0.7),
("Tubes acier", 7.5, 1.2, 0.4),
("Acide chlorhydrique", 1, 1, 1),
("Godet pelleteuse", 2, 2, 1),
("Rails", 11, 1, 0.2),
("Tubes PVC", 3, 2, 0.6),
("Echafaudage", 3, 1.3, 1.8),
("Verre", 3, 2.1, 0.6),
("Ciment", 4, 1, 0.5),
("Bois vrac", 5, 0.8, 1),
("Troncs chênes", 6, 1.9, 1),
("Troncs hêtres", 7, 1.6, 1.5),
("Pompe à chaleur", 5, 1.1, 2.3),
("Cuivre", 6, 2, 1.4),
("Zinc", 5, 0.8, 0.8),
("Papier", 4, 1.6, 0.6),
("Carton", 7, 1, 1.3),
("Verre blanc vrac", 9, 0.9, 2.2),
("Verre brun vrac", 3, 1.6, 0.9),
("Briques rouges", 5, 1.1, 2.4),
("Pièces métalliques", 6, 1.6, 1.4),
("Pièces métalliques", 7, 0.9, 1.2),
("Pièces métalliques", 3, 1.6, 1.9),
("Ardoises", 1, 1.8, 1),
("Tuiles", 2, 1.2, 2.3),
("Vitraux", 4, 0.7, 1.2),
("Carrelage", 6, 1.2, 2.5),
("Tôles", 7, 0.6, 1.5),
("Tôles", 9, 1.7, 1),
("Tôles", 6, 1.9, 1.6),
("Tôles", 3, 2.2, 2.2),
("Tôles", 3, 0.5, 2.2),
("Mobilier urbain", 4, 0.7, 1.9),
("Lin", 5, 2.2, 0.7),
("Textiles à recycler", 6, 1.3, 2.5),
("Aluminium", 6, 1.3, 1.2),
("Batteries automobile", 7, 1.4, 2.5),
("Quincaillerie", 6, 1.1, 1),
("Treuil", 7, 0.9, 1.3),
("Treuil", 8, 0.5, 0.5),
("Acier", 8, 0.9, 1.7),
("Laine de bois", 8, 0.9, 1.8),
("Ouate de cellulose", 5, 1.7, 1.2),
("Chanvre isolation", 2.2, 1.6, 1.1),
("Moteur électrique", 4.2, 1.5, 0.8),
("Semi-conducteurs", 3.7, 0.9, 1.4),
("Semi-conducteurs", 5.6, 0.5, 1.4),
("Semi-conducteurs", 4.9, 0.9, 2.5),
("Semi-conducteurs", 8.7, 1.3, 1.3),
("Semi-conducteurs", 6.1, 2.2, 2.3),
("Semi-conducteurs", 3.3, 1.8, 2.3),
("Semi-conducteurs", 2.6, 1.6, 2.3),
("Semi-conducteurs", 2.9, 1.6, 2),
("Aluminium", 2, 1.1, 0.6),
("Aluminium", 3, 0.6, 1.2),
("Aluminium", 6, 1, 0.8),
("Aluminium", 5, 1.3, 0.6),
("Aluminium", 4, 2.1, 2.1),
("Aluminium", 6, 1.5, 1.9),
("Aluminium", 4, 0.8, 2.1),
("Aluminium", 2, 2, 2.3),
("Aluminium", 4, 1, 1.1),
("Aluminium", 6, 1.8, 1.1),
("Lithium", 6, 1.9, 0.9),
("Lithium", 3, 2, 2.2),
("Lithium", 4, 1.5, 0.9),
("Lithium", 4, 2.1, 2.5),
("Lithium", 2, 1.2, 1.5),
("Lithium", 6, 1.3, 2),
("Lithium", 2, 0.8, 1.1),
("Contreplaqué", 4, 1.4, 2),
("Contreplaqué", 5, 0.6, 0.5),
("Contreplaqué", 5, 0.6, 1.8),
("Contreplaqué", 4, 0.7, 1.4),
("Contreplaqué", 6, 0.5, 0.7),
("Contreplaqué", 3, 1.5, 1.8),
("Contreplaqué", 3, 1.4, 2),
("Contreplaqué", 3, 2, 2.3),
("Contreplaqué", 5, 1.5, 0.7),
("Contreplaqué", 5, 2.2, 0.5),
("Contreplaqué", 6, 1.2, 1.2),
("Poutre", 5, 0.8, 0.7),
("Poutre", 3, 0.5, 1.9),
("Poutre", 5, 1.4, 0.7),
("Poutre", 6, 0.7, 0.7),
("Poutre", 6, 1.2, 2),
("Poutre", 3, 1.7, 1.1),
("Poutre", 5, 1.6, 2.1),
("Pneus", 3, 1.3, 1.7),
("Pneus", 4, 1.5, 1.7),
("Pneus", 3, 1.5, 1.9),
("Pneus", 3, 0.6, 1.9),
("Pneus", 5, 1.8, 0.5),
("Pneus", 3, 1.8, 0.7),
("Pneus", 4, 1.7, 1.4),
("Pneus", 4, 1.5, 0.5),
("Pneus", 2, 2.1, 1.8),
("Pneus", 2, 0.7, 1.1),
("Pneus", 6, 1.2, 1.3)

]
# Définir les dimensions maximales du conteneur (en mètres)
bin_dims = (11.583, 2.294, 2.569)

# Dimensions des wagons
L = 11.583
l = 2.294
h = 2.569

# Volume d'un wagon
wagon_volume = L * l * h

# Liste des volumes des items
item_volumes = [item[1]*item[2]*item[3] for item in items]

# Crée un dictionnaire où chaque item est représenté par une paire clé-valeur
items_dict = {str(i): item_volumes[i] for i in range(len(item_volumes))}

# Utilise l'algorithme de bin packing pour placer les items dans les wagons
bins = binpacking.to_constant_volume(items_dict, wagon_volume)

def plot_wagons_3d(bins, items):
    num_bins = len(bins)
    num_cols = 4
    num_rows = (num_bins + num_cols - 1) // num_cols

    fig = plt.figure(figsize=(num_cols * 5, num_rows * 5))
    
    for bin_index, bin in enumerate(bins):
        ax = fig.add_subplot(num_rows, num_cols, bin_index + 1, projection='3d')
        colors = plt.cm.tab20.colors
        color_idx = 0
        
        for item_str, volume in bin.items():
            item = items[int(item_str)]
            item_dims = (item[1], item[2], item[3])
            position = (0, 0, 0)  # Position to be calculated
            color = colors[color_idx % len(colors)]
            plot_item(ax, position, item_dims, color)
            color_idx += 1
        
        ax.set_xlim(0, bin_dims[0])
        ax.set_ylim(0, bin_dims[1])
        ax.set_zlim(0, bin_dims[2])
        
        ax.set_xlabel('Longueur')
        ax.set_ylabel('Largeur')
        ax.set_zlabel('Hauteur')
        ax.set_title(f'Wagon {bin_index + 1}')
    
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

# Crée un dictionnaire où chaque item est représenté par une paire clé-valeur
items_dict = {str(i): item_volumes[i] for i in range(len(item_volumes))}

# Utilise l'algorithme de bin packing pour placer les items dans les wagons
bins = binpacking.to_constant_volume(items_dict, wagon_volume)

# Volume total des wagons
total_wagon = 13 * (L * l * h)
print(f"Volume total des wagons en m3: {np.round(total_wagon, 2)}")

# Faire la somme des volumes des items
total = sum(item_volumes)
print(f"Total volume en m3 des marchandises: {np.round(total, 2)}")

# Calcul volume total perte
perte = 13 * (L * l * h) - total
print(f"Volume total perte en m3: {np.round(perte, 2)}")

# Afficher le nombre total de conteneurs (wagons) et le nombre total d'objets
print(f"Nombre total de wagons utilisés : {len(bins)}")

# Visualiser chaque conteneur sur une feuille avec plusieurs sous-graphiques
plot_wagons_3d(bins, items)

end_time = time.time()
print(f"Temps de calcul : {end_time - start_time:.2f} secondes")
