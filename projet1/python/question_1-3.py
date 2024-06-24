import pandas as pd
import os
import platform
import math

from get_path import getPath

###
#Pour que ça marche avec le chemind d'accès
# Charger le fichier Excel
chemin_fichier = '/../data/Tableau données sac à dos. Vélo.xlsx'  # Chemin ajusté

script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir, file_dir = getPath(script_dir, chemin_fichier)



data = pd.read_excel(os.path.join(script_dir + chemin_fichier))



#//////////////////////////////////////////////////////////////////////


print("Question 1")

# Définir la fonction pour calculer le nombre de combinaisons
def nombre_de_combinaisons(N):
    return math.factorial(23)/(math.factorial(N)*math.factorial(23-N))


# Définir la liste des valeurs de N
valeurs_N = [1, 2, 10, 23]

# Calculer et imprimer le nombre de combinaisons pour chaque valeur de N
resultats = {N: nombre_de_combinaisons(N) for N in valeurs_N}


for N, combinaisons in resultats.items():
    print(f"Le nombre de sac de {N} objet est {combinaisons} sacs")

#//////////////////////////////////////////////////////////////////////

print("Question 2")
def somme_combinaisons():
    somme = 0
    for N in range(24):  # De 0 à 23 inclus
        somme += nombre_de_combinaisons(N)
    return somme

# Exemple d'utilisation
print(f"La somme des combinaisons de 0 à 23 est {somme_combinaisons()}")    



#/////////////////////////////////

print("Question 3")

print("Le tab_fin.xlsx dans data, est un tableau qui classe les objets en faisant un ratio (utilite/poids)")
print("On additionne les objets avec les meilleurs ratio dans un ordre décroissant jusqu'à arriver à une masse totale de 0.6")
tab= {
    'Objets': ['Rustines', 'Maillon rapide', 'Démonte-pneus', 'Bouchon valve', 'Multi-tool', 'Couteau suisse'],
}
df = pd.DataFrame(tab)
print(df)
print("Avec ces objets on arrive à 0.61 donc on choisit d'enlever Bouchon Valve afin d'arriver à C = 0.6")
df = df[df['Objets'] != 'Bouchon valve']
print("On obteint cette liste d'objets")
print(df)