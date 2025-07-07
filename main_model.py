# Ce script exécute séquentiellement toutes les étapes du pipeline IA (exploration, prétraitement, PCA, clustering, analyse des clusters).
# À lancer après le pipeline ETL (main_etl.py).
import subprocess
import os

steps = [
    'model_ia_steps/step1_load_explore.py',
    'model_ia_steps/step2_preprocess.py',
    'model_ia_steps/step3_pca.py',
    'model_ia_steps/step4_clustering.py',
    'model_ia_steps/step5_analyse_clusters.py',
]

if __name__ == '__main__':
    for step in steps:
        print(f"\n=== Exécution de {step} ===")
        ret = subprocess.run(['python', step])
        if ret.returncode != 0:
            print(f"Erreur lors de l'exécution de {step}. Arrêt du pipeline.")
            break
    print("\nPipeline IA terminé. Tous les fichiers de sortie sont dans le dossier 'model_ia_steps'.") 