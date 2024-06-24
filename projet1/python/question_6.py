import time




def somme_premiers_nombres(n):
    somme = 0
    nombre_operations = 0
    for i in range(1, n + 1):
        somme += i
        nombre_operations += 1  # Pour chaque addition
    return somme, nombre_operations

# Mesurer le temps de calcul pour une grande valeur de n pour estimer T
n = 1000000  # Utiliser une grande valeur de n pour une estimation précise
debut = time.time()
somme, operations = somme_premiers_nombres(n)
fin = time.time()
duree = fin - debut
temps_par_operation = duree / operations


# Calculer le nombre total d'organisations possibles
nombre_organisations = 8388608.0

# Calculer le temps total nécessaire
temps_total = nombre_organisations * temps_par_operation

#:.12f formatte le nombre temps_par_operation pour qu'il soit affiché avec exactement 12 chiffres après la virgule décimale.

print(f"Nombre total d'organisations possibles: {nombre_organisations}")
print(f"Temps moyen par opération: {temps_par_operation:.12f} secondes")
print(f"Temps total estimé pour tester toutes les organisations: {temps_total:.2f} secondes")

