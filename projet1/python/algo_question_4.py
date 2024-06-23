def somme_premiers_nombres(n):
    somme = 0
    nombre_operations = 0
    for i in range(1, n + 1):
        somme += i
        nombre_operations += 1  # Pour chaque addition
    return somme, nombre_operations

# Exemple d'utilisation
n = 10
resultat, operations = somme_premiers_nombres(n)
print(f"La somme des {n} premiers nombres est {resultat} et le nombre d'opérations effectuées est {operations}.")
