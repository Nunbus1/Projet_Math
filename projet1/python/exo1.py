import pandas as pd

# Charger le fichier Excel
chemin_fichier = 'projet1/data/Tableau données sac à dos. Vélo.xlsx'  # Chemin ajusté

# Lire le fichier Excel
data = pd.read_excel(chemin_fichier)

# Afficher les données chargées
#print(data)

# Définir la fonction pour calculer le nombre de combinaisons
def nombre_de_combinaisons(N):
    return 2 ** N

# Définir la liste des valeurs de N
valeurs_N = [1, 2, 10, 23]

# Calculer et imprimer le nombre de combinaisons pour chaque valeur de N
resultats = {N: nombre_de_combinaisons(N) for N in valeurs_N}

print("exo1")
for N, combinaisons in resultats.items():
    print(f"Le nombre de combinaisons possibles pour N = {N} est {combinaisons}")

print("exo2")
# Nombre total d'objets dans le sac à dos
nombre_total_objets = len(data)

# Calculer le nombre total de combinaisons possibles
nombre_total_combinaisons = 2 ** nombre_total_objets

print(f"Le nombre total d'organisations possibles pour le sac à dos, en incluant le sac vide et tous les objets, est {nombre_total_combinaisons}.")