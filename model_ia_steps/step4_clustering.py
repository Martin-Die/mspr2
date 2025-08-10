import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

INPUT_CSV = os.path.join('model_ia_steps', 'features_pca.csv')
OUTPUT_CSV = os.path.join('model_ia_steps', 'features_clusters.csv')
PLOT_PATH = os.path.join('model_ia_steps', 'clusters_projection.png')


def main():
    # Chargement des données PCA
    df = pd.read_csv(INPUT_CSV)
    X = df.drop(columns=['user_id']) if 'user_id' in df.columns else df

    # Recherche du nombre optimal de clusters (méthode du coude + silhouette)
    inertias = []
    silhouettes = []
    K_range = range(2, 11)
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        inertias.append(kmeans.inertia_)
        silhouettes.append(silhouette_score(X, labels, sample_size=10000, random_state=42))
    # Affichage des courbes
    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.plot(K_range, inertias, marker='o')
    plt.xlabel('Nombre de clusters')
    plt.ylabel('Inertie (distorsion)')
    plt.title('Méthode du coude')
    plt.subplot(1,2,2)
    plt.plot(K_range, silhouettes, marker='o')
    plt.xlabel('Nombre de clusters')
    plt.ylabel('Score silhouette')
    plt.title('Score silhouette')
    plt.tight_layout()
    plt.savefig(os.path.join('model_ia_steps', 'clustering_diagnostics.png'))
    print("Courbes du coude et silhouette sauvegardées.")

    # Choix du nombre de clusters (exemple : max du score silhouette)
    best_k = K_range[silhouettes.index(max(silhouettes))]
    print(f"Nombre optimal de clusters retenu : {best_k}")

    # Clustering final
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    df['cluster'] = labels
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Résultats de clustering sauvegardés dans {OUTPUT_CSV}")

    # Visualisation des clusters sur PC1/PC2
    plt.figure(figsize=(8,6))
    for cluster in range(best_k):
        plt.scatter(df.loc[df['cluster']==cluster, 'PC1'], df.loc[df['cluster']==cluster, 'PC2'], label=f'Cluster {cluster}', s=10, alpha=0.5)
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title('Répartition des clusters sur les deux premières composantes')
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_PATH)
    print(f"Graphique des clusters sauvegardé dans {PLOT_PATH}")

if __name__ == '__main__':
    main() 