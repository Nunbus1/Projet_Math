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

# Define the maximum dimensions for the container
longueur_maximale = 11.583
largeur_maximale = 2.294

# Resolution for the grid
resolution = 10  # 10 cm resolution

# Function to check if an item can be placed in a given position in the container matrix
def peut_placer_matrice(conteneur, longueur, largeur, x, y):
    if x + longueur > longueur_maximale or y + largeur > largeur_maximale:
        return False
    return np.all(conteneur[int(x*resolution):int((x + longueur)*resolution), int(y*resolution):int((y + largeur)*resolution)] == 0)

# Function to place an item in the container matrix
def placer_dans_matrice(conteneur, longueur, largeur, x, y):
    conteneur[int(x*resolution):int((x + longueur)*resolution), int(y*resolution):int((y + largeur)*resolution)] = 1

# Function to generate rotations of an item
def generate_rotations(longueur, largeur):
    return [(longueur, largeur), (largeur, longueur)]

# First Fit Decreasing algorithm
def first_fit_decreasing(data, longueur_maximale, largeur_maximale):
    # Sort items by area in decreasing order
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

        for i, conteneur in enumerate(conteneurs):  # Try to place the item in existing containers
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

# Keep only the required columns
data = data[['Longueur', 'Largeur']]

# Convert columns to strings first
data['Longueur'] = data['Longueur'].astype(str)
data['Largeur'] = data['Largeur'].astype(str)

# Replace comma with dot and convert to numeric
data['Longueur'] = pd.to_numeric(data['Longueur'].str.replace(',', '.'), errors='coerce')
data['Largeur'] = pd.to_numeric(data['Largeur'].str.replace(',', '.'), errors='coerce')

# Drop rows with NaN values (which couldn't be converted to numbers)
data.dropna(inplace=True)

# Measure the time taken for allocation
temps_debut = time.time()
conteneurs, items_in_conteneurs = first_fit_decreasing(data, longueur_maximale, largeur_maximale)
temps_fin = time.time()

# Calculate unoccupied areas
total_area = longueur_maximale * largeur_maximale
unoccupied_areas = []
for conteneur in conteneurs:
    occupied_area = np.sum(conteneur) / (resolution ** 2)
    unoccupied_area = total_area - occupied_area
    unoccupied_areas.append(unoccupied_area)

total_unoccupied_area = sum(unoccupied_areas)
average_unoccupied_area = total_unoccupied_area / len(conteneurs)

# Print the results
print(f"Nombre de conteneurs utilisés : {len(conteneurs)}")
print(f"Temps de calcul : {temps_fin - temps_debut} secondes")
print(f"Aire totale innocupée : {total_unoccupied_area:.2f} m²")
print(f"Aire moyenne innocupée par wagon : {average_unoccupied_area:.2f} m²")

# Afficher les wagons utilisés un par un avec leurs détails
for i, items in enumerate(items_in_conteneurs):
    plt.figure(figsize=(8, 6))
    for item in items:
        longueur, largeur, x, y = item
        plt.fill([y, y, y + largeur, y + largeur], [x, x + longueur, x + longueur, x], label=f'Article {longueur}m x {largeur}m')
    plt.xlim(0, largeur_maximale)
    plt.ylim(0, longueur_maximale)
    plt.gca().invert_yaxis()
    plt.xlabel('Largeur')
    plt.ylabel('Longueur')
    plt.title(f'Conteneur {i+1}')
    plt.legend()
    plt.show()
