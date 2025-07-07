import os
import pandas as pd

DATASETS_DIR = 'datasets'
RESULTS_DIR = 'exploration_results'
CHUNK_SIZE = 10000  # Nombre de lignes à lire pour l'échantillon

# Crée le dossier de résultats s'il n'existe pas
os.makedirs(RESULTS_DIR, exist_ok=True)

# Liste les fichiers CSV dans le dossier datasets
for filename in os.listdir(DATASETS_DIR):
    if filename.endswith('.csv'):
        csv_path = os.path.join(DATASETS_DIR, filename)
        txt_name = os.path.splitext(filename)[0] + '.txt'
        txt_path = os.path.join(RESULTS_DIR, txt_name)

        print(f"Analyse de {filename}...")
        try:
            # Lecture d'un échantillon
            df = pd.read_csv(csv_path, nrows=CHUNK_SIZE)
        except Exception as e:
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"Erreur lors de la lecture du fichier : {e}\n")
            continue

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"Exploration du fichier : {filename}\n\n")
            f.write(f"Nombre de lignes chargées (échantillon) : {len(df)}\n\n")
            f.write("Aperçu des colonnes :\n")
            f.write(str(df.dtypes))
            f.write("\n\n")

            f.write("Valeurs manquantes par colonne :\n")
            f.write(str(df.isnull().sum()))
            f.write("\n\n")

            f.write("Statistiques descriptives numériques :\n")
            f.write(str(df.describe()))
            f.write("\n\n")

            f.write("Exemples de valeurs uniques par colonne :\n")
            for col in df.columns:
                uniques = df[col].unique()
                f.write(f"- {col} : {uniques[:10]}{' ...' if len(uniques) > 10 else ''}\n")
            f.write("\n")

        print(f"Rapport généré : {txt_path}") 