import pandas as pd
import os
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

INPUT_CSV = os.path.join('model_ia_steps', 'features_normalized.csv')
OUTPUT_CSV = os.path.join('model_ia_steps', 'features_pca.csv')
PLOT_PATH = os.path.join('model_ia_steps', 'pca_projection.png')


def main():
    # Chargement des données
    df = pd.read_csv(INPUT_CSV)
    print(f"Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")

    # On conserve l'identifiant utilisateur si présent
    user_ids = df['user_id'] if 'user_id' in df.columns else None
    X = df.drop(columns=['user_id']) if 'user_id' in df.columns else df

    # PCA : on garde assez de composantes pour expliquer 90% de la variance
    pca = PCA(n_components=0.9, svd_solver='full')
    X_pca = pca.fit_transform(X)
    print(f"Nombre de composantes principales retenues : {X_pca.shape[1]}")
    print("Variance expliquée cumulée :", pca.explained_variance_ratio_.sum())

    # Sauvegarde des composantes principales
    df_pca = pd.DataFrame(X_pca, columns=[f'PC{i+1}' for i in range(X_pca.shape[1])])
    if user_ids is not None:
        df_pca.insert(0, 'user_id', user_ids)
    df_pca.to_csv(OUTPUT_CSV, index=False)
    print(f"Composantes principales sauvegardées dans {OUTPUT_CSV}")

    # Graphique de projection sur les deux premières composantes
    plt.figure(figsize=(8,6))
    plt.scatter(df_pca['PC1'], df_pca['PC2'], alpha=0.3, s=10)
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title('Projection des utilisateurs sur les deux premières composantes principales')
    plt.tight_layout()
    plt.savefig(PLOT_PATH)
    print(f"Graphique de projection sauvegardé dans {PLOT_PATH}")

if __name__ == '__main__':
    main() 