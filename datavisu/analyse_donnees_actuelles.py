"""
analyse_donnees_actuelles.py
Script pour analyser rapidement la structure des données CSV actuelles
et identifier les variables intéressantes pour la fidélisation client.
"""
import pandas as pd
import os
from pathlib import Path

def analyser_structure_csv():
    """Analyse la structure des fichiers CSV disponibles."""
    print("🔍 ANALYSE DES DONNÉES CSV ACTUELLES")
    print("=" * 50)
    
    # Chemin vers les fichiers CSV
    csv_dir = Path("../extracted_csv")
    
    if not csv_dir.exists():
        print("❌ Dossier extracted_csv non trouvé")
        return
    
    # Lister les fichiers CSV
    csv_files = list(csv_dir.glob("*.csv"))
    print(f"📁 {len(csv_files)} fichier(s) CSV trouvé(s)")
    
    for csv_file in csv_files:
        print(f"\n📊 Analyse de {csv_file.name}")
        print("-" * 30)
        
        try:
            # Lire les premières lignes pour analyser la structure
            df_sample = pd.read_csv(csv_file, nrows=1000)
            
            print(f"   Taille échantillon : {len(df_sample)} lignes")
            print(f"   Nombre de colonnes : {len(df_sample.columns)}")
            print(f"   Taille mémoire : {df_sample.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            # Afficher les colonnes
            print(f"\n   📋 Colonnes disponibles :")
            for i, col in enumerate(df_sample.columns, 1):
                dtype = df_sample[col].dtype
                missing_pct = (df_sample[col].isna().sum() / len(df_sample)) * 100
                print(f"   {i:2d}. {col} ({dtype}) - {missing_pct:.1f}% manquants")
            
            # Identifier les variables importantes pour la fidélisation
            print(f"\n   🎯 Variables importantes pour la fidélisation :")
            
            # Variables cibles potentielles
            target_keywords = ['churn', 'retention', 'loyalty', 'satisfaction', 'score', 'rating',
                             'fidelity', 'engagement', 'activity', 'frequency', 'recency',
                             'monetary', 'value', 'status', 'tier', 'level', 'premium',
                             'active', 'inactive', 'canceled', 'suspended', 'vip', 'gold',
                             'silver', 'bronze', 'platinum', 'diamond', 'elite']
            
            target_vars = []
            for col in df_sample.columns:
                col_lower = col.lower()
                for keyword in target_keywords:
                    if keyword in col_lower:
                        target_vars.append(col)
                        break
            
            if target_vars:
                print(f"   ✅ Variables cibles identifiées :")
                for var in target_vars:
                    print(f"      - {var}")
            else:
                print(f"   ⚠️ Aucune variable cible identifiée")
            
            # Variables prédictives importantes
            predictor_keywords = ['age', 'income', 'spending', 'purchase', 'order', 'transaction',
                                'frequency', 'recency', 'monetary', 'total', 'amount', 'value',
                                'duration', 'tenure', 'membership', 'subscription', 'plan',
                                'category', 'product', 'service', 'location', 'region', 'city',
                                'country', 'gender', 'education', 'occupation', 'marital',
                                'children', 'household', 'credit', 'score', 'rating', 'review',
                                'complaint', 'support', 'interaction', 'contact', 'email',
                                'phone', 'mobile', 'web', 'app', 'online', 'offline']
            
            predictor_vars = []
            for col in df_sample.columns:
                col_lower = col.lower()
                for keyword in predictor_keywords:
                    if keyword in col_lower:
                        predictor_vars.append(col)
                        break
            
            if predictor_vars:
                print(f"   📊 Variables prédictives identifiées :")
                for var in predictor_vars[:10]:  # Top 10
                    print(f"      - {var}")
                if len(predictor_vars) > 10:
                    print(f"      ... et {len(predictor_vars) - 10} autres")
            else:
                print(f"   ⚠️ Aucune variable prédictive identifiée")
            
            # Analyser les types de données
            print(f"\n   📈 Types de données :")
            numeric_cols = df_sample.select_dtypes(include=['number']).columns
            categorical_cols = df_sample.select_dtypes(include=['object']).columns
            datetime_cols = df_sample.select_dtypes(include=['datetime']).columns
            
            print(f"      - Numériques : {len(numeric_cols)}")
            print(f"      - Catégorielles : {len(categorical_cols)}")
            print(f"      - Dates : {len(datetime_cols)}")
            
            # Aperçu des données
            print(f"\n   👀 Aperçu des données :")
            print(df_sample.head(3).to_string())
            
        except Exception as e:
            print(f"   ❌ Erreur lors de l'analyse : {e}")
        
        print("\n" + "="*50)

def analyser_potentiel_fidelisation():
    """Analyse le potentiel de fidélisation basé sur les données."""
    print("\n🎯 ANALYSE DU POTENTIEL DE FIDÉLISATION")
    print("=" * 50)
    
    # Analyser un fichier spécifique
    csv_file = Path("../extracted_csv/2019-Oct.csv")
    
    if not csv_file.exists():
        print("❌ Fichier 2019-Oct.csv non trouvé")
        return
    
    try:
        # Charger un échantillon plus important
        df = pd.read_csv(csv_file, nrows=10000)
        
        print(f"📊 Analyse basée sur {len(df)} lignes de données")
        
        # Identifier les variables clés
        target_vars = []
        predictor_vars = []
        
        for col in df.columns:
            col_lower = col.lower()
            
            # Variables cibles
            if any(keyword in col_lower for keyword in ['churn', 'retention', 'loyalty', 'satisfaction']):
                target_vars.append(col)
            
            # Variables prédictives
            if any(keyword in col_lower for keyword in ['customer', 'user', 'client', 'id', 'amount', 'price', 'quantity', 'date', 'time']):
                predictor_vars.append(col)
        
        print(f"\n🎯 Variables cibles potentielles : {len(target_vars)}")
        for var in target_vars:
            print(f"   - {var}")
        
        print(f"\n📊 Variables prédictives identifiées : {len(predictor_vars)}")
        for var in predictor_vars[:15]:  # Top 15
            print(f"   - {var}")
        
        # Recommandations
        print(f"\n🤖 RECOMMANDATIONS POUR LA FIDÉLISATION :")
        
        if target_vars:
            print(f"   ✅ Variables cibles disponibles pour l'entraînement")
            print(f"   🎯 Modèle recommandé : Classification binaire/multiclasse")
        else:
            print(f"   ⚠️ Aucune variable cible identifiée")
            print(f"   💡 Recommandations :")
            print(f"      - Créer une variable 'churn' basée sur l'inactivité")
            print(f"      - Calculer un 'lifetime_value' basé sur les transactions")
            print(f"      - Définir un 'engagement_score' basé sur l'activité")
        
        if predictor_vars:
            print(f"   ✅ Variables prédictives disponibles")
            print(f"   📈 Features à utiliser dans le modèle")
        else:
            print(f"   ⚠️ Variables prédictives limitées")
            print(f"   💡 Utiliser toutes les variables numériques disponibles")
        
        # Prochaines étapes
        print(f"\n🔄 PROCHAINES ÉTAPES RECOMMANDÉES :")
        print(f"   1. Exécuter l'analyse statistique complète : python 4_analyse_statistique.py")
        print(f"   2. Créer des variables dérivées (RFM, engagement, etc.)")
        print(f"   3. Définir la variable cible (churn, LTV, satisfaction)")
        print(f"   4. Entraîner les modèles de machine learning")
        print(f"   5. Déployer le système de prédiction")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse : {e}")

if __name__ == "__main__":
    analyser_structure_csv()
    analyser_potentiel_fidelisation() 