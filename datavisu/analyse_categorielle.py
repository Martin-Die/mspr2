"""
analyse_categorielle.py
Analyses des variables catégorielles dans les données CSV.
Inclut distributions, associations, et tests de chi-carré.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
EXTRACTED_CSV_DIR = './extracted_csv'
RESULTS_DIR = './exploration_results'
CATEGORICAL_DIR = 'analyses_categorielles'

def create_categorical_directory():
    """Crée le dossier pour les analyses catégorielles."""
    os.makedirs(CATEGORICAL_DIR, exist_ok=True)

def detect_categorical_columns(df, max_unique_ratio=0.1):
    """Détecte les colonnes catégorielles."""
    categorical_columns = []
    
    for col in df.columns:
        # Colonnes de type object (string)
        if df[col].dtype == 'object':
            categorical_columns.append(col)
        # Colonnes numériques avec peu de valeurs uniques
        elif df[col].dtype in ['int64', 'float64']:
            unique_ratio = df[col].nunique() / len(df[col].dropna())
            if unique_ratio <= max_unique_ratio and df[col].nunique() <= 50:
                categorical_columns.append(col)
    
    return categorical_columns

def analyze_categorical_distribution(df, col, filename):
    """Analyse la distribution d'une variable catégorielle."""
    # Nettoyer les données
    clean_data = df[col].dropna()
    
    if len(clean_data) == 0:
        return None
    
    # Calculer les statistiques
    value_counts = clean_data.value_counts()
    value_counts_normalized = clean_data.value_counts(normalize=True)
    
    # Statistiques de base
    stats = {
        'total_values': len(clean_data),
        'unique_values': len(value_counts),
        'missing_values': df[col].isna().sum(),
        'missing_percentage': (df[col].isna().sum() / len(df)) * 100,
        'most_common': value_counts.index[0],
        'most_common_count': value_counts.iloc[0],
        'most_common_percentage': value_counts_normalized.iloc[0] * 100,
        'least_common': value_counts.index[-1],
        'least_common_count': value_counts.iloc[-1],
        'least_common_percentage': value_counts_normalized.iloc[-1] * 100
    }
    
    # Visualisation
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. Graphique en barres
    top_values = value_counts.head(10)  # Top 10 valeurs
    axes[0].bar(range(len(top_values)), top_values.values, color='skyblue')
    axes[0].set_title(f'Distribution de {col} (Top 10)')
    axes[0].set_xlabel('Valeurs')
    axes[0].set_ylabel('Fréquence')
    axes[0].set_xticks(range(len(top_values)))
    axes[0].set_xticklabels(top_values.index, rotation=45, ha='right')
    
    # 2. Graphique en camembert
    if len(value_counts) <= 10:
        axes[1].pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
        axes[1].set_title(f'Répartition de {col}')
    else:
        # Grouper les valeurs moins fréquentes
        top_5 = value_counts.head(5)
        others = value_counts.iloc[5:].sum()
        pie_data = pd.concat([top_5, pd.Series([others], index=['Autres'])])
        axes[1].pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%')
        axes[1].set_title(f'Répartition de {col} (Top 5 + Autres)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(CATEGORICAL_DIR, f'{filename}_{col}_distribution.png'), dpi=300)
    plt.close()
    
    return {
        'stats': stats,
        'value_counts': value_counts,
        'value_counts_normalized': value_counts_normalized
    }

def analyze_categorical_associations(df, cat_columns, filename):
    """Analyse les associations entre variables catégorielles."""
    if len(cat_columns) < 2:
        return None
    
    associations = {}
    
    # Matrice de contingence et tests de chi-carré
    for i, col1 in enumerate(cat_columns):
        for j, col2 in enumerate(cat_columns[i+1:], i+1):
            # Créer la table de contingence
            contingency_table = pd.crosstab(df[col1], df[col2])
            
            # Test de chi-carré
            try:
                chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                
                # Coefficient de contingence de Cramér
                n = contingency_table.sum().sum()
                cramer_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
                
                associations[f"{col1}_vs_{col2}"] = {
                    'contingency_table': contingency_table,
                    'chi2_statistic': chi2,
                    'p_value': p_value,
                    'degrees_of_freedom': dof,
                    'cramer_v': cramer_v,
                    'significant': p_value < 0.05,
                    'strength': 'forte' if cramer_v > 0.3 else 'modérée' if cramer_v > 0.1 else 'faible'
                }
            except Exception as e:
                print(f"Erreur lors du test chi-carré pour {col1} vs {col2}: {e}")
    
    # Visualisation des associations
    if associations:
        n_associations = len(associations)
        n_cols = min(3, n_associations)
        n_rows = (n_associations + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
        if n_rows == 1:
            axes = [axes] if n_cols == 1 else axes
        else:
            axes = axes.flatten()
        
        for idx, (assoc_name, assoc_data) in enumerate(associations.items()):
            if idx < len(axes):
                # Heatmap de la table de contingence
                sns.heatmap(assoc_data['contingency_table'], 
                           annot=True, fmt='d', cmap='Blues', ax=axes[idx])
                axes[idx].set_title(f'{assoc_name}\nχ²={assoc_data["chi2_statistic"]:.2f}, p={assoc_data["p_value"]:.4f}')
        
        # Masquer les axes vides
        for idx in range(n_associations, len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(os.path.join(CATEGORICAL_DIR, f'{filename}_associations.png'), dpi=300)
        plt.close()
    
    return associations

def analyze_categorical_numerical_relationships(df, cat_columns, num_columns, filename):
    """Analyse les relations entre variables catégorielles et numériques."""
    if len(cat_columns) == 0 or len(num_columns) == 0:
        return None
    
    relationships = {}
    
    for cat_col in cat_columns:
        for num_col in num_columns:
            # Statistiques par catégorie
            grouped_stats = df.groupby(cat_col)[num_col].agg(['count', 'mean', 'std', 'min', 'max']).reset_index()
            
            # Test ANOVA (si plus de 2 catégories)
            categories = df[cat_col].dropna().unique()
            if len(categories) >= 2:
                try:
                    from scipy.stats import f_oneway
                    groups = [df[df[cat_col] == cat][num_col].dropna() for cat in categories]
                    f_stat, p_value = f_oneway(*groups)
                    
                    relationships[f"{cat_col}_vs_{num_col}"] = {
                        'grouped_stats': grouped_stats,
                        'f_statistic': f_stat,
                        'p_value': p_value,
                        'significant': p_value < 0.05,
                        'n_categories': len(categories)
                    }
                except Exception as e:
                    print(f"Erreur lors du test ANOVA pour {cat_col} vs {num_col}: {e}")
    
    # Visualisations
    if relationships:
        n_relationships = len(relationships)
        n_cols = min(2, n_relationships)
        n_rows = (n_relationships + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(8*n_cols, 6*n_rows))
        if n_rows == 1:
            axes = [axes] if n_cols == 1 else axes
        else:
            axes = axes.flatten()
        
        for idx, (rel_name, rel_data) in enumerate(relationships.items()):
            if idx < len(axes):
                # Box plot
                cat_col, num_col = rel_name.split('_vs_')
                df_clean = df[[cat_col, num_col]].dropna()
                
                # Limiter le nombre de catégories pour la lisibilité
                if len(df_clean[cat_col].unique()) > 10:
                    top_categories = df_clean[cat_col].value_counts().head(10).index
                    df_clean = df_clean[df_clean[cat_col].isin(top_categories)]
                
                sns.boxplot(data=df_clean, x=cat_col, y=num_col, ax=axes[idx])
                axes[idx].set_title(f'{rel_name}\nF={rel_data["f_statistic"]:.2f}, p={rel_data["p_value"]:.4f}')
                axes[idx].tick_params(axis='x', rotation=45)
        
        # Masquer les axes vides
        for idx in range(n_relationships, len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(os.path.join(CATEGORICAL_DIR, f'{filename}_cat_num_relationships.png'), dpi=300)
        plt.close()
    
    return relationships

def generate_categorical_report(df, filename):
    """Génère un rapport complet d'analyse catégorielle."""
    print(f"📊 Analyse catégorielle de {filename}...")
    
    # Détecter les colonnes catégorielles
    categorical_columns = detect_categorical_columns(df)
    
    if not categorical_columns:
        print(f"  ⚠️ Aucune variable catégorielle détectée dans {filename}")
        return False
    
    print(f"  📋 Variables catégorielles détectées : {len(categorical_columns)}")
    
    # Colonnes numériques pour les relations
    numerical_columns = df.select_dtypes(include=[np.number]).columns
    
    # Analyses
    distributions = {}
    associations = None
    relationships = None
    
    # Distributions individuelles
    for col in categorical_columns:
        distributions[col] = analyze_categorical_distribution(df, col, filename)
    
    # Associations entre variables catégorielles
    if len(categorical_columns) >= 2:
        associations = analyze_categorical_associations(df, categorical_columns, filename)
    
    # Relations avec variables numériques
    if len(numerical_columns) > 0:
        relationships = analyze_categorical_numerical_relationships(df, categorical_columns, numerical_columns, filename)
    
    # Générer le rapport texte
    report_path = os.path.join(CATEGORICAL_DIR, f'{filename}_categorical_report.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"RAPPORT D'ANALYSE CATÉGORIELLE - {filename}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"📊 INFORMATIONS GÉNÉRALES\n")
        f.write(f"Nombre de variables catégorielles : {len(categorical_columns)}\n")
        f.write(f"Variables catégorielles : {', '.join(categorical_columns)}\n\n")
        
        # Distributions
        f.write(f"📈 DISTRIBUTIONS INDIVIDUELLES\n")
        for col, dist_data in distributions.items():
            if dist_data:
                stats = dist_data['stats']
                f.write(f"\n{col}:\n")
                f.write(f"  - Total de valeurs : {stats['total_values']}\n")
                f.write(f"  - Valeurs uniques : {stats['unique_values']}\n")
                f.write(f"  - Valeurs manquantes : {stats['missing_values']} ({stats['missing_percentage']:.1f}%)\n")
                f.write(f"  - Valeur la plus fréquente : {stats['most_common']} ({stats['most_common_count']} fois, {stats['most_common_percentage']:.1f}%)\n")
                f.write(f"  - Valeur la moins fréquente : {stats['least_common']} ({stats['least_common_count']} fois, {stats['least_common_percentage']:.1f}%)\n")
                
                # Top 5 valeurs
                top_5 = dist_data['value_counts'].head(5)
                f.write(f"  - Top 5 valeurs :\n")
                for val, count in top_5.items():
                    percentage = (count / stats['total_values']) * 100
                    f.write(f"    * {val}: {count} ({percentage:.1f}%)\n")
        
        # Associations
        if associations:
            f.write(f"\n🔗 ASSOCIATIONS ENTRE VARIABLES CATÉGORIELLES\n")
            for assoc_name, assoc_data in associations.items():
                f.write(f"\n{assoc_name}:\n")
                f.write(f"  - Test de chi-carré : χ² = {assoc_data['chi2_statistic']:.4f}\n")
                f.write(f"  - P-valeur : {assoc_data['p_value']:.4f}\n")
                f.write(f"  - Significatif : {'Oui' if assoc_data['significant'] else 'Non'}\n")
                f.write(f"  - Coefficient de Cramér : {assoc_data['cramer_v']:.4f}\n")
                f.write(f"  - Force de l'association : {assoc_data['strength']}\n")
        
        # Relations avec variables numériques
        if relationships:
            f.write(f"\n📊 RELATIONS AVEC VARIABLES NUMÉRIQUES\n")
            for rel_name, rel_data in relationships.items():
                f.write(f"\n{rel_name}:\n")
                f.write(f"  - Test ANOVA : F = {rel_data['f_statistic']:.4f}\n")
                f.write(f"  - P-valeur : {rel_data['p_value']:.4f}\n")
                f.write(f"  - Significatif : {'Oui' if rel_data['significant'] else 'Non'}\n")
                f.write(f"  - Nombre de catégories : {rel_data['n_categories']}\n")
                
                # Statistiques par groupe
                f.write(f"  - Statistiques par catégorie :\n")
                for _, row in rel_data['grouped_stats'].iterrows():
                    f.write(f"    * {row.iloc[0]}: n={row['count']}, moy={row['mean']:.2f}, std={row['std']:.2f}\n")
        
        f.write(f"\n📁 FICHIERS GÉNÉRÉS :\n")
        f.write(f"  - Distributions : {filename}_*_distribution.png\n")
        if associations:
            f.write(f"  - Associations : {filename}_associations.png\n")
        if relationships:
            f.write(f"  - Relations : {filename}_cat_num_relationships.png\n")
        f.write(f"  - Rapport : {filename}_categorical_report.txt\n")
    
    print(f"✅ Rapport catégoriel généré : {report_path}")
    return True

def main():
    """Fonction principale pour les analyses catégorielles."""
    print("📊 Début des analyses catégorielles...")
    
    # Créer le dossier de résultats
    create_categorical_directory()
    
    # Lister les fichiers CSV
    extracted_dir = Path(EXTRACTED_CSV_DIR)
    if not extracted_dir.exists():
        print(f"❌ Le dossier {EXTRACTED_CSV_DIR} n'existe pas.")
        print("💡 Veuillez d'abord exécuter extract.py pour extraire les fichiers compressés.")
        print("   Commande : python ../etl_steps/extract.py")
        return
    
    csv_files = list(extracted_dir.rglob("*.csv"))
    
    if not csv_files:
        print("❌ Aucun fichier CSV trouvé.")
        print("💡 Veuillez d'abord exécuter extract.py pour extraire les fichiers compressés.")
        print("   Commande : python ../etl_steps/extract.py")
        return
    
    print(f"📁 {len(csv_files)} fichier(s) CSV trouvé(s)")
    
    # Analyser chaque fichier
    successful_analyses = 0
    for csv_path in csv_files:
        try:
            # Charger un échantillon
            df = pd.read_csv(csv_path, nrows=10000)
            filename = os.path.splitext(os.path.basename(csv_path))[0]
            
            if generate_categorical_report(df, filename):
                successful_analyses += 1
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse de {csv_path}: {e}")
    
    print(f"\n✅ Analyses catégorielles terminées !")
    print(f"   - Fichiers analysés : {successful_analyses}/{len(csv_files)}")
    print(f"   - Résultats dans : {CATEGORICAL_DIR}")

if __name__ == "__main__":
    main() 