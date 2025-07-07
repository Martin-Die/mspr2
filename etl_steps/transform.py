"""
transform.py
Étape 2 du pipeline ETL : Transformation et nettoyage des données, création des variables explicatives.
"""
import pandas as pd
from typing import List

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les données brutes :
    - Gère les valeurs manquantes (remplissage ou suppression)
    - Uniformise les types de colonnes
    - Filtre les lignes inutiles (ex : user_id manquant)
    """
    df = df.copy()
    # Suppression des lignes sans user_id
    df = df.dropna(subset=['user_id'])
    # Remplissage des valeurs manquantes pour les colonnes non critiques
    if 'brand' in df.columns:
        df['brand'] = df['brand'].fillna('unknown')
    # Conversion des types
    if 'event_time' in df.columns:
        df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
    return df

def create_features(df: pd.DataFrame, min_events: int = 10) -> pd.DataFrame:
    """
    Crée les variables explicatives pour chaque utilisateur :
    - Nombre d'événements par type
    - Montant total dépensé
    - Nombre de catégories visitées/achetées
    - Prix moyen d'achat
    - Taux de conversion
    - Filtre les utilisateurs avec peu d'activité
    """
    if 'user_id' not in df.columns or 'event_type' not in df.columns:
        return pd.DataFrame()
    # Nombre d'événements par utilisateur et par type
    event_counts = df.pivot_table(index='user_id', columns='event_type', values='event_time', aggfunc='count', fill_value=0)
    # Montant total dépensé
    if 'price' in df.columns and 'event_type' in df.columns:
        spent = df[df['event_type']=='purchase'].groupby('user_id')['price'].sum().rename('total_spent')
        avg_price = df[df['event_type']=='purchase'].groupby('user_id')['price'].mean().rename('avg_purchase_price')
    else:
        spent = pd.Series(dtype=float, name='total_spent')
        avg_price = pd.Series(dtype=float, name='avg_purchase_price')
    # Nombre de catégories différentes visitées
    if 'category_id' in df.columns:
        n_cat = df.groupby('user_id')['category_id'].nunique().rename('unique_categories')
    else:
        n_cat = pd.Series(dtype=int, name='unique_categories')
    # Taux de conversion (achats / visites)
    purchases = event_counts['purchase'] if 'purchase' in event_counts.columns else pd.Series(0, index=event_counts.index)
    views = event_counts['view'] if 'view' in event_counts.columns else pd.Series(1, index=event_counts.index)
    conv = (purchases / views).rename('conversion_rate')
    # Fusion des features
    features = pd.concat([event_counts, spent, n_cat, avg_price, conv], axis=1)
    # Remplacement des NaN par 0
    features = features.fillna(0)
    # Filtrage des utilisateurs peu actifs
    features = features[features.sum(axis=1) >= min_events]
    return features.reset_index() 