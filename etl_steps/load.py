"""
load.py
Étape 3 du pipeline ETL : Chargement des données transformées vers la destination (fichier, base, etc.).
"""
import pandas as pd
from sqlalchemy import create_engine

def save_to_csv(df: pd.DataFrame, output_path: str):
    """Enregistre le DataFrame transformé dans un fichier CSV."""
    df.to_csv(output_path, index=False)

def save_to_database(df: pd.DataFrame, connection_string: str, table_name: str):
    """
    Enregistre le DataFrame transformé dans une base de données PostgreSQL (ex : ElephantSQL).
    Args:
        df: DataFrame à sauvegarder
        connection_string: Chaîne de connexion SQLAlchemy (ex : postgresql://user:pass@host/db)
        table_name: Nom de la table cible
    """
    try:
        engine = create_engine(connection_string)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Données sauvegardées dans la table {table_name}.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde en base : {e}") 