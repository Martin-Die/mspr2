import pandas as pd
import os

INPUT_CSV = os.path.join('output', 'features_all_users.csv')
REPORT_PATH = os.path.join('model_ia_steps', 'exploration_report.txt')


def main():
    # Chargement des données
    df = pd.read_csv(INPUT_CSV)
    print(f"Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
    print(df.head())

    # Statistiques descriptives
    desc = df.describe(include='all')
    print(desc)

    # Valeurs manquantes
    missing = df.isnull().sum()
    print("Valeurs manquantes par colonne :")
    print(missing)

    # Valeurs aberrantes (exemple : valeurs négatives sur des colonnes qui ne devraient pas l'être)
    outliers = {}
    for col in df.select_dtypes(include=['number']).columns:
        if (df[col] < 0).any():
            outliers[col] = (df[col] < 0).sum()
    if outliers:
        print("Colonnes avec valeurs négatives :", outliers)
    else:
        print("Aucune valeur négative détectée dans les colonnes numériques.")

    # Sauvegarde d'un rapport d'exploration
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(f"Dimensions : {df.shape}\n\n")
        f.write("Aperçu :\n")
        f.write(str(df.head()))
        f.write("\n\nStatistiques descriptives :\n")
        f.write(str(desc))
        f.write("\n\nValeurs manquantes :\n")
        f.write(str(missing))
        f.write("\n\nValeurs négatives détectées :\n")
        f.write(str(outliers))
    print(f"Rapport d'exploration sauvegardé dans {REPORT_PATH}")

if __name__ == '__main__':
    main() 