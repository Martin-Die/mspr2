"""
extract.py
Étape 1 du pipeline ETL : Extraction des données brutes depuis les fichiers sources.
Optimisé pour les gros fichiers CSV.
"""
import os
import pandas as pd
from typing import List, Iterator, Optional

def list_csv_files(datasets_dir: str) -> List[str]:
    """Liste les fichiers CSV dans le dossier datasets."""
    return [os.path.join(datasets_dir, f) for f in os.listdir(datasets_dir) if f.endswith('.csv')]

def extract_data_in_chunks(file_path: str, chunk_size: int = 100000) -> Iterator[pd.DataFrame]:
    """
    Extrait les données d'un gros fichier CSV par morceaux (chunks).
    Args:
        file_path: Chemin du fichier CSV.
        chunk_size: Nombre de lignes par chunk.
    Returns:
        Un itérateur de DataFrames pandas.
    """
    return pd.read_csv(file_path, chunksize=chunk_size)

def get_csv_columns(file_path: str) -> List[str]:
    """Retourne la liste des colonnes d'un fichier CSV sans tout charger en mémoire."""
    df = pd.read_csv(file_path, nrows=0)
    return list(df.columns)

def extract_data(file_path: str, nrows: Optional[int] = None) -> pd.DataFrame:
    """Extrait les données d'un fichier CSV et retourne un DataFrame pandas.
    Args:
        file_path: Chemin du fichier CSV.
        nrows: Nombre de lignes à lire (optionnel).
    Returns:
        DataFrame pandas contenant les données extraites, ou None si erreur.
    """
    try:
        df = pd.read_csv(file_path, nrows=nrows)
        return df
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path} : {e}")
        return None 