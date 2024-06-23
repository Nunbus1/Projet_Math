import pandas as pd

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

# Charger les données
chemin_fichier = 'projet1/data/Tableau données sac à dos. Vélo.xlsx'
data = pd.read_excel(chemin_fichier)

# Définir la capacité maximale du sac à dos
capacite_max = 2  # Par exemple

# Exécuter l'algorithme
objets_selectionnes, utilite_totale, masse_totale = algo_sac_a_dos(data, capacite_max)

# Afficher les résultats
print("Objets sélectionnés:", objets_selectionnes)
print("Utilité totale:", utilite_totale)
print("Masse totale:", masse_totale)
