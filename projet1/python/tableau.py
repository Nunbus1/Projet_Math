import pandas as pd

# Chemins des fichiers
chemin_fichier = 'projet1/data/Tableau données sac à dos. Vélo.xlsx'
fichier_modifier = 'projet1/data/tab_arrang.xlsx'
fic_fin = 'projet1/data/tab_fin.xlsx'

# Lire le fichier Excel
data = pd.read_excel(chemin_fichier)

# Trier les données
data_dec_utilite = data.sort_values(by='Utilité', ascending=False)
data_dec_masse = data.sort_values(by='Masse', ascending=True)

# Calculer le ratio utilité/masse
data['Ratio_Utilite_Masse'] = data['Utilité'] / data['Masse']
data_dec_ratio = data.sort_values(by='Ratio_Utilite_Masse', ascending=False)

# Renommer les colonnes pour éviter les conflits
data_dec_utilite.columns = [f'{col}_utilite' for col in data_dec_utilite.columns]
data_dec_masse.columns = [f'{col}_masse' for col in data_dec_masse.columns]

# Combiner les deux DataFrames côte à côte
data_combined = pd.concat([data_dec_utilite.reset_index(drop=True), data_dec_masse.reset_index(drop=True)], axis=1)

# Écrire les données combinées dans le fichier tab_arrang.xlsx
data_combined.to_excel(fichier_modifier, index=False)

# Écrire data_dec_ratio dans un autre fichier Excel tab_fin.xlsx
data_dec_ratio.to_excel(fic_fin, sheet_name='tab_fin', index=False)

print("Les données ont été écrites dans les fichiers", fichier_modifier, "et", fic_fin)
