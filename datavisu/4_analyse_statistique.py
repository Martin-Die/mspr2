"""
analyse_statistique.py
Analyses statistiques orientées fidélisation client.
Identifie les variables importantes pour un modèle IA de fidélisation.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
EXTRACTED_CSV_DIR = './extracted_csv'
RESULTS_DIR = './exploration_results'
STATS_DIR = 'analyses_statistiques'

# Variables cibles potentielles pour la fidélisation
POTENTIAL_TARGET_VARIABLES = [
    'churn', 'retention', 'loyalty', 'satisfaction', 'score', 'rating',
    'fidelity', 'engagement', 'activity', 'frequency', 'recency',
    'monetary', 'value', 'status', 'tier', 'level', 'premium',
    'active', 'inactive', 'canceled', 'suspended', 'vip', 'gold',
    'silver', 'bronze', 'platinum', 'diamond', 'elite'
]

# Variables prédictives importantes pour la fidélisation
IMPORTANT_PREDICTORS = [
    'age', 'income', 'spending', 'purchase', 'order', 'transaction',
    'frequency', 'recency', 'monetary', 'total', 'amount', 'value',
    'duration', 'tenure', 'membership', 'subscription', 'plan',
    'category', 'product', 'service', 'location', 'region', 'city',
    'country', 'gender', 'education', 'occupation', 'marital',
    'children', 'household', 'credit', 'score', 'rating', 'review',
    'complaint', 'support', 'interaction', 'contact', 'email',
    'phone', 'mobile', 'web', 'app', 'online', 'offline'
]

def create_stats_directory():
    """Crée le dossier pour les analyses statistiques."""
    os.makedirs(STATS_DIR, exist_ok=True)

def load_data_sample(csv_path, sample_size=10000):
    """Charge un échantillon de données."""
    try:
        df = pd.read_csv(csv_path, nrows=sample_size)
        return df
    except Exception as e:
        print(f"Erreur lors du chargement de {csv_path}: {e}")
        return None

def identify_target_variables(df):
    """Identifie les variables cibles potentielles pour la fidélisation."""
    target_vars = []
    
    for col in df.columns:
        col_lower = col.lower()
        for target in POTENTIAL_TARGET_VARIABLES:
            if target in col_lower:
                target_vars.append(col)
                break
    
    return target_vars

def identify_predictor_variables(df):
    """Identifie les variables prédictives importantes pour la fidélisation."""
    predictor_vars = []
    
    for col in df.columns:
        col_lower = col.lower()
        for predictor in IMPORTANT_PREDICTORS:
            if predictor in col_lower:
                predictor_vars.append(col)
                break
    
    return predictor_vars

def analyze_correlations_for_fidelity(df, filename):
    """Analyse les corrélations orientées fidélisation client."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    target_vars = identify_target_variables(df)
    predictor_vars = identify_predictor_variables(df)
    
    if len(numeric_cols) < 2:
        return None
    
    # Matrice de corrélation
    corr_matrix = df[numeric_cols].corr()
    
    # Corrélations avec les variables cibles
    target_correlations = []
    if target_vars:
        for target in target_vars:
            if target in numeric_cols:
                for pred in numeric_cols:
                    if pred != target:
                        corr_val = corr_matrix.loc[target, pred]
                        if abs(corr_val) > 0.3:  # Seuil plus bas pour la fidélisation
                            target_correlations.append({
                                'target': target,
                                'predictor': pred,
                                'correlation': corr_val,
                                'strength': 'forte' if abs(corr_val) > 0.7 else 'modérée' if abs(corr_val) > 0.5 else 'faible'
                            })
    
    # Visualisation orientée fidélisation
    plt.figure(figsize=(14, 12))
    
    # Heatmap avec focus sur les variables importantes
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
    plt.title(f'Matrice de Corrélation - {filename}\n(Variables importantes pour la fidélisation)')
    
    # Mettre en évidence les variables cibles et prédictives
    if target_vars:
        plt.text(0.02, 0.98, f'Variables cibles: {", ".join(target_vars)}', 
                transform=plt.gca().transAxes, fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    if predictor_vars:
        plt.text(0.02, 0.95, f'Variables prédictives: {", ".join(predictor_vars[:5])}...', 
                transform=plt.gca().transAxes, fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(os.path.join(STATS_DIR, f'{filename}_fidelity_correlation_heatmap.png'), dpi=300)
    plt.close()
    
    return {
        'correlation_matrix': corr_matrix,
        'target_correlations': target_correlations,
        'target_variables': target_vars,
        'predictor_variables': predictor_vars
    }

def analyze_customer_segments(df, filename):
    """Analyse les segments de clients pour la fidélisation."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    target_vars = identify_target_variables(df)
    predictor_vars = identify_predictor_variables(df)
    
    if len(numeric_cols) == 0:
        return None
    
    # Focus sur les variables importantes pour la fidélisation
    important_cols = []
    for col in numeric_cols:
        if col in target_vars or col in predictor_vars:
            important_cols.append(col)
    
    if not important_cols:
        important_cols = numeric_cols[:5]  # Prendre les 5 premières si aucune variable importante
    
    # Analyse des segments
    segments_analysis = {}
    
    for col in important_cols:
        data = df[col].dropna()
        if len(data) > 0:
            # Segmentation en quartiles
            quartiles = data.quantile([0.25, 0.5, 0.75])
            
            segments_analysis[col] = {
                'mean': data.mean(),
                'median': data.median(),
                'std': data.std(),
                'q1': quartiles[0.25],
                'q2': quartiles[0.5],
                'q3': quartiles[0.75],
                'segments': {
                    'low': data[data <= quartiles[0.25]].count(),
                    'medium_low': data[(data > quartiles[0.25]) & (data <= quartiles[0.5])].count(),
                    'medium_high': data[(data > quartiles[0.5]) & (data <= quartiles[0.75])].count(),
                    'high': data[data > quartiles[0.75]].count()
                }
            }
    
    # Visualisation des segments
    n_cols = min(3, len(important_cols))
    n_rows = (len(important_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    if n_rows == 1:
        axes = [axes] if n_cols == 1 else axes
    else:
        axes = axes.flatten()
    
    for i, col in enumerate(important_cols):
        if i < len(axes):
            data = df[col].dropna()
            
            # Box plot avec segments
            bp = axes[i].boxplot(data, patch_artist=True)
            bp['boxes'][0].set_facecolor('lightblue')
            bp['medians'][0].set_color('red')
            
            # Ajouter les quartiles
            q1, q2, q3 = data.quantile([0.25, 0.5, 0.75])
            axes[i].axhline(y=q1, color='orange', linestyle='--', alpha=0.7, label='Q1')
            axes[i].axhline(y=q3, color='orange', linestyle='--', alpha=0.7, label='Q3')
            
            axes[i].set_title(f'Segmentation de {col}\n(Important pour la fidélisation)')
            axes[i].set_ylabel(col)
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
    
    # Masquer les axes vides
    for i in range(len(important_cols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(STATS_DIR, f'{filename}_customer_segments.png'), dpi=300)
    plt.close()
    
    return segments_analysis

def analyze_fidelity_features(df, filename):
    """Analyse les features importantes pour la fidélisation client."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    target_vars = identify_target_variables(df)
    predictor_vars = identify_predictor_variables(df)
    
    if len(numeric_cols) == 0:
        return None
    
    # Focus sur les variables importantes
    important_cols = []
    for col in numeric_cols:
        if col in target_vars or col in predictor_vars:
            important_cols.append(col)
    
    if not important_cols:
        important_cols = numeric_cols[:5]  # Prendre les 5 premières
    
    # Analyse des features
    feature_analysis = {}
    
    for col in important_cols:
        data = df[col].dropna()
        if len(data) > 0:
            # Statistiques descriptives
            feature_analysis[col] = {
                'mean': data.mean(),
                'median': data.median(),
                'std': data.std(),
                'min': data.min(),
                'max': data.max(),
                'skewness': data.skew(),
                'kurtosis': data.kurtosis(),
                'missing_pct': (df[col].isna().sum() / len(df)) * 100,
                'type': 'target' if col in target_vars else 'predictor'
            }
    
    # Visualisation des features importantes
    n_cols = min(3, len(important_cols))
    n_rows = (len(important_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    if n_rows == 1:
        axes = [axes] if n_cols == 1 else axes
    else:
        axes = axes.flatten()
    
    for i, col in enumerate(important_cols):
        if i < len(axes):
            data = df[col].dropna()
            
            # Histogramme avec courbe de densité
            axes[i].hist(data, bins=30, alpha=0.7, density=True, 
                        color='lightgreen' if col in target_vars else 'lightblue')
            
            # Courbe de densité
            from scipy.stats import gaussian_kde
            kde = gaussian_kde(data)
            x_range = np.linspace(data.min(), data.max(), 100)
            axes[i].plot(x_range, kde(x_range), 'r-', lw=2, label='Densité')
            
            # Ajouter les statistiques
            mean_val = data.mean()
            median_val = data.median()
            axes[i].axvline(mean_val, color='red', linestyle='--', alpha=0.7, label=f'Moyenne: {mean_val:.2f}')
            axes[i].axvline(median_val, color='orange', linestyle='--', alpha=0.7, label=f'Médiane: {median_val:.2f}')
            
            feature_type = 'Cible' if col in target_vars else 'Prédictive'
            axes[i].set_title(f'{col} ({feature_type})\n(Feature importante pour la fidélisation)')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Densité')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
    
    # Masquer les axes vides
    for i in range(len(important_cols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(STATS_DIR, f'{filename}_fidelity_features.png'), dpi=300)
    plt.close()
    
    return feature_analysis

def analyze_fidelity_importance(df, filename):
    """Analyse l'importance des variables pour la fidélisation client."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    target_vars = identify_target_variables(df)
    predictor_vars = identify_predictor_variables(df)
    
    if len(numeric_cols) < 2:
        return None
    
    importance_analysis = {}
    
    # Analyser l'importance des variables prédictives par rapport aux cibles
    if target_vars and predictor_vars:
        for target in target_vars:
            if target in numeric_cols:
                target_importance = {}
                for predictor in predictor_vars:
                    if predictor in numeric_cols and predictor != target:
                        # Corrélation de Spearman
                        data1 = df[target].dropna()
                        data2 = df[predictor].dropna()
                        
                        common_idx = data1.index.intersection(data2.index)
                        if len(common_idx) > 10:
                            data1_aligned = data1.loc[common_idx]
                            data2_aligned = data2.loc[common_idx]
                            
                            spearman_corr, spearman_p = stats.spearmanr(data1_aligned, data2_aligned)
                            
                            target_importance[predictor] = {
                                'spearman_correlation': spearman_corr,
                                'spearman_p_value': spearman_p,
                                'absolute_correlation': abs(spearman_corr),
                                'importance_score': abs(spearman_corr) * (1 - spearman_p) if spearman_p < 0.05 else 0
                            }
                
                importance_analysis[target] = target_importance
    
    # Visualisation de l'importance des variables
    if importance_analysis:
        plt.figure(figsize=(12, 8))
        
        # Créer un graphique d'importance
        all_importances = []
        all_predictors = []
        all_targets = []
        
        for target, predictors in importance_analysis.items():
            for predictor, stats in predictors.items():
                all_importances.append(stats['importance_score'])
                all_predictors.append(predictor)
                all_targets.append(target)
        
        if all_importances:
            # Trier par importance
            sorted_data = sorted(zip(all_importances, all_predictors, all_targets), reverse=True)
            importances, predictors, targets = zip(*sorted_data[:15])  # Top 15
            
            # Graphique en barres
            colors = ['red' if t in target_vars else 'blue' for t in targets]
            bars = plt.barh(range(len(importances)), importances, color=colors, alpha=0.7)
            
            plt.yticks(range(len(predictors)), predictors)
            plt.xlabel('Score d\'importance pour la fidélisation')
            plt.title(f'Importance des variables pour la fidélisation - {filename}')
            
            # Ajouter les valeurs sur les barres
            for i, (bar, imp) in enumerate(zip(bars, importances)):
                plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                        f'{imp:.3f}', ha='left', va='center')
            
            plt.tight_layout()
            plt.savefig(os.path.join(STATS_DIR, f'{filename}_fidelity_importance.png'), dpi=300)
            plt.close()
    
    return importance_analysis

def generate_fidelity_report(csv_path, filename):
    """Génère un rapport orienté fidélisation client."""
    print(f"📊 Analyse de fidélisation pour {filename}...")
    
    # Charger les données
    df = load_data_sample(csv_path)
    if df is None:
        return False
    
    # Identifier les variables importantes
    target_vars = identify_target_variables(df)
    predictor_vars = identify_predictor_variables(df)
    
    print(f"  🎯 Variables cibles identifiées : {len(target_vars)}")
    print(f"  📊 Variables prédictives identifiées : {len(predictor_vars)}")
    
    # Analyses orientées fidélisation
    correlations = analyze_correlations_for_fidelity(df, filename)
    segments = analyze_customer_segments(df, filename)
    features = analyze_fidelity_features(df, filename)
    importance = analyze_fidelity_importance(df, filename)
    
    # Générer le rapport
    report_path = os.path.join(STATS_DIR, f'{filename}_fidelity_report.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"RAPPORT DE FIDÉLISATION CLIENT - {filename}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"🎯 OBJECTIF : Identifier les variables importantes pour un modèle IA de fidélisation\n\n")
        
        f.write(f"📊 INFORMATIONS GÉNÉRALES\n")
        f.write(f"Nombre de lignes : {len(df)}\n")
        f.write(f"Nombre de colonnes : {len(df.columns)}\n")
        f.write(f"Colonnes numériques : {len(df.select_dtypes(include=[np.number]).columns)}\n\n")
        
        # Variables identifiées
        f.write(f"🔍 VARIABLES IDENTIFIÉES\n")
        f.write(f"Variables cibles potentielles :\n")
        if target_vars:
            for var in target_vars:
                f.write(f"  ✅ {var}\n")
        else:
            f.write(f"  ⚠️ Aucune variable cible identifiée\n")
        
        f.write(f"\nVariables prédictives importantes :\n")
        if predictor_vars:
            for var in predictor_vars[:10]:  # Top 10
                f.write(f"  📊 {var}\n")
            if len(predictor_vars) > 10:
                f.write(f"  ... et {len(predictor_vars) - 10} autres\n")
        else:
            f.write(f"  ⚠️ Aucune variable prédictive identifiée\n")
        f.write("\n")
        
        # Corrélations avec les cibles
        if correlations and correlations['target_correlations']:
            f.write(f"🔗 CORRÉLATIONS AVEC LES VARIABLES CIBLES\n")
            for corr in correlations['target_correlations']:
                f.write(f"{corr['target']} ← {corr['predictor']}:\n")
                f.write(f"  - Corrélation : {corr['correlation']:.3f}\n")
                f.write(f"  - Force : {corr['strength']}\n")
            f.write("\n")
        
        # Segments de clients
        if segments:
            f.write(f"👥 SEGMENTATION DES CLIENTS\n")
            for col, stats in segments.items():
                f.write(f"{col}:\n")
                f.write(f"  - Moyenne : {stats['mean']:.2f}\n")
                f.write(f"  - Médiane : {stats['median']:.2f}\n")
                f.write(f"  - Segments :\n")
                f.write(f"    * Faible : {stats['segments']['low']} clients\n")
                f.write(f"    * Moyen-faible : {stats['segments']['medium_low']} clients\n")
                f.write(f"    * Moyen-élevé : {stats['segments']['medium_high']} clients\n")
                f.write(f"    * Élevé : {stats['segments']['high']} clients\n")
            f.write("\n")
        
        # Features importantes
        if features:
            f.write(f"📈 FEATURES IMPORTANTES\n")
            for col, stats in features.items():
                feature_type = "Cible" if stats['type'] == 'target' else "Prédictive"
                f.write(f"{col} ({feature_type}):\n")
                f.write(f"  - Moyenne : {stats['mean']:.2f}\n")
                f.write(f"  - Médiane : {stats['median']:.2f}\n")
                f.write(f"  - Écart-type : {stats['std']:.2f}\n")
                f.write(f"  - Valeurs manquantes : {stats['missing_pct']:.1f}%\n")
            f.write("\n")
        
        # Importance des variables
        if importance:
            f.write(f"🏆 IMPORTANCE DES VARIABLES POUR LA FIDÉLISATION\n")
            for target, predictors in importance.items():
                f.write(f"Pour prédire {target}:\n")
                # Trier par importance
                sorted_predictors = sorted(predictors.items(), 
                                         key=lambda x: x[1]['importance_score'], reverse=True)
                for predictor, stats in sorted_predictors[:5]:  # Top 5
                    f.write(f"  - {predictor} : Score = {stats['importance_score']:.3f}\n")
            f.write("\n")
        
        # Recommandations pour le modèle IA
        f.write(f"🤖 RECOMMANDATIONS POUR LE MODÈLE IA\n")
        f.write(f"1. Variables cibles à utiliser :\n")
        if target_vars:
            for var in target_vars:
                f.write(f"   ✅ {var}\n")
        else:
            f.write(f"   ⚠️ Créer une variable cible (ex: churn, satisfaction, retention)\n")
        
        f.write(f"\n2. Variables prédictives prioritaires :\n")
        if predictor_vars:
            for var in predictor_vars[:10]:
                f.write(f"   📊 {var}\n")
        else:
            f.write(f"   ⚠️ Utiliser toutes les variables numériques disponibles\n")
        
        f.write(f"\n3. Type de modèle recommandé :\n")
        if target_vars:
            f.write(f"   🎯 Classification binaire ou multiclasse\n")
        else:
            f.write(f"   📈 Régression ou clustering\n")
        
        f.write(f"\n4. Prochaines étapes :\n")
        f.write(f"   🔄 Prétraitement des données (normalisation, encodage)\n")
        f.write(f"   🧪 Tests de différents algorithmes (Random Forest, XGBoost, etc.)\n")
        f.write(f"   📊 Validation croisée et métriques de performance\n")
        f.write(f"   🎯 Optimisation des hyperparamètres\n")
        
        f.write(f"\n📁 FICHIERS GÉNÉRÉS :\n")
        f.write(f"  - Corrélations : {filename}_fidelity_correlation_heatmap.png\n")
        f.write(f"  - Segments : {filename}_customer_segments.png\n")
        f.write(f"  - Features : {filename}_fidelity_features.png\n")
        f.write(f"  - Importance : {filename}_fidelity_importance.png\n")
        f.write(f"  - Rapport : {filename}_fidelity_report.txt\n")
    
    print(f"✅ Rapport de fidélisation généré : {report_path}")
    return True

def main():
    """Fonction principale pour les analyses de fidélisation."""
    print("🎯 Début des analyses de fidélisation client...")
    
    # Créer le dossier de résultats
    create_stats_directory()
    
    # Lister les fichiers CSV
    extracted_dir = Path(EXTRACTED_CSV_DIR)
    if not extracted_dir.exists():
        print(f"❌ Le dossier {EXTRACTED_CSV_DIR} n'existe pas.")
        print("💡 Veuillez d'abord exécuter extract.py pour extraire les fichiers compressés.")
        print("   Commande : python ./etl_steps/extract.py")
        return
    
    csv_files = list(extracted_dir.rglob("*.csv"))
    
    if not csv_files:
        print("❌ Aucun fichier CSV trouvé.")
        print("💡 Veuillez d'abord exécuter extract.py pour extraire les fichiers compressés.")
        print("   Commande : python ./etl_steps/extract.py")
        return
    
    print(f"📁 {len(csv_files)} fichier(s) CSV trouvé(s)")
    
    # Analyser chaque fichier
    successful_analyses = 0
    for csv_path in csv_files:
        filename = os.path.splitext(os.path.basename(csv_path))[0]
        if generate_fidelity_report(str(csv_path), filename):
            successful_analyses += 1
    
    print(f"\n✅ Analyses de fidélisation terminées !")
    print(f"   - Fichiers analysés : {successful_analyses}/{len(csv_files)}")
    print(f"   - Résultats dans : {STATS_DIR}")
    print(f"   🎯 Objectif : Identifier les variables pour un modèle IA de fidélisation")

if __name__ == "__main__":
    main() 