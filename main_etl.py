import os
from etl_steps.extract import list_csv_files, extract_data_in_chunks
from etl_steps.transform import clean_data, create_features
from etl_steps.load import save_to_csv
import pandas as pd

DATASETS_DIR = 'datasets'
OUTPUT_DIR = 'output'
OUTPUT_CSV = os.path.join(OUTPUT_DIR, 'features_all_users.csv')
CHUNK_SIZE = 100000

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_features = []
    csv_files = list_csv_files(DATASETS_DIR)
    print(f"Fichiers à traiter : {csv_files}")
    for csv_file in csv_files:
        print(f"Traitement de {csv_file}...")
        for chunk in extract_data_in_chunks(csv_file, chunk_size=CHUNK_SIZE):
            cleaned = clean_data(chunk)
            features = create_features(cleaned)
            if not features.empty:
                all_features.append(features)
    if all_features:
        features_df = pd.concat(all_features, ignore_index=True)
        print(f"Nombre total d'utilisateurs traités : {len(features_df)}")
        save_to_csv(features_df, OUTPUT_CSV)
        print(f"Données sauvegardées dans {OUTPUT_CSV}")
    else:
        print("Aucune donnée utilisateur à sauvegarder.")

if __name__ == '__main__':
    main() 