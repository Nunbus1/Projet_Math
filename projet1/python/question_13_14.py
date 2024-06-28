import pandas as pd



print("Question 13")


# Lire le DataFrame depuis le fichier CSV qui ont été pour l'algo A et B 
df_results_A = pd.read_csv('Projet_Math/projet1/data/resultats_algo_A.csv')
df_results_B = pd.read_csv('Projet_Math/projet1/data/resultats_algo_B.csv')

# Configurer pandas pour afficher toutes les colonnes et lignes
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Afficher le tableau des résultats des algorithmes
print("Algo A")
print()
print(df_results_A)
print("Algo B")
print()
print(df_results_B)

#Comparaison des algo A et B
print("L'algo A est moins rapide que l'algo B, mais il se rapproche le plus possible de poid maximal possible")
print("L'algo B lui est rapide mais n'est pas optimisé, il prends seulement les objets avec le ratio Utilité masse le plus élevé dans l'ordre croissant et il s'arrète avant d'attendre le poid maximal")
print()
print()
#//////////////////////////////////////////////////

print("question 14")

print("Les deux algorithmes ont des valeurs de temps de calcul infèrieur à 2 secondes")