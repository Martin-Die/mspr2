"""
analyse_complete.py
Script principal pour l'analyse complète des données CSV.
Orchestre toutes les analyses et génère un rapport de synthèse.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
EXTRACTED_CSV_DIR = '../extracted_csv'
RESULTS_DIR = '../exploration_results'
COMPLETE_DIR = 'analyse_complete'

def create_complete_directory():
    """Crée le dossier pour l'analyse complète."""
    os.makedirs(COMPLETE_DIR, exist_ok=True)

def load_and_summarize_data(csv_path):
    """Charge et résume les données d'un fichier CSV."""
    try:
        # Charger un échantillon pour l'analyse
        df = pd.read_csv(csv_path, nrows=10000)
        
        # Informations de base
        summary = {
            'file_path': str(csv_path),
            'file_name': os.path.basename(csv_path),
            'file_size_mb': os.path.getsize(csv_path) / (1024 * 1024),
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
            'missing_data_percentage': (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        }
        
        # Types de données
        dtype_counts = df.dtypes.value_counts()
        summary['data_types'] = dtype_counts.to_dict()
        
        # Colonnes par type
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        datetime_cols = []
        
        # Détecter les colonnes de dates
        for col in df.columns:
            try:
                pd.to_datetime(df[col].head(100), errors='raise')
                datetime_cols.append(col)
            except:
                pass
        
        summary['numeric_columns'] = numeric_cols
        summary['categorical_columns'] = categorical_cols
        summary['datetime_columns'] = datetime_cols
        
        # Statistiques descriptives pour les variables numériques
        if numeric_cols:
            numeric_stats = df[numeric_cols].describe()
            summary['numeric_statistics'] = numeric_stats.to_dict()
        
        return df, summary
        
    except Exception as e:
        print(f"Erreur lors du chargement de {csv_path}: {e}")
        return None, None

def create_overview_visualizations(df, filename):
    """Crée des visualisations d'aperçu général."""
    # 1. Heatmap des valeurs manquantes
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap='viridis')
    plt.title(f'Valeurs manquantes - {filename}')
    plt.tight_layout()
    plt.savefig(os.path.join(COMPLETE_DIR, f'{filename}_missing_values.png'), dpi=300)
    plt.close()
    
    # 2. Distribution des types de données
    dtype_counts = df.dtypes.value_counts()
    plt.figure(figsize=(10, 6))
    plt.pie(dtype_counts.values, labels=dtype_counts.index, autopct='%1.1f%%')
    plt.title(f'Répartition des types de données - {filename}')
    plt.savefig(os.path.join(COMPLETE_DIR, f'{filename}_data_types.png'), dpi=300)
    plt.close()
    
    # 3. Corrélation des variables numériques (si applicable)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, square=True, fmt='.2f')
        plt.title(f'Matrice de corrélation - {filename}')
        plt.tight_layout()
        plt.savefig(os.path.join(COMPLETE_DIR, f'{filename}_correlation_matrix.png'), dpi=300)
        plt.close()

def generate_comprehensive_report(all_summaries, filename):
    """Génère un rapport complet d'analyse."""
    report_path = os.path.join(COMPLETE_DIR, f'{filename}_comprehensive_report.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"RAPPORT D'ANALYSE COMPLÈTE - {filename}\n")
        f.write("=" * 60 + "\n\n")
        
        # Informations générales
        f.write(f"📊 INFORMATIONS GÉNÉRALES\n")
        f.write(f"Fichier analysé : {all_summaries['file_name']}\n")
        f.write(f"Taille du fichier : {all_summaries['file_size_mb']:.2f} MB\n")
        f.write(f"Nombre de lignes analysées : {all_summaries['total_rows']:,}\n")
        f.write(f"Nombre de colonnes : {all_summaries['total_columns']}\n")
        f.write(f"Utilisation mémoire : {all_summaries['memory_usage_mb']:.2f} MB\n")
        f.write(f"Pourcentage de données manquantes : {all_summaries['missing_data_percentage']:.2f}%\n\n")
        
        # Types de données
        f.write(f"📋 TYPES DE DONNÉES\n")
        for dtype, count in all_summaries['data_types'].items():
            f.write(f"  - {dtype}: {count} colonne(s)\n")
        f.write("\n")
        
        # Répartition des colonnes
        f.write(f"🔍 RÉPARTITION DES COLONNES\n")
        f.write(f"  - Variables numériques : {len(all_summaries['numeric_columns'])}\n")
        f.write(f"  - Variables catégorielles : {len(all_summaries['categorical_columns'])}\n")
        f.write(f"  - Variables temporelles : {len(all_summaries['datetime_columns'])}\n\n")
        
        # Variables numériques
        if all_summaries['numeric_columns']:
            f.write(f"📈 VARIABLES NUMÉRIQUES\n")
            f.write(f"Colonnes : {', '.join(all_summaries['numeric_columns'])}\n\n")
            
            if 'numeric_statistics' in all_summaries:
                f.write(f"Statistiques descriptives :\n")
                stats = all_summaries['numeric_statistics']
                for col in all_summaries['numeric_columns']:
                    if col in stats:
                        f.write(f"  {col}:\n")
                        f.write(f"    - Moyenne : {stats[col].get('mean', 'N/A'):.2f}\n")
                        f.write(f"    - Médiane : {stats[col].get('50%', 'N/A'):.2f}\n")
                        f.write(f"    - Écart-type : {stats[col].get('std', 'N/A'):.2f}\n")
                        f.write(f"    - Min : {stats[col].get('min', 'N/A'):.2f}\n")
                        f.write(f"    - Max : {stats[col].get('max', 'N/A'):.2f}\n\n")
        
        # Variables catégorielles
        if all_summaries['categorical_columns']:
            f.write(f"📊 VARIABLES CATÉGORIELLES\n")
            f.write(f"Colonnes : {', '.join(all_summaries['categorical_columns'])}\n\n")
        
        # Variables temporelles
        if all_summaries['datetime_columns']:
            f.write(f"📅 VARIABLES TEMPORELLES\n")
            f.write(f"Colonnes : {', '.join(all_summaries['datetime_columns'])}\n\n")
        
        # Recommandations
        f.write(f"💡 RECOMMANDATIONS D'ANALYSE\n")
        
        if all_summaries['numeric_columns']:
            f.write(f"  ✅ Analyser les corrélations entre variables numériques\n")
            f.write(f"  ✅ Détecter les outliers dans les variables numériques\n")
            f.write(f"  ✅ Analyser les distributions des variables numériques\n")
        
        if all_summaries['categorical_columns']:
            f.write(f"  ✅ Analyser les distributions des variables catégorielles\n")
            f.write(f"  ✅ Effectuer des tests de chi-carré entre variables catégorielles\n")
        
        if all_summaries['datetime_columns'] and all_summaries['numeric_columns']:
            f.write(f"  ✅ Analyser les tendances temporelles\n")
            f.write(f"  ✅ Détecter la saisonnalité dans les données\n")
        
        if all_summaries['missing_data_percentage'] > 10:
            f.write(f"  ⚠️ Traiter les valeurs manquantes ({all_summaries['missing_data_percentage']:.1f}%)\n")
        
        f.write(f"\n📁 FICHIERS GÉNÉRÉS :\n")
        f.write(f"  - Valeurs manquantes : {filename}_missing_values.png\n")
        f.write(f"  - Types de données : {filename}_data_types.png\n")
        if all_summaries['numeric_columns']:
            f.write(f"  - Matrice de corrélation : {filename}_correlation_matrix.png\n")
        f.write(f"  - Rapport complet : {filename}_comprehensive_report.txt\n")
    
    print(f"✅ Rapport complet généré : {report_path}")

def run_complete_analysis(csv_path):
    """Exécute une analyse complète d'un fichier CSV."""
    filename = os.path.splitext(os.path.basename(csv_path))[0]
    print(f"🔍 Analyse complète de {filename}...")
    
    # Charger et résumer les données
    df, summary = load_and_summarize_data(csv_path)
    
    if df is None or summary is None:
        return False
    
    # Créer les visualisations d'aperçu
    create_overview_visualizations(df, filename)
    
    # Générer le rapport complet
    generate_comprehensive_report(summary, filename)
    
    return True

def generate_master_summary(all_files_summaries):
    """Génère un résumé maître de toutes les analyses."""
    master_path = os.path.join(COMPLETE_DIR, "00_master_summary.txt")
    
    with open(master_path, 'w', encoding='utf-8') as f:
        f.write("RÉSUMÉ MAÎTRE - ANALYSE COMPLÈTE DES DONNÉES\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"📊 SYNTHÈSE GÉNÉRALE\n")
        f.write(f"Nombre de fichiers analysés : {len(all_files_summaries)}\n")
        f.write(f"Date d'analyse : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        total_rows = sum(s['total_rows'] for s in all_files_summaries)
        total_columns = sum(s['total_columns'] for s in all_files_summaries)
        total_size = sum(s['file_size_mb'] for s in all_files_summaries)
        
        f.write(f"📈 STATISTIQUES GLOBALES\n")
        f.write(f"  - Total de lignes : {total_rows:,}\n")
        f.write(f"  - Total de colonnes : {total_columns}\n")
        f.write(f"  - Taille totale : {total_size:.2f} MB\n")
        f.write(f"  - Moyenne de lignes par fichier : {total_rows/len(all_files_summaries):.0f}\n")
        f.write(f"  - Moyenne de colonnes par fichier : {total_columns/len(all_files_summaries):.1f}\n\n")
        
        f.write(f"📋 DÉTAIL PAR FICHIER\n")
        for summary in all_files_summaries:
            f.write(f"\n{summary['file_name']}:\n")
            f.write(f"  - Taille : {summary['file_size_mb']:.2f} MB\n")
            f.write(f"  - Lignes : {summary['total_rows']:,}\n")
            f.write(f"  - Colonnes : {summary['total_columns']}\n")
            f.write(f"  - Numériques : {len(summary['numeric_columns'])}\n")
            f.write(f"  - Catégorielles : {len(summary['categorical_columns'])}\n")
            f.write(f"  - Temporelles : {len(summary['datetime_columns'])}\n")
            f.write(f"  - Données manquantes : {summary['missing_data_percentage']:.1f}%\n")
        
        f.write(f"\n🎯 RECOMMANDATIONS GLOBALES\n")
        f.write(f"  ✅ Exécuter analyse_statistique.py pour les corrélations et outliers\n")
        f.write(f"  ✅ Exécuter analyse_categorielle.py pour les variables catégorielles\n")
        f.write(f"  ✅ Exécuter analyse_temporelle.py pour les séries temporelles\n")
        f.write(f"  ✅ Consulter les rapports individuels pour chaque fichier\n")
    
    print(f"📋 Résumé maître généré : {master_path}")

def main():
    """Fonction principale pour l'analyse complète."""
    print("🚀 Début de l'analyse complète des données...")
    
    # Créer le dossier de résultats
    create_complete_directory()
    
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
    all_summaries = []
    successful_analyses = 0
    
    for csv_path in csv_files:
        try:
            # Charger et résumer les données
            df, summary = load_and_summarize_data(csv_path)
            
            if df is not None and summary is not None:
                filename = os.path.splitext(os.path.basename(csv_path))[0]
                
                # Créer les visualisations d'aperçu
                create_overview_visualizations(df, filename)
                
                # Générer le rapport complet
                generate_comprehensive_report(summary, filename)
                
                all_summaries.append(summary)
                successful_analyses += 1
                
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse de {csv_path}: {e}")
    
    # Générer le résumé maître
    if all_summaries:
        generate_master_summary(all_summaries)
    
    print(f"\n✅ Analyse complète terminée !")
    print(f"   - Fichiers analysés : {successful_analyses}/{len(csv_files)}")
    print(f"   - Résultats dans : {COMPLETE_DIR}")
    print(f"\n📋 Prochaines étapes recommandées :")
    print(f"   1. Consulter le résumé maître : {COMPLETE_DIR}/00_master_summary.txt")
    print(f"   2. Exécuter analyse_statistique.py pour les analyses avancées")
    print(f"   3. Exécuter analyse_categorielle.py pour les variables catégorielles")
    print(f"   4. Exécuter analyse_temporelle.py pour les séries temporelles")

if __name__ == "__main__":
    main() 