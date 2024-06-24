import pandas as pd
import os
from get_path import getPath
import time

"question 7"

"""
Commencer
    
    Définir la fonction algo_sac_a_dos avec les paramètres objets et capacite_max
        Pour chaque objet dans objets
            Calculer le ratio utilité/masse et l'ajouter à objets

        Trier les objets par ratio utilité/masse en ordre décroissant

        Initialiser utilite_totale à 0
        Initialiser masse_totale à 0
        Initialiser objets_selectionnes comme une liste vide

        Pour chaque objet dans objets triés
            Si la masse totale plus la masse de l'objet est inférieure ou égale à capacite_max
                Ajouter l'objet à objets_selectionnes
                Ajouter la masse de l'objet à masse_totale
                Ajouter l'utilité de l'objet à utilite_totale

        Retourner objets_selectionnes, utilite_totale, masse_totale

    Définir capacite_max 

    Exécuter la fonction algo_sac_a_dos avec les données chargées et capacite_max
    Stocker les résultats dans objets_selectionnes, utilite_totale, masse_totale

    Affichage de
    "Objets sélectionnés:" 
    "Utilité totale:
    "Masse totale:"
Fin

"""


#////////////////////////////////
"question 8-9"
# Charger le fichier Excel
chemin_fichier = '/../data/Tableau données sac à dos. Vélo.xlsx'  

#Pour ajuster le chemin d'accès
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir, file_dir = getPath(script_dir, chemin_fichier)
data = pd.read_excel(os.path.join(script_dir + chemin_fichier))



def algo_sac_a_dos(objets, capacite_max):
    # Calculer le ratio utilité/masse pour chaque objet
    objets['Ratio_Utilite_Masse'] = objets['Utilité'] / objets['Masse']
    
    # Trier les objets par ratio utilité/masse décroissant
    objets_triees = objets.sort_values(by='Ratio_Utilite_Masse', ascending=False)
    
    # Initialiser les variables
    utilite_totale = 0
    masse_totale = 0
    objets_selectionnes = []
    
    # Sélectionner les objets
    for _, objet in objets_triees.iterrows():
        if masse_totale + objet['Masse'] <= capacite_max:
            objets_selectionnes.append(objet['Objet'])
            masse_totale += objet['Masse']
            utilite_totale += objet['Utilité']
    
    # Retourner les résultats
    return objets_selectionnes, utilite_totale, masse_totale


# Définir la capacité maximale du sac à dos
# Définir une liste des valeurs de capacité maximale
capacites_max = [2, 3, 4, 5]


# Boucle pour exécuter l'algorithme avec différentes capacités maximales
for capacite_max in capacites_max:
    start_time = time.time()
    objets_selectionnes, utilite_totale, masse_totale = algo_sac_a_dos(data, capacite_max)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    
    # Afficher les résultats
    print(f"Pour une capacité maximale de {capacite_max}:")
    print("Objets sélectionnés:", objets_selectionnes)
    print("Utilité totale:", utilite_totale)
    print("Masse totale:", masse_totale)
    print(f"Temps de calcul: {elapsed_time:.6f} secondes")
    print("l'algo n'est pas opti car il prends seulement les objets avec la plus grand ratio sans essayer de se rapprocher de la masse maximale")  # Pour ajouter une ligne vide entre les résultats