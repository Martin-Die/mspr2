import pandas as pd
import numpy as np
from datetime import datetime

# Analyser le fichier CSV
csv_file = "../extracted_csv/2019-Oct.csv"

print("🎯 ANALYSE DÉTAILLÉE POUR LA FIDÉLISATION CLIENT")
print("=" * 60)

# Lire un échantillon plus important
df = pd.read_csv(csv_file, nrows=50000)

print(f"📊 Données analysées : {len(df)} lignes")
print(f"📅 Période : {df['event_time'].min()} à {df['event_time'].max()}")

# Analyser les colonnes
print(f"\n📋 STRUCTURE DES DONNÉES :")
print(f"Colonnes disponibles ({len(df.columns)}):")
for i, col in enumerate(df.columns, 1):
    dtype = df[col].dtype
    missing_pct = (df[col].isna().sum() / len(df)) * 100
    unique_count = df[col].nunique()
    print(f"{i:2d}. {col} ({dtype}) - {missing_pct:.1f}% manquants - {unique_count} valeurs uniques")

# Analyser les types d'événements
print(f"\n🎯 TYPES D'ÉVÉNEMENTS (event_type):")
event_counts = df['event_type'].value_counts()
for event, count in event_counts.items():
    pct = (count / len(df)) * 100
    print(f"  - {event}: {count} ({pct:.1f}%)")

# Analyser les utilisateurs
print(f"\n👥 ANALYSE DES UTILISATEURS :")
user_stats = df.groupby('user_id').agg({
    'event_time': 'count',
    'price': ['sum', 'mean'],
    'event_type': 'nunique'
}).round(2)

user_stats.columns = ['nb_events', 'total_spent', 'avg_price', 'nb_event_types']
print(f"  - Nombre d'utilisateurs uniques : {df['user_id'].nunique()}")
print(f"  - Événements par utilisateur : {user_stats['nb_events'].mean():.1f} (moyenne)")
print(f"  - Dépenses par utilisateur : {user_stats['total_spent'].mean():.2f} (moyenne)")
print(f"  - Types d'événements par utilisateur : {user_stats['nb_event_types'].mean():.1f} (moyenne)")

# Analyser les produits et catégories
print(f"\n🛍️ ANALYSE DES PRODUITS :")
print(f"  - Nombre de produits uniques : {df['product_id'].nunique()}")
print(f"  - Nombre de catégories : {df['category_id'].nunique()}")
print(f"  - Nombre de marques : {df['brand'].nunique()}")

# Analyser les prix
print(f"\n💰 ANALYSE DES PRIX :")
print(f"  - Prix moyen : {df['price'].mean():.2f}")
print(f"  - Prix médian : {df['price'].median():.2f}")
print(f"  - Prix min : {df['price'].min():.2f}")
print(f"  - Prix max : {df['price'].max():.2f}")

# Identifier les variables pour la fidélisation
print(f"\n🎯 VARIABLES POUR LA FIDÉLISATION :")

# Variables cibles potentielles (à créer)
print(f"📊 Variables cibles à créer :")
print(f"  1. CHURN : Basé sur l'inactivité des utilisateurs")
print(f"  2. LIFETIME_VALUE : Valeur totale par utilisateur")
print(f"  3. ENGAGEMENT_SCORE : Fréquence d'activité")
print(f"  4. PURCHASE_FREQUENCY : Fréquence d'achat")
print(f"  5. CUSTOMER_SEGMENT : Segment basé sur RFM")

# Variables prédictives disponibles
print(f"\n📈 Variables prédictives disponibles :")
print(f"  ✅ user_id : Identifiant client")
print(f"  ✅ event_type : Type d'interaction")
print(f"  ✅ product_id : Produits consultés/achetés")
print(f"  ✅ category_id : Catégories préférées")
print(f"  ✅ brand : Marques préférées")
print(f"  ✅ price : Comportement de prix")
print(f"  ✅ event_time : Patterns temporels")
print(f"  ✅ user_session : Sessions utilisateur")

# Recommandations pour le modèle
print(f"\n🤖 RECOMMANDATIONS POUR LE MODÈLE IA :")

print(f"1. VARIABLES CIBLES À CRÉER :")
print(f"   - CHURN_BINARY : 1 si utilisateur inactif > 30 jours")
print(f"   - CUSTOMER_VALUE : Somme totale des achats")
print(f"   - ENGAGEMENT_LEVEL : Basé sur la fréquence d'événements")
print(f"   - PURCHASE_INTENT : Probabilité d'achat")

print(f"\n2. FEATURES À CRÉER :")
print(f"   - RFM_SCORE : Recency, Frequency, Monetary")
print(f"   - PRODUCT_PREFERENCES : Catégories/marques préférées")
print(f"   - PRICE_SENSITIVITY : Comportement face aux prix")
print(f"   - ACTIVITY_PATTERNS : Patterns temporels")
print(f"   - SESSION_BEHAVIOR : Comportement par session")

print(f"\n3. ALGORITHMES RECOMMANDÉS :")
print(f"   - Classification : Random Forest, XGBoost pour le churn")
print(f"   - Régression : Linear Regression, Random Forest pour LTV")
print(f"   - Clustering : K-Means pour la segmentation")

print(f"\n4. MÉTRIQUES DE PERFORMANCE :")
print(f"   - Pour le churn : Precision, Recall, F1-Score")
print(f"   - Pour LTV : RMSE, MAE, R²")
print(f"   - Pour segmentation : Silhouette Score")

print(f"\n5. PROCHAINES ÉTAPES :")
print(f"   1. Créer les variables cibles (churn, LTV)")
print(f"   2. Feature engineering (RFM, préférences)")
print(f"   3. Entraîner les modèles de prédiction")
print(f"   4. Valider et optimiser les performances")
print(f"   5. Déployer le système de fidélisation")

# Exemple de création de features
print(f"\n💡 EXEMPLE DE FEATURES À CRÉER :")

# Calculer quelques statistiques par utilisateur
user_features = df.groupby('user_id').agg({
    'event_time': ['count', 'min', 'max'],
    'price': ['sum', 'mean', 'std'],
    'event_type': 'nunique',
    'product_id': 'nunique',
    'category_id': 'nunique',
    'brand': 'nunique'
}).round(2)

user_features.columns = ['total_events', 'first_event', 'last_event', 
                        'total_spent', 'avg_price', 'price_std',
                        'event_types', 'products_viewed', 'categories_viewed', 'brands_viewed']

print(f"Features calculées pour {len(user_features)} utilisateurs :")
print(user_features.head())

print(f"\n✅ ANALYSE TERMINÉE - Prêt pour la modélisation IA !") 