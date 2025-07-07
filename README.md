# Projet IA - Catégorisation des clients d'Amazing

## Présentation
Ce projet vise à catégoriser les clients d'une marketplace (Amazing) selon leurs comportements d'achat et de navigation, à l'aide d'un pipeline ETL robuste et d'un pipeline IA basé sur le clustering non supervisé.

- **Données** : Fichiers d'événements utilisateurs (CSV volumineux)
- **Objectif** : Identifier des groupes de clients pour adapter l'offre, le marketing et la personnalisation
- **Respect RGPD** : Données anonymisées, aucun traitement nominatif

## Organisation du projet
```
mspr2/
│
├── etl_steps/           # Scripts ETL (extraction, transformation, chargement)
│     ├── extract.py
│     ├── transform.py
│     └── load.py
│
├── model_ia_steps/      # Scripts IA (exploration, PCA, clustering, analyse)
│     ├── step1_load_explore.py
│     ├── step2_preprocess.py
│     ├── step3_pca.py
│     ├── step4_clustering.py
│     └── step5_analyse_clusters.py
│
├── datasets/            # Fichiers CSV bruts
├── output/              # Données utilisateurs agrégées (features)
├── exploration_results/ # Rapports d'exploration des CSV bruts
│
├── main_all.py          # Orchestration complète (ETL + IA)
├── main_etl.py          # Pipeline ETL seul
├── main_model.py        # Pipeline IA seul
│
└── requirements.txt     # Dépendances Python
```

## Prérequis
- Python 3.10 ou 3.11 recommandé
- Installer les dépendances :
  ```bash
  pip install -r requirements.txt
  ```

## Exécution du projet

### 1. Pipeline complet (ETL + IA)
```bash
python main_all.py
```
- Extrait, nettoie, agrège les données utilisateurs
- Catégorise les clients par clustering
- Génère tous les rapports et graphiques dans `output/` et `model_ia_steps/`

### 2. Pipeline ETL seul
```bash
python main_etl.py
```
- Produit le fichier `output/features_all_users.csv` à partir des CSV bruts

### 3. Pipeline IA seul
```bash
python main_model.py
```
- À utiliser si les features utilisateurs sont déjà générées
- Produit les clusters, rapports et visualisations dans `model_ia_steps/`

## Détail des étapes IA
1. **Exploration** : Statistiques, valeurs manquantes, outliers
2. **Prétraitement** : Normalisation, gestion des extrêmes
3. **PCA** : Réduction de dimensionnalité, visualisation
4. **Clustering** : K-Means, choix du nombre de groupes (coude, silhouette)
5. **Analyse** : Description, nommage et rapport sur chaque cluster

## Conseils pour l'analyse et la soutenance
- Justifiez chaque choix (features, seuils, algorithmes)
- Interprétez les groupes trouvés (profils-types, recommandations métier)
- Mettez en avant la robustesse, la reproductibilité et le respect du RGPD
- Utilisez les graphiques générés pour illustrer vos propos

## Respect du RGPD
- Les données sont anonymisées (`user_id` non nominatif)
- Aucun traitement nominatif ou sensible
- Les scripts sont conçus pour garantir la confidentialité et la sécurité des données

## Auteurs
- Projet réalisé dans le cadre de la certification Chef.fe de projet expert en IA (RNCP36582) 