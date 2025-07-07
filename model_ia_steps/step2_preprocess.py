import pandas as pd
import os
from sklearn.preprocessing import StandardScaler

INPUT_CSV = os.path.join('output', 'features_all_users.csv')
OUTPUT_CSV = os.path.join('model_ia_steps', 'features_normalized.csv')


def main():
    # Chargement des données
    df = pd.read_csv(INPUT_CSV)
    print(f"Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")

    # Sélection des colonnes numériques à normaliser (hors user_id)
    num_cols = [col for col in df.select_dtypes(include=['number']).columns if col != 'user_id']
    print(f"Colonnes numériques à normaliser : {num_cols}")

    # Gestion des valeurs extrêmes (optionnel : ici on les tronque à +/- 5 écarts-types)
    for col in num_cols:
        mean = df[col].mean()
        std = df[col].std()
        df[col] = df[col].clip(lower=mean-5*std, upper=mean+5*std)

    # Standardisation
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[num_cols] = scaler.fit_transform(df[num_cols])

    # Sauvegarde
    df_scaled.to_csv(OUTPUT_CSV, index=False)
    print(f"Données normalisées sauvegardées dans {OUTPUT_CSV}")

if __name__ == '__main__':
    main() 