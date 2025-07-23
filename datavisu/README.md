# 📊 Module d'Analyse de Données - Datavisu

Ce dossier contient une suite complète d'outils d'analyse de données pour explorer et analyser les fichiers CSV extraits.

## 🚀 Démarrage Rapide

### 0. Vérification de l'État du Projet (Recommandé en premier)
```bash
python 0_check_setup.py
```
Ce script vérifie les prérequis et vous guide pour la configuration.

### 1. Lanceur Principal (Recommandé)
```bash
python 1_lanceur_analyses.py
```
Le lanceur vous guide à travers toutes les analyses disponibles avec un menu interactif.

### 2. Exécution Directe
Vous pouvez également exécuter chaque script individuellement :

```bash
# Analyse complète (recommandé en premier)
python 3_analyse_complete.py

# Exploration de base
python 2_exploration_csv.py

# Analyses statistiques avancées
python 4_analyse_statistique.py

# Analyses des variables catégorielles
python 5_analyse_categorielle.py

# Analyses temporelles
python 6_analyse_temporelle.py
```

## ⚠️ Prérequis Importants

**Avant d'exécuter les analyses, assurez-vous que :**

1. **L'extraction a été effectuée** : Le dossier `../extracted_csv` doit contenir des fichiers CSV
2. **Les dépendances sont installées** : pandas, numpy, matplotlib, seaborn, scipy

Si vous obtenez une erreur "Le dossier ../extracted_csv n'existe pas", exécutez d'abord :
```bash
python ../etl_steps/extract.py
```

## 📋 Scripts Disponibles

### 1. `0_check_setup.py` 🔍
**Script de vérification et guide d'initialisation**
- Vérifie les dépendances Python
- Contrôle l'état d'extraction des données
- Guide l'utilisateur pour la configuration
- Recommande les prochaines étapes

### 2. `1_lanceur_analyses.py` 🎯
**Script principal recommandé**
- Interface interactive pour toutes les analyses
- Vérification automatique des prérequis
- Exécution orchestrée de toutes les analyses
- Gestion des erreurs et rapports de progression

### 2. `3_analyse_complete.py` 📊
**Analyse d'aperçu général**
- Résumé complet de chaque fichier CSV
- Visualisations des valeurs manquantes
- Distribution des types de données
- Matrices de corrélation
- Recommandations d'analyse

**Sortie :** Dossier `analyse_complete/`

### 3. `2_exploration_csv.py` 🔍
**Exploration de base des données**
- Informations générales sur les fichiers
- Structure des données
- Qualité des données (valeurs manquantes)
- Statistiques descriptives
- Exemples de valeurs

**Sortie :** Dossier `../exploration_results/`

### 4. `4_analyse_statistique.py` 📈
**Analyses statistiques avancées**
- Matrices de corrélation avec heatmaps
- Détection d'outliers (méthode IQR)
- Analyse des distributions
- Tests de normalité
- Tests statistiques (Spearman, Mann-Whitney)

**Sortie :** Dossier `analyses_statistiques/`

### 5. `5_analyse_categorielle.py` 📊
**Analyses des variables catégorielles**
- Distributions des variables catégorielles
- Tests de chi-carré entre variables
- Coefficient de Cramér
- Relations avec variables numériques (ANOVA)
- Visualisations (barres, camembert, boxplots)

**Sortie :** Dossier `analyses_categorielles/`

### 6. `6_analyse_temporelle.py` 📅
**Analyses temporelles et séries temporelles**
- Détection automatique des colonnes de dates
- Tendances temporelles
- Saisonnalité
- Patterns mensuels/annuels
- Régression linéaire pour les tendances

**Sortie :** Dossier `analyses_temporelles/`

## 📁 Structure des Résultats

```
datavisu/
├── analyse_complete/           # Analyses d'aperçu général
│   ├── 00_master_summary.txt   # Résumé maître de toutes les analyses
│   ├── *_comprehensive_report.txt
│   ├── *_missing_values.png
│   ├── *_data_types.png
│   └── *_correlation_matrix.png
│
├── analyses_statistiques/      # Analyses statistiques avancées
│   ├── *_statistical_report.txt
│   ├── *_correlation_heatmap.png
│   └── *_distributions.png
│
├── analyses_categorielles/     # Analyses des variables catégorielles
│   ├── *_categorical_report.txt
│   ├── *_distribution.png
│   ├── *_associations.png
│   └── *_cat_num_relationships.png
│
├── analyses_temporelles/       # Analyses temporelles
│   ├── *_temporal_report.txt
│   └── *_temporal_patterns.png
│
└── ../exploration_results/     # Exploration de base (déplacé)
    ├── 00_summary_exploration.txt
    └── *_exploration.txt
```

## 🎯 Ordre d'Exécution Recommandé

1. **`analyse_complete.py`** - Aperçu général et recommandations
2. **`exploration_csv.py`** - Exploration de base
3. **`analyse_statistique.py`** - Corrélations et outliers
4. **`analyse_categorielle.py`** - Variables catégorielles
5. **`analyse_temporelle.py`** - Séries temporelles

## 📊 Types d'Analyses Disponibles

### Analyses Numériques
- ✅ Corrélations (Pearson, Spearman)
- ✅ Détection d'outliers (IQR)
- ✅ Distributions et tests de normalité
- ✅ Statistiques descriptives
- ✅ Tests statistiques (Mann-Whitney, ANOVA)

### Analyses Catégorielles
- ✅ Distributions et fréquences
- ✅ Tests de chi-carré
- ✅ Coefficient de Cramér
- ✅ Associations entre variables
- ✅ Relations avec variables numériques

### Analyses Temporelles
- ✅ Détection automatique des dates
- ✅ Tendances linéaires
- ✅ Saisonnalité
- ✅ Patterns temporels
- ✅ Régression temporelle

### Visualisations
- ✅ Heatmaps de corrélation
- ✅ Histogrammes et distributions
- ✅ Boxplots et outliers
- ✅ Graphiques temporels
- ✅ Graphiques catégoriels

## ⚙️ Prérequis

### Dépendances Python
```bash
pip install pandas numpy matplotlib seaborn scipy
```

### Structure des Données
- Les fichiers CSV doivent être dans le dossier `../extracted_csv/`
- Format CSV standard avec séparateur virgule
- Encodage UTF-8 recommandé

## 🔧 Configuration

### Chemins des Dossiers
Les scripts utilisent les chemins relatifs suivants :
- `../extracted_csv/` - Fichiers CSV source
- `../exploration_results/` - Résultats d'exploration
- `./analyses_*/` - Résultats des analyses spécialisées

### Paramètres d'Analyse
- **Taille d'échantillon** : 10 000 lignes par défaut
- **Seuil de corrélation** : |r| > 0.5 pour les corrélations significatives
- **Seuil d'outliers** : Méthode IQR (Q1 - 1.5*IQR, Q3 + 1.5*IQR)
- **Seuil de significativité** : p < 0.05

## 📈 Interprétation des Résultats

### Corrélations
- **|r| > 0.7** : Corrélation forte
- **0.3 < |r| < 0.7** : Corrélation modérée
- **|r| < 0.3** : Corrélation faible

### Tests Statistiques
- **p < 0.05** : Différence significative
- **p < 0.01** : Différence très significative
- **p < 0.001** : Différence hautement significative

### Coefficient de Cramér
- **V > 0.3** : Association forte
- **0.1 < V < 0.3** : Association modérée
- **V < 0.1** : Association faible

## 🚨 Dépannage

### Erreurs Courantes

1. **"Aucun fichier CSV trouvé"**
   - Vérifiez que `extract.py` a été exécuté
   - Vérifiez le dossier `../extracted_csv/`

2. **"Module non trouvé"**
   - Installez les dépendances : `pip install pandas numpy matplotlib seaborn scipy`

3. **"Erreur de mémoire"**
   - Réduisez la taille d'échantillon dans les scripts
   - Utilisez des fichiers plus petits

4. **"Erreur d'encodage"**
   - Vérifiez que les fichiers CSV sont en UTF-8
   - Utilisez des fichiers sans caractères spéciaux

### Conseils d'Optimisation

- **Gros fichiers** : Les scripts utilisent des échantillons de 10 000 lignes
- **Mémoire** : Fermez les autres applications pendant l'analyse
- **Performance** : Exécutez les analyses une par une pour les gros datasets

## 📞 Support

Pour toute question ou problème :
1. Consultez les rapports d'erreur générés
2. Vérifiez les prérequis et la structure des dossiers
3. Testez avec un petit fichier CSV d'abord

---

**Version :** 1.0  
**Dernière mise à jour :** 2024  
**Auteur :** Module d'analyse de données MSPR2 