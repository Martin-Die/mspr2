import os
import pandas as pd
from pathlib import Path

# Configuration des dossiers
EXTRACTED_CSV_DIR = 'extracted_csv'
RESULTS_DIR = 'exploration_results'
CHUNK_SIZE = 10000  # Nombre de lignes à lire pour l'échantillon

def create_results_directory():
    """Crée le dossier de résultats s'il n'existe pas."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

def list_extracted_csv_files():
    """Liste tous les fichiers CSV dans le dossier extracted_csv."""
    extracted_dir = Path(EXTRACTED_CSV_DIR)
    if not extracted_dir.exists():
        print(f"⚠️ Le dossier {EXTRACTED_CSV_DIR} n'existe pas.")
        print("Veuillez d'abord exécuter extract.py pour extraire les fichiers compressés.")
        return []
    
    csv_files = []
    for file in extracted_dir.rglob("*.csv"):
        csv_files.append(str(file))
    
    return csv_files

def analyze_csv_file(csv_path, txt_path):
    """Analyse un fichier CSV et génère un rapport d'exploration."""
    filename = os.path.basename(csv_path)
    print(f"📊 Analyse de {filename}...")
    
    try:
        # Lecture d'un échantillon
        df = pd.read_csv(csv_path, nrows=CHUNK_SIZE)
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"Exploration du fichier : {filename}\n")
            f.write(f"Chemin complet : {csv_path}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"📈 INFORMATIONS GÉNÉRALES\n")
            f.write(f"Nombre de lignes chargées (échantillon) : {len(df)}\n")
            f.write(f"Nombre de colonnes : {len(df.columns)}\n")
            f.write(f"Taille mémoire de l'échantillon : {df.memory_usage(deep=True).sum() / 1024:.2f} KB\n\n")
            
            f.write(f"📋 STRUCTURE DES DONNÉES\n")
            f.write("Types de données par colonne :\n")
            f.write(str(df.dtypes))
            f.write("\n\n")
            
            f.write("Colonnes :\n")
            for i, col in enumerate(df.columns, 1):
                f.write(f"  {i:2d}. {col}\n")
            f.write("\n")
            
            f.write(f"🔍 QUALITÉ DES DONNÉES\n")
            f.write("Valeurs manquantes par colonne :\n")
            missing_data = df.isnull().sum()
            missing_percent = (missing_data / len(df)) * 100
            for col in df.columns:
                f.write(f"  {col}: {missing_data[col]} ({missing_percent[col]:.2f}%)\n")
            f.write("\n")
            
            f.write(f"📊 STATISTIQUES DESCRIPTIVES\n")
            # Statistiques pour les colonnes numériques
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                f.write("Statistiques descriptives (colonnes numériques) :\n")
                f.write(str(df[numeric_cols].describe()))
                f.write("\n\n")
            else:
                f.write("Aucune colonne numérique trouvée.\n\n")
            
            f.write(f"🎯 EXEMPLES DE VALEURS\n")
            f.write("Exemples de valeurs uniques par colonne :\n")
            for col in df.columns:
                uniques = df[col].dropna().unique()
                f.write(f"\n{col}:\n")
                if len(uniques) <= 10:
                    f.write(f"  {list(uniques)}\n")
                else:
                    f.write(f"  {list(uniques[:10])} ... (et {len(uniques) - 10} autres)\n")
                f.write(f"  Nombre de valeurs uniques : {len(uniques)}\n")
            
            f.write(f"\n📋 APERÇU DES DONNÉES\n")
            f.write("Premières lignes :\n")
            f.write(str(df.head()))
            f.write("\n\n")
            
            f.write("Dernières lignes :\n")
            f.write(str(df.tail()))
            f.write("\n\n")
            
            # Informations supplémentaires
            f.write(f"🔧 INFORMATIONS TECHNIQUES\n")
            f.write(f"Encodage détecté : UTF-8\n")
            f.write(f"Séparateur : virgule (,)\n")
            f.write(f"Taille du fichier original : {os.path.getsize(csv_path) / (1024*1024):.2f} MB\n")
        
        print(f"✅ Rapport généré : {txt_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse de {filename} : {e}")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"Erreur lors de l'analyse du fichier {filename} :\n")
            f.write(f"{str(e)}\n")
        return False

def generate_summary_report(csv_files, results_dir):
    """Génère un rapport de synthèse de l'exploration."""
    summary_path = os.path.join(results_dir, "00_summary_exploration.txt")
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("RAPPORT DE SYNTHÈSE - EXPLORATION DES DONNÉES\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"📁 Dossier source : {EXTRACTED_CSV_DIR}\n")
        f.write(f"📁 Dossier résultats : {RESULTS_DIR}\n")
        f.write(f"📊 Nombre de fichiers CSV analysés : {len(csv_files)}\n\n")
        
        f.write("📋 LISTE DES FICHIERS ANALYSÉS :\n")
        for i, csv_file in enumerate(csv_files, 1):
            file_size = os.path.getsize(csv_file) / (1024 * 1024)  # Taille en MB
            f.write(f"  {i:2d}. {os.path.basename(csv_file)} ({file_size:.2f} MB)\n")
        
        f.write(f"\n📈 RÉSUMÉ DE L'EXPLORATION :\n")
        f.write(f"  - Échantillon analysé par fichier : {CHUNK_SIZE} lignes\n")
        f.write(f"  - Rapports générés : {len(csv_files)} fichiers .txt\n")
        f.write(f"  - Rapport de synthèse : 00_summary_exploration.txt\n")
    
    print(f"📋 Rapport de synthèse généré : {summary_path}")

def main():
    """Fonction principale pour l'exploration des données."""
    print("🔍 Début de l'exploration des données CSV...")
    
    # Créer le dossier de résultats
    create_results_directory()
    
    # Lister les fichiers CSV extraits
    csv_files = list_extracted_csv_files()
    
    if not csv_files:
        print("❌ Aucun fichier CSV trouvé dans le dossier extracted_csv.")
        print("💡 Conseil : Exécutez d'abord extract.py pour extraire les fichiers compressés.")
        return
    
    print(f"📁 {len(csv_files)} fichier(s) CSV trouvé(s) dans {EXTRACTED_CSV_DIR}")
    
    # Analyser chaque fichier CSV
    successful_analyses = 0
    for csv_path in csv_files:
        filename = os.path.basename(csv_path)
        txt_name = os.path.splitext(filename)[0] + '_exploration.txt'
        txt_path = os.path.join(RESULTS_DIR, txt_name)
        
        if analyze_csv_file(csv_path, txt_path):
            successful_analyses += 1
    
    # Générer le rapport de synthèse
    generate_summary_report(csv_files, RESULTS_DIR)
    
    print(f"\n✅ Exploration terminée !")
    print(f"   - Fichiers analysés avec succès : {successful_analyses}/{len(csv_files)}")
    print(f"   - Rapports disponibles dans : {RESULTS_DIR}")

if __name__ == "__main__":
    main() 