import pandas as pd
import time
from get_path import getPath
import os


# Charger le fichier Excel
chemin_fichier = '/../data/Tableau données sac à dos. Vélo.xlsx'  

#Pour ajuster le chemin d'accès

#Déterminer le répertoire du script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Ajuster les chemins en fonction du système d'exploitation
script_dir, file_dir = getPath(script_dir, chemin_fichier)
#Lire le fichier Excel
data = pd.read_excel(os.path.join(script_dir + chemin_fichier))

def algo_sac_a_dos_optimise(objets, capacite_max):
    n = len(objets)
    capacite_max = int(capacite_max * 100)  # Pour éviter les problèmes de flottants

    # Initialiser le tableau dp
    dp = [0] * (capacite_max + 1)
    keep = [[False] * (capacite_max + 1) for _ in range(n)]

    # Remplir le tableau dp
    for i in range(n):
        masse = int(objets.iloc[i]['Masse'] * 100)  # Convertir en entier
        utilite = objets.iloc[i]['Utilité']
        for w in range(capacite_max, masse - 1, -1):
            if dp[w] < dp[w - masse] + utilite:
                dp[w] = dp[w - masse] + utilite
                keep[i][w] = True

    # Backtracking pour trouver les objets sélectionnés
    w = capacite_max
    objets_selectionnes = []
    masse_totale = 0

    for i in range(n - 1, -1, -1):
        if keep[i][w]:
            objets_selectionnes.append(objets.iloc[i]['Objet'])
            masse_totale += objets.iloc[i]['Masse']
            w -= int(objets.iloc[i]['Masse'] * 100)

    utilite_totale = dp[capacite_max]
    return objets_selectionnes, utilite_totale, masse_totale



# Définir la capacité maximale du sac à dos
# Définir une liste des valeurs de capacité maximale
capacites_max = [2, 3, 4, 5]
results = []

# Boucle pour exécuter l'algorithme avec différentes capacités maximales
for capacite_max in capacites_max:
    start_time = time.time()
    objets_selectionnes, utilite_totale, masse_totale = algo_sac_a_dos_optimise(data, capacite_max)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    
   
     # Enregistrer les résultats dans un dictionnaire
    result = {
        "Capacité Max": capacite_max,
        "Objets Sélectionnés": objets_selectionnes,
        "Utilité Totale": utilite_totale,
        "Masse Totale": masse_totale,
        "Temps de Calcul (s)": elapsed_time
    }
    
    # Ajouter le dictionnaire à la liste des résultats
    results.append(result)

# Convertir la liste des résultats en un DataFrame pandas
df_results = pd.DataFrame(results)
# Configurer pandas pour afficher toutes les colonnes et lignes
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# Afficher le tableau des résultats
print(df_results)


# Sauvegarder le DataFrame dans un fichier CSV
#Pour ajuster le chemin d'accès
chemin_csv = '/../data/resultat_algo_A.csv'

script_dir_csv = os.path.dirname(os.path.abspath(__file__))
script_dir_csv, file_dir = getPath(script_dir_csv, chemin_csv)
adresse =os.path.join(script_dir + file_dir)
df_results.to_csv(adresse, index=False)
print("Les résultats ont été enregistrés dans 'resultats.csv'.")