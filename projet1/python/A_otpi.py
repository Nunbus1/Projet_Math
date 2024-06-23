import pandas as pd
import time

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

# Charger les données
chemin_fichier = 'projet1/data/Tableau données sac à dos. Vélo.xlsx'
data = pd.read_excel(chemin_fichier)

# Définir la capacité maximale du sac à dos
capacite_max = 2  # Par exemple

# Mesurer le temps de l'exécution de l'algorithme
debut = time.time()
objets_selectionnes, utilite_totale, masse_totale = algo_sac_a_dos_optimise(data, capacite_max)
fin = time.time()
duree = fin - debut

# Afficher les résultats
print("Objets sélectionnés:", objets_selectionnes)
print("Utilité totale:", utilite_totale)
print("Masse totale prise:", masse_totale)
print(f"Temps d'exécution: {duree:.6f} secondes")
