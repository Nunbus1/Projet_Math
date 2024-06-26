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

# # Fonction pour vérifier si un article peut être placé à une position donnée dans la matrice du conteneur
def peut_placer_matrice(conteneur, longueur, largeur, x, y):
    # Vérifie si les coordonnées de l'article dépassent les limites du conteneur
    if x + longueur > longueur_maximale or y + largeur > largeur_maximale:
        return False
     # Vérifie si la zone dans le conteneur où l'article doit être placé est libre (contient des zéros)
    return np.all(conteneur[int(x*resolution):int((x + longueur)*resolution), int(y*resolution):int((y + largeur)*resolution)] == 0)

# Fonction pour placer un article dans la matrice du conteneur
def placer_dans_matrice(conteneur, longueur, largeur, x, y):
    # Marque la zone dans le conteneur où l'article est placé comme occupée (avec des uns)
    conteneur[int(x*resolution):int((x + longueur)*resolution), int(y*resolution):int((y + largeur)*resolution)] = 1

# Fonction pour générer toutes les rotations possibles d'un article
def generate_rotations(longueur, largeur):
    # Retourne une liste de tuples représentant les dimensions de l'article dans ses rotations possibles (0° et 90°)
    return [(longueur, largeur), (largeur, longueur)]

# First Fit Decreasing algorithm
def first_fit_decreasing(data, longueur_maximale, largeur_maximale):
    # Calcul de l'aire et tri par ordre décroissant 
    data['Area'] = data['Longueur'] * data['Largeur']
    data = data.sort_values(by='Area', ascending=False)

    #Initialisation des conteneurs et des paramètres :
    conteneurs = []
    items_in_conteneurs = []
    longueur_maximale_int = int(longueur_maximale * resolution)
    largeur_maximale_int = int(largeur_maximale * resolution)

    #Placement des articles
    for _, marchandise in data.iterrows():
        longueur = marchandise['Longueur']
        largeur = marchandise['Largeur']
        placer = False

        #Essai de placement dans les conteneurs existants
        for i, conteneur in enumerate(conteneurs):  
            for rotation in generate_rotations(longueur, largeur):
                r_longueur, r_largeur = rotation

                #Essai de placement dans le conteneur :
                for x in range(0, longueur_maximale_int - int(r_longueur * resolution) + 1):
                    for y in range(0, largeur_maximale_int - int(r_largeur * resolution) + 1):
                        if peut_placer_matrice(conteneur, r_longueur, r_largeur, x / resolution, y / resolution):
                            placer_dans_matrice(conteneur, r_longueur, r_largeur, x / resolution, y / resolution)
                            items_in_conteneurs[i].append((r_longueur, r_largeur, x / resolution, y / resolution))
                            placer = True
                            break
                    #Création d'un nouveau conteneur     
                    if placer:
                        break
                if placer:
                    break
            if placer:
                break
        #Création d'un nouveau conteneur        
        if not placer:
            new_conteneur = np.zeros((longueur_maximale_int, largeur_maximale_int))
            placer_dans_matrice(new_conteneur, longueur, largeur, 0, 0)
            conteneurs.append(new_conteneur)
            items_in_conteneurs.append([(longueur, largeur, 0, 0)])
    #Retour des résultats
    return conteneurs, items_in_conteneurs

# Préparation des données
data = data[['Longueur', 'Largeur']]
#Conversion des colonnes en chaînes de caractères
data['Longueur'] = data['Longueur'].astype(str)
data['Largeur'] = data['Largeur'].astype(str)
#Remplacement des virgules par des points et conversion en numériques
data['Longueur'] = pd.to_numeric(data['Longueur'].str.replace(',', '.'), errors='coerce')
data['Largeur'] = pd.to_numeric(data['Largeur'].str.replace(',', '.'), errors='coerce')
#permet de supprimer toutes les lignes ou colonnes qui contiennent des valeurs NaN
data.dropna(inplace=True)

#  Exécution de l'algorithme et mesures
temps_debut = time.time()
conteneurs, items_in_conteneurs = first_fit_decreasing(data, longueur_maximale, largeur_maximale)
temps_fin = time.time()

#  Calcul des aires innocupées
total_area = longueur_maximale * largeur_maximale
unoccupied_areas = []
for conteneur in conteneurs:
    occupied_area = np.sum(conteneur) / (resolution ** 2)
    unoccupied_area = total_area - occupied_area
    unoccupied_areas.append(unoccupied_area)

total_unoccupied_area = sum(unoccupied_areas)
average_unoccupied_area = total_unoccupied_area / len(conteneurs)

#  Affichage des résultats
print(f"Nombre de conteneurs utilisés : {len(conteneurs)}")
print(f"Aire moyenne innocupée par wagon : {average_unoccupied_area:.2f} m²")
print(f"Aire totale innocupée : {total_unoccupied_area:.2f} m²")
print(f"Temps de calcul : {temps_fin - temps_debut} secondes")

#  Visualisation des conteneurs
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
