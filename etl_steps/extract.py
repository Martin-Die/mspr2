"""
extract.py
Étape 1 du pipeline ETL : Extraction des données brutes depuis les fichiers sources.
Optimisé pour les gros fichiers CSV et fichiers compressés (zip, gz, etc.).
"""
import os
import pandas as pd
import gzip
import zipfile
import tarfile
import shutil
from pathlib import Path
from typing import List, Iterator, Optional, Tuple

# Configuration des dossiers
EXTRACTED_CSV_DIR = "extracted_csv"
DATASETS_DIR = "datasets"

def create_extraction_directory() -> str:
    """Crée le dossier pour les CSV extraits s'il n'existe pas."""
    extracted_dir = Path(EXTRACTED_CSV_DIR)
    extracted_dir.mkdir(exist_ok=True)
    return str(extracted_dir)

def is_compressed_file(file_path: str) -> bool:
    """Vérifie si un fichier est compressé."""
    compressed_extensions = ['.gz', '.zip', '.tar', '.tar.gz', '.tgz', '.bz2']
    return any(file_path.lower().endswith(ext) for ext in compressed_extensions)

def extract_gzip_file(gzip_path: str, output_dir: str) -> List[str]:
    """Extrait un fichier .gz et retourne la liste des fichiers extraits."""
    extracted_files = []
    
    # Déterminer le nom du fichier de sortie
    base_name = os.path.basename(gzip_path)
    if base_name.endswith('.gz'):
        output_name = base_name[:-3]  # Enlever .gz
    else:
        output_name = base_name
    
    output_path = os.path.join(output_dir, output_name)
    
    try:
        with gzip.open(gzip_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        extracted_files.append(output_path)
        print(f"✓ Fichier extrait : {gzip_path} -> {output_path}")
    except Exception as e:
        print(f"✗ Erreur lors de l'extraction de {gzip_path} : {e}")
    
    return extracted_files

def extract_zip_file(zip_path: str, output_dir: str) -> List[str]:
    """Extrait un fichier .zip et retourne la liste des fichiers extraits."""
    extracted_files = []
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
            extracted_files = [os.path.join(output_dir, f) for f in zip_ref.namelist()]
        print(f"✓ Fichier ZIP extrait : {zip_path} -> {len(extracted_files)} fichiers")
    except Exception as e:
        print(f"✗ Erreur lors de l'extraction de {zip_path} : {e}")
    
    return extracted_files

def extract_tar_file(tar_path: str, output_dir: str) -> List[str]:
    """Extrait un fichier .tar et retourne la liste des fichiers extraits."""
    extracted_files = []
    
    try:
        with tarfile.open(tar_path, 'r:*') as tar_ref:
            tar_ref.extractall(output_dir)
            extracted_files = [os.path.join(output_dir, f) for f in tar_ref.getnames()]
        print(f"✓ Fichier TAR extrait : {tar_path} -> {len(extracted_files)} fichiers")
    except Exception as e:
        print(f"✗ Erreur lors de l'extraction de {tar_path} : {e}")
    
    return extracted_files

def extract_compressed_file(file_path: str, output_dir: str) -> List[str]:
    """Extrait un fichier compressé selon son type."""
    file_path_lower = file_path.lower()
    
    if file_path_lower.endswith('.gz'):
        return extract_gzip_file(file_path, output_dir)
    elif file_path_lower.endswith('.zip'):
        return extract_zip_file(file_path, output_dir)
    elif file_path_lower.endswith(('.tar', '.tar.gz', '.tgz')):
        return extract_tar_file(file_path, output_dir)
    else:
        print(f"✗ Type de compression non supporté pour : {file_path}")
        return []

def list_all_files(datasets_dir: str) -> List[str]:
    """Liste tous les fichiers dans le dossier datasets."""
    all_files = []
    for root, dirs, files in os.walk(datasets_dir):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def list_csv_files(datasets_dir: str) -> List[str]:
    """Liste les fichiers CSV dans le dossier datasets."""
    return [os.path.join(datasets_dir, f) for f in os.listdir(datasets_dir) if f.endswith('.csv')]

def list_extracted_csv_files() -> List[str]:
    """Liste les fichiers CSV extraits dans le dossier extracted_csv."""
    extracted_dir = Path(EXTRACTED_CSV_DIR)
    if not extracted_dir.exists():
        return []
    
    csv_files = []
    for file in extracted_dir.rglob("*.csv"):
        csv_files.append(str(file))
    return csv_files

def extract_all_compressed_files() -> List[str]:
    """
    Extrait tous les fichiers compressés du dossier datasets.
    Returns:
        Liste des chemins des fichiers CSV extraits.
    """
    print("🔍 Recherche de fichiers compressés...")
    
    # Créer le dossier d'extraction
    extracted_dir = create_extraction_directory()
    
    # Lister tous les fichiers dans datasets
    all_files = list_all_files(DATASETS_DIR)
    compressed_files = [f for f in all_files if is_compressed_file(f)]
    
    if not compressed_files:
        print("ℹ️ Aucun fichier compressé trouvé dans le dossier datasets.")
        return []
    
    print(f"📦 {len(compressed_files)} fichier(s) compressé(s) trouvé(s)")
    
    all_extracted_files = []
    
    for compressed_file in compressed_files:
        print(f"\n📂 Traitement de : {os.path.basename(compressed_file)}")
        extracted_files = extract_compressed_file(compressed_file, extracted_dir)
        all_extracted_files.extend(extracted_files)
    
    # Filtrer pour ne garder que les CSV
    csv_files = [f for f in all_extracted_files if f.endswith('.csv')]
    
    print(f"\n✅ Extraction terminée : {len(csv_files)} fichier(s) CSV extrait(s)")
    return csv_files

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

def get_extraction_summary() -> dict:
    """Retourne un résumé de l'extraction."""
    datasets_files = list_all_files(DATASETS_DIR)
    compressed_files = [f for f in datasets_files if is_compressed_file(f)]
    extracted_csv_files = list_extracted_csv_files()
    
    return {
        "datasets_total_files": len(datasets_files),
        "compressed_files": len(compressed_files),
        "extracted_csv_files": len(extracted_csv_files),
        "extracted_csv_paths": extracted_csv_files
    }

def main():
    """Fonction principale pour l'extraction."""
    print("🚀 Début de l'extraction des données...")
    
    # Extraire tous les fichiers compressés
    extracted_files = extract_all_compressed_files()
    
    # Afficher le résumé
    summary = get_extraction_summary()
    print(f"\n📊 Résumé de l'extraction :")
    print(f"   - Fichiers dans datasets : {summary['datasets_total_files']}")
    print(f"   - Fichiers compressés : {summary['compressed_files']}")
    print(f"   - CSV extraits : {summary['extracted_csv_files']}")
    
    if extracted_files:
        print(f"\n📁 Fichiers CSV disponibles :")
        for file in extracted_files:
            file_size = os.path.getsize(file) / (1024 * 1024)  # Taille en MB
            print(f"   - {os.path.basename(file)} ({file_size:.1f} MB)")
    
    print("\n✅ Extraction terminée avec succès !")

if __name__ == "__main__":
    main() 