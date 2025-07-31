import pandas as pd
import os

# Analyser un fichier CSV
csv_file = "../extracted_csv/2019-Oct.csv"

if os.path.exists(csv_file):
    print("📊 Analyse du fichier 2019-Oct.csv")
    print("=" * 40)
    
    # Lire les premières lignes
    df = pd.read_csv(csv_file, nrows=1000)
    
    print(f"Colonnes disponibles ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"{i:2d}. {col}")
    
    print(f"\nAperçu des données:")
    print(df.head(3))
    
    print(f"\nTypes de données:")
    print(df.dtypes.value_counts())
    
    print(f"\nInformations sur les colonnes numériques:")
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        print(f"- {col}: min={df[col].min()}, max={df[col].max()}, mean={df[col].mean():.2f}")
    
else:
    print("Fichier non trouvé") 