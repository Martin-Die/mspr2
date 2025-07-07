import pandas as pd
import os

INPUT_CSV = os.path.join('model_ia_steps', 'features_clusters.csv')
REPORT_PATH = os.path.join('model_ia_steps', 'clusters_analysis_report.txt')


def main():
    df = pd.read_csv(INPUT_CSV)
    if 'cluster' not in df.columns:
        print("Aucune colonne 'cluster' trouvée dans les données.")
        return
    clusters = df['cluster'].unique()
    report_lines = []
    report_lines.append(f"Nombre total de clusters : {len(clusters)}\n")
    for cluster in sorted(clusters):
        group = df[df['cluster'] == cluster]
        size = len(group)
        report_lines.append(f"\n--- Cluster {cluster} ---")
        report_lines.append(f"Taille du cluster : {size}")
        # Moyennes des features principales
        means = group.mean(numeric_only=True)
        report_lines.append("Moyennes des variables principales :")
        for col, val in means.items():
            if col not in ['cluster', 'user_id']:
                report_lines.append(f"  {col} : {val:.2f}")
        # Caractéristiques principales (features les plus élevées)
        top_features = means.drop(['cluster'], errors='ignore').sort_values(ascending=False).head(3)
        report_lines.append("Caractéristiques principales du groupe :")
        for feat, val in top_features.items():
            report_lines.append(f"  {feat} (moyenne : {val:.2f})")
        # Proposition de nom (exemple simple)
        if top_features.index[0] == 'total_spent':
            name = "Gros acheteurs"
        elif top_features.index[0] == 'conversion_rate':
            name = "Acheteurs efficaces"
        elif top_features.index[0] == 'view':
            name = "Curieux/Explorateurs"
        else:
            name = f"Cluster {cluster}"
        report_lines.append(f"Nom proposé : {name}\n")
    # Sauvegarde du rapport
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    print(f"Rapport d'analyse des clusters sauvegardé dans {REPORT_PATH}")

if __name__ == '__main__':
    main() 