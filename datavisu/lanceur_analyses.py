"""
lanceur_analyses.py
Script de lancement principal pour toutes les analyses de données.
Permet d'exécuter les analyses de manière orchestrée et interactive.
"""
import os
import sys
import subprocess
import time
from pathlib import Path

# Configuration
EXTRACTED_CSV_DIR = './extracted_csv'
SCRIPTS_DIR = '.'

def check_prerequisites():
    """Vérifie les prérequis pour l'exécution des analyses."""
    print("🔍 Vérification des prérequis...")
    
    # Vérifier que le dossier extracted_csv existe
    if not Path(EXTRACTED_CSV_DIR).exists():
        print(f"❌ Le dossier {EXTRACTED_CSV_DIR} n'existe pas.")
        print("💡 Veuillez d'abord exécuter extract.py pour extraire les fichiers compressés.")
        return False
    
    # Vérifier qu'il y a des fichiers CSV
    csv_files = list(Path(EXTRACTED_CSV_DIR).rglob("*.csv"))
    if not csv_files:
        print(f"❌ Aucun fichier CSV trouvé dans {EXTRACTED_CSV_DIR}")
        print("💡 Veuillez d'abord exécuter extract.py pour extraire les fichiers compressés.")
        return False
    
    print(f"✅ {len(csv_files)} fichier(s) CSV trouvé(s)")
    return True

def list_available_scripts():
    """Liste les scripts d'analyse disponibles."""
    scripts = {
        '1': {
            'name': 'exploration_csv.py',
            'description': 'Exploration de base des données CSV',
            'output_dir': './exploration_results'
        },
        '2': {
            'name': 'analyse_complete.py',
            'description': 'Analyse complète avec aperçu général',
            'output_dir': 'analyse_complete'
        },
        '3': {
            'name': 'analyse_statistique.py',
            'description': 'Analyses statistiques avancées (corrélations, outliers, distributions)',
            'output_dir': 'analyses_statistiques'
        },
        '4': {
            'name': 'analyse_categorielle.py',
            'description': 'Analyses des variables catégorielles (distributions, associations)',
            'output_dir': 'analyses_categorielles'
        },
        '5': {
            'name': 'analyse_temporelle.py',
            'description': 'Analyses temporelles et séries temporelles',
            'output_dir': 'analyses_temporelles'
        }
    }
    return scripts

def display_menu():
    """Affiche le menu principal."""
    print("\n" + "="*60)
    print("📊 LANCEUR D'ANALYSES DE DONNÉES")
    print("="*60)
    
    scripts = list_available_scripts()
    
    print("\n📋 Scripts d'analyse disponibles :")
    for key, script in scripts.items():
        print(f"  {key}. {script['name']}")
        print(f"     {script['description']}")
        print(f"     📁 Sortie : {script['output_dir']}")
        print()
    
    print("🎯 Options spéciales :")
    print("  A. Exécuter TOUTES les analyses (séquentiellement)")
    print("  Q. Quitter")
    print()

def run_script(script_name):
    """Exécute un script d'analyse."""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    
    if not os.path.exists(script_path):
        print(f"❌ Script non trouvé : {script_path}")
        return False
    
    print(f"🚀 Exécution de {script_name}...")
    print("-" * 40)
    
    start_time = time.time()
    
    try:
        # Exécuter le script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, cwd=SCRIPTS_DIR)
        
        # Afficher la sortie
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("⚠️ Avertissements/Erreurs :")
            print(result.stderr)
        
        execution_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ {script_name} exécuté avec succès en {execution_time:.1f} secondes")
            return True
        else:
            print(f"❌ {script_name} a échoué (code de retour: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution de {script_name}: {e}")
        return False

def run_all_analyses():
    """Exécute toutes les analyses dans l'ordre recommandé."""
    print("🚀 Exécution de TOUTES les analyses...")
    print("="*60)
    
    scripts = list_available_scripts()
    execution_order = ['2', '1', '3', '4', '5']  # Ordre recommandé
    
    successful_scripts = []
    failed_scripts = []
    
    for script_key in execution_order:
        if script_key in scripts:
            script = scripts[script_key]
            print(f"\n📊 Étape {execution_order.index(script_key) + 1}/5 : {script['name']}")
            
            if run_script(script['name']):
                successful_scripts.append(script['name'])
            else:
                failed_scripts.append(script['name'])
            
            print()  # Ligne vide pour la lisibilité
    
    # Résumé final
    print("="*60)
    print("📋 RÉSUMÉ DE L'EXÉCUTION")
    print("="*60)
    print(f"✅ Scripts réussis ({len(successful_scripts)}):")
    for script in successful_scripts:
        print(f"  - {script}")
    
    if failed_scripts:
        print(f"\n❌ Scripts échoués ({len(failed_scripts)}):")
        for script in failed_scripts:
            print(f"  - {script}")
    
    print(f"\n📁 Résultats disponibles dans les dossiers :")
    for script_key in execution_order:
        if script_key in scripts:
            script = scripts[script_key]
            print(f"  - {script['output_dir']} ({script['name']})")

def main():
    """Fonction principale du lanceur."""
    print("🎯 Lanceur d'analyses de données")
    print("Version 1.0 - Analyse complète des données CSV")
    
    # Vérifier les prérequis
    if not check_prerequisites():
        return
    
    while True:
        display_menu()
        
        choice = input("🎯 Votre choix : ").strip().upper()
        
        if choice == 'Q':
            print("👋 Au revoir !")
            break
        
        elif choice == 'A':
            run_all_analyses()
            break
        
        elif choice in ['1', '2', '3', '4', '5']:
            scripts = list_available_scripts()
            script = scripts[choice]
            
            print(f"\n🎯 Exécution de : {script['name']}")
            print(f"📝 Description : {script['description']}")
            
            confirm = input("✅ Confirmer l'exécution ? (o/N) : ").strip().lower()
            if confirm in ['o', 'oui', 'y', 'yes']:
                run_script(script['name'])
            else:
                print("❌ Exécution annulée")
        
        else:
            print("❌ Choix invalide. Veuillez réessayer.")
        
        input("\n⏸️ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main() 