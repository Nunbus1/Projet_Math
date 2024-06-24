import time

def somme_premiers_nombres(n):
    somme = 0
    nombre_operations = 0
    for i in range(1, n + 1):
        somme += i
        nombre_operations += 1  # Pour chaque addition
    return somme, nombre_operations

# Mesurer le temps de calcul pour différentes valeurs de n
valeurs_n = [10, 1000, 10000, 100000]
resultats = []

for n in valeurs_n:
    debut = time.time()
    somme, operations = somme_premiers_nombres(n)
    fin = time.time()
    duree = fin - debut
    temps_par_operation = duree / operations
    resultats.append((n, duree, temps_par_operation))
    print(f"Pour n = {n}:")
    print(f"  - Somme: {somme}")
    print(f"  - Nombre d'opérations: {operations}")
    print(f"  - Temps total: {duree:.6f} secondes")
    print(f"  - Temps par opération: {temps_par_operation:.12f} secondes\n")

# Afficher les résultats
print("Résultats:")
for res in resultats:
    print(f"n = {res[0]}, Temps total = {res[1]:.6f} sec, Temps par opération = {res[2]:.12f} sec")
