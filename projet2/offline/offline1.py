import pandas as pd
import time
import os
from get_path import getPath
from math import prod
import matplotlib.pyplot as plt

# Charger les données depuis le fichier Excel
chemin_fichier = '/../data/Données marchandises.xlsx' 
#Pour ajuster le chemin d'accès
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir, file_dir = getPath(script_dir, chemin_fichier)
data = pd.read_excel(os.path.join(script_dir + chemin_fichier))

# Définir les dimensions maximales du conteneur (en mètres)
bin_dims = (11.583,)

# Fonction pour vérifier si un article peut être placé dans un conteneur à une position donnée sans chevauchement
def can_place_in_bin(item_dims, bin, bin_dims, pos):
    # Parcourt chaque article déjà placé dans le conteneur
    for placed_item in bin:
        # Vérifie s'il y a un chevauchement entre l'article actuel et l'article déjà placé
        if check_overlap(item_dims, placed_item['dimensions'], pos, placed_item['position']):
            # Si chevauchement détecté, retourne False
            return False
    # Vérifie si l'article dépasse les limites du conteneur en x    
    return pos[0] + item_dims[0] <= bin_dims[0]

def check_overlap(dim1, dim2, pos1, pos2):
    #Initialisation des variables
    x1 = pos1[0]
    x2 = pos2[0]
    lx1 = dim1[0]
    lx2 = dim2[0]
    #Vérification du chevauchement
    return not (x1 + lx1 <= x2 or x2 + lx2 <= x1)

def first_fit_decreasing_1d(data, bin_dims):
    #initialisation
    bins = []
    # Placement des articles
    for _, item in data.iterrows():
        item_dims = (item['Longueur'],)
        placed = False
        #Essai de placement dans les conteneurs existants
        for bin in bins:
            for x in range(int(bin_dims[0] - item_dims[0]) + 1):
                if can_place_in_bin(item_dims, bin, bin_dims, (x,)):
                    bin.append({'dimensions': item_dims, 'position': (x,)})
                    placed = True
                    break
            if placed:
                break
        #Création d'un nouveau conteneur
        if not placed:
            bins.append([{'dimensions': item_dims, 'position': (0,)}])
    #Calcul des métriques 
    total_length = len(bins) * bin_dims[0]
    used_length = sum(item['dimensions'][0] for bin in bins for item in bin)
    unused_length = total_length - used_length
    total_items = sum(len(bin) for bin in bins)
    #Retour des résultats
    return bins, len(bins), total_length, used_length, unused_length, total_items

def plot_bin(bin, bin_dims, bin_index):
    fig, ax = plt.subplots()
    
    # Définir les couleurs pour chaque item
    colors = plt.cm.tab20.colors
    
    for i, item in enumerate(bin):
        color = colors[i % len(colors)]
        plot_item(ax, item['position'], item['dimensions'], color)
    
    # Définir les dimensions de l'axe
    ax.set_xlim(0, bin_dims[0])
    ax.set_ylim(0, 1)  # Fixer l'axe y à une unité (dimension 1D)
    
    ax.set_xlabel('Longueur')
    ax.set_title(f'Conteneur {bin_index + 1} - Nombre d\'objets: {len(bin)}')
    plt.show()

def plot_item(ax, position, dimensions, color):
    x = position[0]
    dx = dimensions[0]
    rect = plt.Rectangle((x, 0), dx, 1, linewidth=1, edgecolor='r', facecolor=color, alpha=0.25)
    ax.add_patch(rect)

#Mesure du temps de calcul et appel de la fonction
start_time = time.time()
bins, num_bins, total_length, used_length, unused_length, total_items = first_fit_decreasing_1d(data, bin_dims)
end_time = time.time()

#Affichage des résultats
print(f"Nombre de wagons : {num_bins}")
print(f"Longueur totale : {total_length:.2f} mètres")
print(f"Longueur occupée : {used_length:.2f} mètres")
print(f"Longueur non occupée : {unused_length:.2f} mètres")
print(f"Temps de calcul : {end_time - start_time:.2f} secondes")

# Afficher le nombre total de conteneurs (wagons) et le nombre total d'objets
print(f"Nombre total de wagons utilisés : {num_bins}")
print(f"Nombre total de conteneurs placés : {total_items}")

# Visualiser chaque conteneur
for i, bin in enumerate(bins):
    print(f"Wagon {i + 1} - Nombre d'objets : {len(bin)}")
    plot_bin(bin, bin_dims, i)
