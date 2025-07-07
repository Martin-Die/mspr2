# Ce script principal orchestre l'exécution du pipeline ETL (main_etl.py) puis du pipeline IA (model_ia_steps/main_model_ia.py).
# À lancer depuis la racine du projet.
import subprocess
import sys

if __name__ == '__main__':
    print("=== Lancement du pipeline ETL ===")
    ret_etl = subprocess.run([sys.executable, 'main_etl.py'])
    if ret_etl.returncode != 0:
        print("Erreur lors de l'exécution du pipeline ETL. Arrêt du processus.")
        sys.exit(1)
    print("\n=== Lancement du pipeline IA ===")
    ret_ia = subprocess.run([sys.executable, 'model_ia_steps/main_model_ia.py'])
    if ret_ia.returncode != 0:
        print("Erreur lors de l'exécution du pipeline IA.")
        sys.exit(1)
    print("\nPipeline complet terminé avec succès !") 