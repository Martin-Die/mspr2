"""
analyse_statistique.py
Analyses statistiques avancées des données CSV extraites.
Inclut corrélations, tests statistiques, distributions et outliers.
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
EXTRACTED_CSV_DIR = '../extracted_csv'
RESULTS_DIR = '../exploration_results'
STATS_DIR = 'analyses_statistiques'

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

def analyze_correlations(df, filename):
    """Analyse les corrélations entre variables numériques."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        return None
    
    # Matrice de corrélation
    corr_matrix = df[numeric_cols].corr()
    
    # Corrélations significatives (|r| > 0.5)
    significant_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.5:
                significant_corr.append({
                    'var1': corr_matrix.columns[i],
                    'var2': corr_matrix.columns[j],
                    'correlation': corr_val
                })
    
    # Visualisation
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.2f')
    plt.title(f'Matrice de Corrélation - {filename}')
    plt.tight_layout()
    plt.savefig(os.path.join(STATS_DIR, f'{filename}_correlation_heatmap.png'), dpi=300)
    plt.close()
    
    return {
        'correlation_matrix': corr_matrix,
        'significant_correlations': significant_corr
    }

def detect_outliers(df, filename):
    """Détecte les outliers dans les variables numériques."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers_info = {}
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        
        outliers_info[col] = {
            'count': len(outliers),
            'percentage': (len(outliers) / len(df)) * 100,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outliers_values': outliers[col].tolist()[:10]  # Premiers 10 outliers
        }
    
    return outliers_info

def analyze_distributions(df, filename):
    """Analyse les distributions des variables numériques."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        return None
    
    # Calcul des statistiques de distribution
    dist_stats = {}
    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) > 0:
            # Test de normalité
            stat, p_value = stats.normaltest(data)
            
            dist_stats[col] = {
                'mean': data.mean(),
                'median': data.median(),
                'std': data.std(),
                'skewness': data.skew(),
                'kurtosis': data.kurtosis(),
                'is_normal': p_value > 0.05,
                'normality_p_value': p_value
            }
    
    # Visualisation des distributions
    n_cols = min(3, len(numeric_cols))
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    if n_rows == 1:
        axes = [axes] if n_cols == 1 else axes
    else:
        axes = axes.flatten()
    
    for i, col in enumerate(numeric_cols):
        if i < len(axes):
            # Histogramme avec courbe de densité
            axes[i].hist(df[col].dropna(), bins=30, alpha=0.7, density=True, color='skyblue')
            
            # Courbe de densité normale théorique
            mu, sigma = df[col].mean(), df[col].std()
            x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
            axes[i].plot(x, stats.norm.pdf(x, mu, sigma), 'r-', lw=2, label='Normal')
            
            axes[i].set_title(f'Distribution de {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Densité')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
    
    # Masquer les axes vides
    for i in range(len(numeric_cols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(STATS_DIR, f'{filename}_distributions.png'), dpi=300)
    plt.close()
    
    return dist_stats

def perform_statistical_tests(df, filename):
    """Effectue des tests statistiques sur les données."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        return None
    
    tests_results = {}
    
    # Test de corrélation de Spearman pour toutes les paires
    for i, col1 in enumerate(numeric_cols):
        for j, col2 in enumerate(numeric_cols[i+1:], i+1):
            data1 = df[col1].dropna()
            data2 = df[col2].dropna()
            
            # Aligner les données
            common_idx = data1.index.intersection(data2.index)
            if len(common_idx) > 10:  # Au moins 10 observations communes
                data1_aligned = data1.loc[common_idx]
                data2_aligned = data2.loc[common_idx]
                
                # Corrélation de Spearman
                spearman_corr, spearman_p = stats.spearmanr(data1_aligned, data2_aligned)
                
                # Test de Mann-Whitney (si les distributions sont différentes)
                if len(data1_aligned) > 0 and len(data2_aligned) > 0:
                    try:
                        mw_stat, mw_p = stats.mannwhitneyu(data1_aligned, data2_aligned, alternative='two-sided')
                    except:
                        mw_stat, mw_p = np.nan, np.nan
                else:
                    mw_stat, mw_p = np.nan, np.nan
                
                test_name = f"{col1}_vs_{col2}"
                tests_results[test_name] = {
                    'spearman_correlation': spearman_corr,
                    'spearman_p_value': spearman_p,
                    'mann_whitney_statistic': mw_stat,
                    'mann_whitney_p_value': mw_p,
                    'sample_size': len(common_idx)
                }
    
    return tests_results

def generate_statistical_report(csv_path, filename):
    """Génère un rapport statistique complet pour un fichier CSV."""
    print(f"📊 Analyse statistique de {filename}...")
    
    # Charger les données
    df = load_data_sample(csv_path)
    if df is None:
        return False
    
    # Effectuer les analyses
    correlations = analyze_correlations(df, filename)
    outliers = detect_outliers(df, filename)
    distributions = analyze_distributions(df, filename)
    tests = perform_statistical_tests(df, filename)
    
    # Générer le rapport texte
    report_path = os.path.join(STATS_DIR, f'{filename}_statistical_report.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"RAPPORT STATISTIQUE - {filename}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"📈 INFORMATIONS GÉNÉRALES\n")
        f.write(f"Nombre de lignes analysées : {len(df)}\n")
        f.write(f"Nombre de colonnes : {len(df.columns)}\n")
        f.write(f"Colonnes numériques : {len(df.select_dtypes(include=[np.number]).columns)}\n\n")
        
        # Corrélations
        if correlations:
            f.write(f"🔗 ANALYSE DES CORRÉLATIONS\n")
            f.write(f"Matrice de corrélation générée : {filename}_correlation_heatmap.png\n")
            f.write(f"Corrélations significatives (|r| > 0.5) :\n")
            for corr in correlations['significant_correlations']:
                f.write(f"  {corr['var1']} ↔ {corr['var2']} : r = {corr['correlation']:.3f}\n")
            f.write("\n")
        
        # Outliers
        f.write(f"⚠️ DÉTECTION D'OUTLIERS\n")
        for col, info in outliers.items():
            f.write(f"{col}:\n")
            f.write(f"  - Nombre d'outliers : {info['count']} ({info['percentage']:.1f}%)\n")
            f.write(f"  - Bornes : [{info['lower_bound']:.3f}, {info['upper_bound']:.3f}]\n")
            if info['outliers_values']:
                f.write(f"  - Exemples d'outliers : {info['outliers_values'][:5]}\n")
            f.write("\n")
        
        # Distributions
        if distributions:
            f.write(f"📊 ANALYSE DES DISTRIBUTIONS\n")
            f.write(f"Graphiques générés : {filename}_distributions.png\n")
            for col, stats_info in distributions.items():
                f.write(f"{col}:\n")
                f.write(f"  - Moyenne : {stats_info['mean']:.3f}\n")
                f.write(f"  - Médiane : {stats_info['median']:.3f}\n")
                f.write(f"  - Écart-type : {stats_info['std']:.3f}\n")
                f.write(f"  - Asymétrie : {stats_info['skewness']:.3f}\n")
                f.write(f"  - Aplatissement : {stats_info['kurtosis']:.3f}\n")
                f.write(f"  - Distribution normale : {'Oui' if stats_info['is_normal'] else 'Non'}\n")
                f.write(f"  - P-valeur test normalité : {stats_info['normality_p_value']:.4f}\n\n")
        
        # Tests statistiques
        if tests:
            f.write(f"🧪 TESTS STATISTIQUES\n")
            for test_name, test_results in tests.items():
                f.write(f"{test_name}:\n")
                f.write(f"  - Corrélation de Spearman : r = {test_results['spearman_correlation']:.3f}\n")
                f.write(f"  - P-valeur Spearman : {test_results['spearman_p_value']:.4f}\n")
                if not np.isnan(test_results['mann_whitney_statistic']):
                    f.write(f"  - Statistique Mann-Whitney : {test_results['mann_whitney_statistic']:.3f}\n")
                    f.write(f"  - P-valeur Mann-Whitney : {test_results['mann_whitney_p_value']:.4f}\n")
                f.write(f"  - Taille échantillon : {test_results['sample_size']}\n\n")
    
    print(f"✅ Rapport statistique généré : {report_path}")
    return True

def main():
    """Fonction principale pour les analyses statistiques."""
    print("📊 Début des analyses statistiques...")
    
    # Créer le dossier de résultats
    create_stats_directory()
    
    # Lister les fichiers CSV
    extracted_dir = Path(EXTRACTED_CSV_DIR)
    if not extracted_dir.exists():
        print(f"❌ Le dossier {EXTRACTED_CSV_DIR} n'existe pas.")
        return
    
    csv_files = list(extracted_dir.rglob("*.csv"))
    
    if not csv_files:
        print("❌ Aucun fichier CSV trouvé.")
        return
    
    print(f"📁 {len(csv_files)} fichier(s) CSV trouvé(s)")
    
    # Analyser chaque fichier
    successful_analyses = 0
    for csv_path in csv_files:
        filename = os.path.splitext(os.path.basename(csv_path))[0]
        if generate_statistical_report(str(csv_path), filename):
            successful_analyses += 1
    
    print(f"\n✅ Analyses statistiques terminées !")
    print(f"   - Fichiers analysés : {successful_analyses}/{len(csv_files)}")
    print(f"   - Résultats dans : {STATS_DIR}")

if __name__ == "__main__":
    main() 