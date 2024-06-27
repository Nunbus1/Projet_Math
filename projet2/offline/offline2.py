import numpy as np
import os
import pandas as pd
import time
import matplotlib.pyplot as plt

# Charger les données depuis le fichier Excel
chemin_fichier = '/../data/Données marchandises.xlsx'

# Pour ajuster le chemin d'accès
script_dir = os.path.dirname(os.path.abspath(__file__))

data = pd.read_excel(os.path.join(script_dir + chemin_fichier))

# Définir les dimensions maximales pour le conteneur
longueur_maximale = 11.583
largeur_maximale = 2.294

# Resolution pour le grid
resolution = 10  

# Fonction pour vérifier si un article peut être placé à une position donnée dans la matrice du conteneur
def peut_placer_matrice(conteneur, longueur, largeur, x, y):
    if x + longueur > longueur_maximale or y + largeur > largeur_maximale:
        return False
    return np.all(conteneur[int(x*resolution):int((x + longueur)*resolution), int(y*resolution):int((y + largeur)*resolution)] == 0)

# Fonction pour placer un article dans la matrice du conteneur
def placer_dans_matrice(conteneur, longueur, largeur, x, y):
    conteneur[int(x*resolution):int((x + longueur)*resolution), int(y*resolution):int((y + largeur)*resolution)] = 1

# Fonction pour générer toutes les rotations possibles d'un article
def generate_rotations(longueur, largeur):
    return [(longueur, largeur), (largeur, longueur)]

# First Fit Decreasing algorithm
def first_fit_decreasing(data, longueur_maximale, largeur_maximale):
    data['Area'] = data['Longueur'] * data['Largeur']
    data = data.sort_values(by='Area', ascending=False)

    conteneurs = []
    items_in_conteneurs = []
    longueur_maximale_int = int(longueur_maximale * resolution)
    largeur_maximale_int = int(largeur_maximale * resolution)

    for _, marchandise in data.iterrows():
        longueur = marchandise['Longueur']
        largeur = marchandise['Largeur']
        placer = False

        for i, conteneur in enumerate(conteneurs):
            for rotation in generate_rotations(longueur, largeur):
                r_longueur, r_largeur = rotation
                for x in range(0, longueur_maximale_int - int(r_longueur * resolution) + 1):
                    for y in range(0, largeur_maximale_int - int(r_largeur * resolution) + 1):
                        if peut_placer_matrice(conteneur, r_longueur, r_largeur, x / resolution, y / resolution):
                            placer_dans_matrice(conteneur, r_longueur, r_largeur, x / resolution, y / resolution)
                            items_in_conteneurs[i].append((r_longueur, r_largeur, x / resolution, y / resolution))
                            placer = True
                            break
                    if placer:
                        break
                if placer:
                    break
            if placer:
                break
        if not placer:
            new_conteneur = np.zeros((longueur_maximale_int, largeur_maximale_int))
            placer_dans_matrice(new_conteneur, longueur, largeur, 0, 0)
            conteneurs.append(new_conteneur)
            items_in_conteneurs.append([(longueur, largeur, 0, 0)])
    return conteneurs, items_in_conteneurs

# Préparation des données
data = data[['Longueur', 'Largeur']]
data['Longueur'] = data['Longueur'].astype(str)
data['Largeur'] = data['Largeur'].astype(str)
data['Longueur'] = pd.to_numeric(data['Longueur'].str.replace(',', '.'), errors='coerce')
data['Largeur'] = pd.to_numeric(data['Largeur'].str.replace(',', '.'), errors='coerce')
data.dropna(inplace=True)

temps_debut = time.time()
conteneurs, items_in_conteneurs = first_fit_decreasing(data, longueur_maximale, largeur_maximale)
temps_fin = time.time()

total_area = longueur_maximale * largeur_maximale
unoccupied_areas = []
for conteneur in conteneurs:
    occupied_area = np.sum(conteneur) / (resolution ** 2)
    unoccupied_area = total_area - occupied_area
    unoccupied_areas.append(unoccupied_area)

total_unoccupied_area = sum(unoccupied_areas)
average_unoccupied_area = total_unoccupied_area / len(conteneurs)

print(f"Nombre de conteneurs utilisés : {len(conteneurs)}")
print(f"Aire moyenne innocupée par wagon : {average_unoccupied_area:.2f} m²")
print(f"Aire totale innocupée : {total_unoccupied_area:.2f} m²")
print(f"Temps de calcul : {temps_fin - temps_debut} secondes")

def plot_bins_on_sheet(conteneurs, items_in_conteneurs, longueur_maximale, largeur_maximale):
    num_bins = len(conteneurs)
    num_cols = 4
    num_rows = (num_bins + num_cols - 1) // num_cols

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(num_cols * 5, num_rows * 5), constrained_layout=True)
    colors = plt.cm.tab20.colors
    axs = axs.flatten()

    for i, items in enumerate(items_in_conteneurs):
        ax = axs[i]
        for j, item in enumerate(items):
            longueur, largeur, x, y = item
            color = colors[j % len(colors)]
            ax.fill([y, y, y + largeur, y + largeur], [x, x + longueur, x + longueur, x], color=color, alpha=0.5)
        
        ax.set_xlim(0, largeur_maximale)
        ax.set_ylim(0, longueur_maximale)
        ax.invert_yaxis()
        ax.set_xlabel('Largeur')
        ax.set_ylabel('Longueur')
        ax.set_title(f'Conteneur {i + 1}')
    
    for j in range(i + 1, len(axs)):
        fig.delaxes(axs[j])

    plt.show()

plot_bins_on_sheet(conteneurs, items_in_conteneurs, longueur_maximale, largeur_maximale)
