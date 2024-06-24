import pandas as pd
import time
from math import prod

# Charger les données depuis le fichier Excel
file_path = 'projet2/data/Données marchandises.xlsx'
data = pd.read_excel(file_path)

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
    for _, item in data_sorted.iterrows():
        item_dims = (item['Longueur'], item['Largeur'], item['Hauteur'])
        placed = False

        for bin in bins:
            if can_place_in_bin(item_dims, bin, bin_dims):
                bin.append(item_dims)
                placed = True
                break
        
        if not placed:
            bins.append([item_dims])
    
    total_volume = len(bins) * prod(bin_dims)
    used_volume = sum(prod(item) for bin in bins for item in bin)
    unused_volume = total_volume - used_volume
    return len(bins), total_volume, used_volume, unused_volume

start_time = time.time()
num_bins, total_volume, used_volume, unused_volume = first_fit_decreasing_3d(data, bin_dims)
end_time = time.time()

print(f"Nombre de conteneurs : {num_bins}")
print(f"Volume total : {total_volume:.2f} mètres cubes")
print(f"Volume occupé : {used_volume:.2f} mètres cubes")
print(f"Volume non occupé : {unused_volume:.2f} mètres cubes")
print(f"Temps de calcul : {end_time - start_time:.2f} secondes")
