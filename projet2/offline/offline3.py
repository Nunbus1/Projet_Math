import pandas as pd
import time
import os
import numpy as np
from math import prod
from get_path import getPath
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Charger les données depuis le fichier Excel
chemin_fichier = '/../data/Données marchandises.xlsx'

# Pour ajuster le chemin d'accès
#Déterminer le répertoire du script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Ajuster les chemins en fonction du système d'exploitation
script_dir, file_dir = getPath(script_dir, chemin_fichier)
#Lire le fichier Excel
data = pd.read_excel(os.path.join(script_dir + chemin_fichier))

# Définir les dimensions maximales du conteneur (en mètres)
bin_dims = (11.583, 2.294, 2.569)
longueur_maximale, largeur_maximale, hauteur_maximale = bin_dims

# Résolution de la grille
resolution = 10

def calculate_volume(row):
    return row['Longueur'] * row['Largeur'] * row['Hauteur']

def generate_rotations(dimensions):
    l, w, h = dimensions
    return [
        (l, w, h), (l, h, w), 
        (w, l, h), (w, h, l), 
        (h, l, w), (h, w, l)
    ]

def peut_placer_volume(conteneur, longueur, largeur, hauteur, x, y, z):
    if x + longueur > longueur_maximale or y + largeur > largeur_maximale or z + hauteur > hauteur_maximale:
        return False
    return np.all(conteneur[
        int(x*resolution):int((x + longueur)*resolution),
        int(y*resolution):int((y + largeur)*resolution),
        int(z*resolution):int((z + hauteur)*resolution)] == 0)

def placer_dans_volume(conteneur, longueur, largeur, hauteur, x, y, z):
    conteneur[
        int(x*resolution):int((x + longueur)*resolution),
        int(y*resolution):int((y + largeur)*resolution),
        int(z*resolution):int((z + hauteur)*resolution)] = 1

def first_fit_decreasing_3d(data, bin_dims):

    #Calcul du volume de chaque marchandise et tri décroissant par volume
    data['Volume'] = data.apply(calculate_volume, axis=1)
    data_sorted = data.sort_values(by='Volume', ascending=False)
    #Initialisation des conteneurs
    bins = []
    #Parcours de chaque marchandise trié par volume décroissant
    for _, item in data_sorted.iterrows():
        item_dims = (item['Longueur'], item['Largeur'], item['Hauteur'])
        placed = False

        #Parcours des conteneurs existants pour essayer de placer la marchandise
        for bin_index, bin in enumerate(bins):
            #Génère toutes les rotations possibles de la marchandise
            for rotation in generate_rotations(item_dims):
                #Parcours de toutes les positions possibles dans le conteneur pour chaque rotation de la marchandise
                for x in np.arange(0, bin_dims[0] - rotation[0], 1/resolution):
                    for y in np.arange(0, bin_dims[1] - rotation[1], 1/resolution):
                        for z in np.arange(0, bin_dims[2] - rotation[2], 1/resolution):
                            #Vérifie si la marchandise peut être placé à cette position dans le conteneur
                            if peut_placer_volume(bin['matrix'], *rotation, x, y, z):
                                #Place la marchandise dans le conteneur
                                placer_dans_volume(bin['matrix'], *rotation, x, y, z)
                                # Enregistre les informations sur la marchandise placé dans le conteneur
                                bin['items'].append({'dimensions': rotation, 'position': (x, y, z)})
                                placed = True
                                break
                        if placed:
                            break
                    if placed:
                        break
                if placed:
                    break
        #Si la marchandise n'a pas pu être placé dans aucun conteneur existant, crée un nouveau conteneur
        if not placed:
            new_bin_matrix = np.zeros((int(bin_dims[0]*resolution), int(bin_dims[1]*resolution), int(bin_dims[2]*resolution)))
            placer_dans_volume(new_bin_matrix, *item_dims, 0, 0, 0)
            bins.append({'matrix': new_bin_matrix, 'items': [{'dimensions': item_dims, 'position': (0, 0, 0)}]})
    # Calcul des statistiques sur les conteneurs et les marchandises placés
    total_volume = len(bins) * prod(bin_dims) # Calcul des statistiques sur les conteneurs et les marchandises placés
    used_volume = sum(prod(item['dimensions']) for bin in bins for item in bin['items'])
    unused_volume = total_volume - used_volume # Volume non utilisé dans tous les conteneurs
    total_items = sum(len(bin['items']) for bin in bins)# Nombre total marchandise placés

     # Retourne les conteneurs avec les marchandises placés, ainsi que les statistiques sur les volumes
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
        
        for item in bin['items']:
            color = colors[color_idx % len(colors)]
            plot_item(ax, item['position'], item['dimensions'], color)
            color_idx += 1
        
        ax.set_xlim(0, bin_dims[0])
        ax.set_ylim(0, bin_dims[1])
        ax.set_zlim(0, bin_dims[2])
        
        ax.set_xlabel('Longueur')
        ax.set_ylabel('Largeur')
        ax.set_zlabel('Hauteur')
        ax.set_title(f'Wagon {bin_index + 1} - Nombre d\'objets: {len(bin["items"])}')
    
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

# Utiliser FFD pour une solution initiale
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
    print(f"Wagon {i + 1} - Nombre d'objets : {len(bin['items'])}")

# Visualiser chaque conteneur sur une feuille avec plusieurs sous-graphiques
plot_bins_on_sheet(bins, bin_dims)
