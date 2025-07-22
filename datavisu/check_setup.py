"""
check_setup.py
Script de vérification de l'état du projet et guide d'initialisation.
Vérifie les prérequis et guide l'utilisateur pour la configuration.
"""
import os
import sys
from pathlib import Path

def check_extraction_status():
    """Vérifie si l'extraction a été effectuée."""
    extracted_dir = Path("../extracted_csv")
    datasets_dir = Path("../datasets")
    
    print("🔍 Vérification de l'état d'extraction...")
    
    # Vérifier si le dossier datasets existe
    if not datasets_dir.exists():
        print("❌ Le dossier ../datasets n'existe pas.")
        print("💡 Veuillez créer le dossier datasets et y placer vos fichiers compressés.")
        return False
    
    # Lister les fichiers dans datasets
    datasets_files = list(datasets_dir.glob("*"))
    compressed_files = [f for f in datasets_files if f.is_file() and any(f.name.endswith(ext) for ext in ['.gz', '.zip', '.tar', '.bz2'])]
    
    if not compressed_files:
        print("⚠️ Aucun fichier compressé trouvé dans ../datasets")
        print("💡 Veuillez placer vos fichiers .gz, .zip, .tar dans le dossier datasets")
        return False
    
    print(f"✅ {len(compressed_files)} fichier(s) compressé(s) trouvé(s) dans ../datasets")
    
    # Vérifier si l'extraction a été faite
    if not extracted_dir.exists():
        print("❌ Le dossier ../extracted_csv n'existe pas.")
        print("💡 L'extraction n'a pas encore été effectuée.")
        return False
    
    # Lister les fichiers CSV extraits
    csv_files = list(extracted_dir.rglob("*.csv"))
    
    if not csv_files:
        print("❌ Aucun fichier CSV trouvé dans ../extracted_csv")
        print("💡 L'extraction n'a pas encore été effectuée ou a échoué.")
        return False
    
    print(f"✅ {len(csv_files)} fichier(s) CSV trouvé(s) dans ../extracted_csv")
    
    # Afficher les tailles des fichiers
    total_size = sum(f.stat().st_size for f in csv_files)
    print(f"📊 Taille totale des CSV : {total_size / (1024*1024):.1f} MB")
    
    return True

def check_dependencies():
    """Vérifie les dépendances Python."""
    print("\n🔍 Vérification des dépendances...")
    
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MANQUANT")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Packages manquants : {', '.join(missing_packages)}")
        print("💡 Installez-les avec : pip install " + " ".join(missing_packages))
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True

def show_next_steps():
    """Affiche les prochaines étapes recommandées."""
    print("\n🎯 PROCHAINES ÉTAPES RECOMMANDÉES :")
    print("=" * 50)
    
    if not check_extraction_status():
        print("\n1️⃣ EXTRACTION DES DONNÉES :")
        print("   python ../etl_steps/extract.py")
        print("   (Cela va extraire les fichiers compressés en CSV)")
        return
    
    print("\n2️⃣ EXPLORATION DE BASE :")
    print("   python exploration_csv.py")
    print("   (Analyse rapide de la structure des données)")
    
    print("\n3️⃣ ANALYSE COMPLÈTE :")
    print("   python analyse_complete.py")
    print("   (Aperçu général et résumé des données)")
    
    print("\n4️⃣ ANALYSES SPÉCIALISÉES :")
    print("   python analyse_statistique.py    # Corrélations, outliers")
    print("   python analyse_categorielle.py   # Variables catégorielles")
    print("   python analyse_temporelle.py     # Séries temporelles")
    
    print("\n5️⃣ LANCEUR INTERACTIF :")
    print("   python lanceur_analyses.py")
    print("   (Menu interactif pour toutes les analyses)")

def main():
    """Fonction principale."""
    print("🚀 VÉRIFICATION DE L'ÉTAT DU PROJET")
    print("=" * 50)
    
    # Vérifier les dépendances
    deps_ok = check_dependencies()
    
    # Vérifier l'état d'extraction
    extraction_ok = check_extraction_status()
    
    print("\n📊 RÉSUMÉ :")
    print(f"   Dépendances : {'✅ OK' if deps_ok else '❌ MANQUANTES'}")
    print(f"   Extraction : {'✅ FAITE' if extraction_ok else '❌ À FAIRE'}")
    
    # Afficher les prochaines étapes
    show_next_steps()

if __name__ == "__main__":
    main() 