"""
analyse_temporelle.py
Analyses temporelles et séries temporelles des données CSV.
Inclut tendances, saisonnalité, et patterns temporels.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
EXTRACTED_CSV_DIR = '../extracted_csv'
RESULTS_DIR = '../exploration_results'
TEMPORAL_DIR = 'analyses_temporelles'

def create_temporal_directory():
    """Crée le dossier pour les analyses temporelles."""
    os.makedirs(TEMPORAL_DIR, exist_ok=True)

def detect_date_columns(df):
    """Détecte les colonnes qui pourraient contenir des dates."""
    date_columns = []
    
    for col in df.columns:
        # Vérifier si la colonne contient des valeurs qui ressemblent à des dates
        sample_values = df[col].dropna().head(100)
        
        if len(sample_values) > 0:
            # Essayer de convertir en datetime
            try:
                pd.to_datetime(sample_values, errors='raise')
                date_columns.append(col)
            except:
                # Vérifier si le nom de la colonne suggère une date
                col_lower = col.lower()
                date_keywords = ['date', 'time', 'timestamp', 'jour', 'mois', 'année', 'year', 'month', 'day']
                if any(keyword in col_lower for keyword in date_keywords):
                    try:
                        pd.to_datetime(sample_values, errors='coerce')
                        if sample_values.notna().sum() > len(sample_values) * 0.5:  # Au moins 50% de dates valides
                            date_columns.append(col)
                    except:
                        pass
    
    return date_columns

def convert_to_datetime(df, date_columns):
    """Convertit les colonnes de dates en datetime."""
    df_temp = df.copy()
    
    for col in date_columns:
        try:
            df_temp[col] = pd.to_datetime(df_temp[col], errors='coerce')
        except Exception as e:
            print(f"Erreur lors de la conversion de {col}: {e}")
    
    return df_temp

def analyze_temporal_patterns(df, date_col, value_col, filename):
    """Analyse les patterns temporels d'une variable."""
    # Nettoyer les données
    temp_df = df[[date_col, value_col]].dropna()
    
    if len(temp_df) < 10:
        return None
    
    # Trier par date
    temp_df = temp_df.sort_values(date_col)
    
    # Extraire les composantes temporelles
    temp_df['year'] = temp_df[date_col].dt.year
    temp_df['month'] = temp_df[date_col].dt.month
    temp_df['day'] = temp_df[date_col].dt.day
    temp_df['weekday'] = temp_df[date_col].dt.weekday
    temp_df['quarter'] = temp_df[date_col].dt.quarter
    
    # Analyses temporelles
    patterns = {}
    
    # Tendances par année
    yearly_trend = temp_df.groupby('year')[value_col].agg(['mean', 'std', 'count']).reset_index()
    patterns['yearly_trend'] = yearly_trend
    
    # Patterns mensuels
    monthly_pattern = temp_df.groupby('month')[value_col].agg(['mean', 'std', 'count']).reset_index()
    patterns['monthly_pattern'] = monthly_pattern
    
    # Patterns par jour de la semaine
    weekday_pattern = temp_df.groupby('weekday')[value_col].agg(['mean', 'std', 'count']).reset_index()
    patterns['weekday_pattern'] = weekday_pattern
    
    # Patterns par trimestre
    quarterly_pattern = temp_df.groupby('quarter')[value_col].agg(['mean', 'std', 'count']).reset_index()
    patterns['quarterly_pattern'] = quarterly_pattern
    
    # Visualisations
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Évolution temporelle
    axes[0, 0].plot(temp_df[date_col], temp_df[value_col], alpha=0.6)
    axes[0, 0].set_title(f'Évolution temporelle de {value_col}')
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel(value_col)
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 2. Tendances annuelles
    axes[0, 1].bar(yearly_trend['year'], yearly_trend['mean'])
    axes[0, 1].set_title(f'Tendance annuelle de {value_col}')
    axes[0, 1].set_xlabel('Année')
    axes[0, 1].set_ylabel(f'Moyenne {value_col}')
    
    # 3. Patterns mensuels
    month_names = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 
                   'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
    axes[1, 0].bar(monthly_pattern['month'], monthly_pattern['mean'])
    axes[1, 0].set_title(f'Pattern mensuel de {value_col}')
    axes[1, 0].set_xlabel('Mois')
    axes[1, 0].set_ylabel(f'Moyenne {value_col}')
    axes[1, 0].set_xticks(range(1, 13))
    axes[1, 0].set_xticklabels(month_names, rotation=45)
    
    # 4. Patterns par jour de la semaine
    day_names = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    axes[1, 1].bar(weekday_pattern['weekday'], weekday_pattern['mean'])
    axes[1, 1].set_title(f'Pattern par jour de la semaine de {value_col}')
    axes[1, 1].set_xlabel('Jour de la semaine')
    axes[1, 1].set_ylabel(f'Moyenne {value_col}')
    axes[1, 1].set_xticks(range(7))
    axes[1, 1].set_xticklabels(day_names)
    
    plt.tight_layout()
    plt.savefig(os.path.join(TEMPORAL_DIR, f'{filename}_{value_col}_temporal_patterns.png'), dpi=300)
    plt.close()
    
    return patterns

def calculate_trends(df, date_col, value_col):
    """Calcule les tendances linéaires."""
    temp_df = df[[date_col, value_col]].dropna()
    
    if len(temp_df) < 5:
        return None
    
    # Convertir les dates en nombres pour la régression
    temp_df = temp_df.sort_values(date_col)
    temp_df['date_numeric'] = (temp_df[date_col] - temp_df[date_col].min()).dt.days
    
    # Régression linéaire
    x = temp_df['date_numeric'].values
    y = temp_df[value_col].values
    
    # Calculer la pente et l'intercept
    slope, intercept = np.polyfit(x, y, 1)
    
    # Calculer R²
    y_pred = slope * x + intercept
    r_squared = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2)
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'trend_direction': 'croissante' if slope > 0 else 'décroissante',
        'trend_strength': 'forte' if abs(r_squared) > 0.7 else 'modérée' if abs(r_squared) > 0.3 else 'faible'
    }

def detect_seasonality(df, date_col, value_col):
    """Détecte la saisonnalité dans les données."""
    temp_df = df[[date_col, value_col]].dropna()
    
    if len(temp_df) < 12:  # Au moins 12 observations pour détecter la saisonnalité
        return None
    
    # Extraire les composantes saisonnières
    temp_df = temp_df.sort_values(date_col)
    temp_df['month'] = temp_df[date_col].dt.month
    
    # Calculer la variance entre les mois
    monthly_means = temp_df.groupby('month')[value_col].mean()
    overall_mean = temp_df[value_col].mean()
    
    # Coefficient de variation saisonnier
    seasonal_variance = np.var(monthly_means)
    total_variance = np.var(temp_df[value_col])
    seasonal_strength = seasonal_variance / total_variance if total_variance > 0 else 0
    
    # Identifier les mois avec les valeurs les plus élevées/basses
    peak_month = monthly_means.idxmax()
    trough_month = monthly_means.idxmin()
    
    return {
        'seasonal_strength': seasonal_strength,
        'has_seasonality': seasonal_strength > 0.1,
        'peak_month': peak_month,
        'trough_month': trough_month,
        'monthly_means': monthly_means.to_dict()
    }

def analyze_temporal_data(df, filename):
    """Analyse complète des données temporelles."""
    print(f"📅 Analyse temporelle de {filename}...")
    
    # Détecter les colonnes de dates
    date_columns = detect_date_columns(df)
    
    if not date_columns:
        print(f"  ⚠️ Aucune colonne de date détectée dans {filename}")
        return False
    
    # Convertir en datetime
    df_temp = convert_to_datetime(df, date_columns)
    
    # Colonnes numériques pour l'analyse
    numeric_columns = df_temp.select_dtypes(include=[np.number]).columns
    
    if len(numeric_columns) == 0:
        print(f"  ⚠️ Aucune colonne numérique trouvée dans {filename}")
        return False
    
    # Analyser chaque combinaison date-valeur
    analyses_results = {}
    
    for date_col in date_columns:
        for value_col in numeric_columns:
            if date_col != value_col:
                print(f"  📊 Analyse {date_col} → {value_col}")
                
                # Patterns temporels
                patterns = analyze_temporal_patterns(df_temp, date_col, value_col, filename)
                
                # Tendances
                trends = calculate_trends(df_temp, date_col, value_col)
                
                # Saisonnalité
                seasonality = detect_seasonality(df_temp, date_col, value_col)
                
                analyses_results[f"{date_col}_{value_col}"] = {
                    'patterns': patterns,
                    'trends': trends,
                    'seasonality': seasonality
                }
    
    # Générer le rapport
    generate_temporal_report(analyses_results, filename)
    
    return True

def generate_temporal_report(analyses_results, filename):
    """Génère un rapport d'analyse temporelle."""
    report_path = os.path.join(TEMPORAL_DIR, f'{filename}_temporal_report.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"RAPPORT D'ANALYSE TEMPORELLE - {filename}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"📅 ANALYSES TEMPORELLES EFFECTUÉES\n")
        f.write(f"Nombre de combinaisons analysées : {len(analyses_results)}\n\n")
        
        for analysis_key, results in analyses_results.items():
            date_col, value_col = analysis_key.split('_', 1)
            f.write(f"🔍 ANALYSE : {date_col} → {value_col}\n")
            f.write("-" * 40 + "\n")
            
            # Tendances
            if results['trends']:
                trends = results['trends']
                f.write(f"📈 TENDANCES :\n")
                f.write(f"  - Direction : {trends['trend_direction']}\n")
                f.write(f"  - Pente : {trends['slope']:.4f}\n")
                f.write(f"  - R² : {trends['r_squared']:.4f}\n")
                f.write(f"  - Force de la tendance : {trends['trend_strength']}\n\n")
            
            # Saisonnalité
            if results['seasonality']:
                seasonality = results['seasonality']
                f.write(f"🌍 SAISONNALITÉ :\n")
                f.write(f"  - Présence de saisonnalité : {'Oui' if seasonality['has_seasonality'] else 'Non'}\n")
                f.write(f"  - Force saisonnière : {seasonality['seasonal_strength']:.4f}\n")
                if seasonality['has_seasonality']:
                    f.write(f"  - Mois de pic : {seasonality['peak_month']}\n")
                    f.write(f"  - Mois de creux : {seasonality['trough_month']}\n")
                f.write("\n")
            
            # Patterns temporels
            if results['patterns']:
                patterns = results['patterns']
                f.write(f"📊 PATTERNS TEMPORELS :\n")
                
                if 'yearly_trend' in patterns:
                    yearly = patterns['yearly_trend']
                    f.write(f"  - Tendances annuelles :\n")
                    for _, row in yearly.iterrows():
                        f.write(f"    {row['year']}: {row['mean']:.2f} (n={row['count']})\n")
                    f.write("\n")
                
                if 'monthly_pattern' in patterns:
                    monthly = patterns['monthly_pattern']
                    f.write(f"  - Patterns mensuels :\n")
                    for _, row in monthly.iterrows():
                        f.write(f"    Mois {row['month']}: {row['mean']:.2f} (n={row['count']})\n")
                    f.write("\n")
            
            f.write("\n")
        
        f.write(f"📁 FICHIERS GÉNÉRÉS :\n")
        f.write(f"  - Graphiques : {filename}_*_temporal_patterns.png\n")
        f.write(f"  - Rapport : {filename}_temporal_report.txt\n")
    
    print(f"✅ Rapport temporel généré : {report_path}")

def main():
    """Fonction principale pour les analyses temporelles."""
    print("📅 Début des analyses temporelles...")
    
    # Créer le dossier de résultats
    create_temporal_directory()
    
    # Lister les fichiers CSV
    extracted_dir = Path(EXTRACTED_CSV_DIR)
    if not extracted_dir.exists():
        print(f"❌ Le dossier {EXTRACTED_CSV_DIR} n'existe pas.")
        print("💡 Veuillez d'abord exécuter extract.py pour extraire les fichiers compressés.")
        print("   Commande : python ../etl_steps/extract.py")
        return
    
    csv_files = list(extracted_dir.rglob("*.csv"))
    
    if not csv_files:
        print("❌ Aucun fichier CSV trouvé.")
        print("💡 Veuillez d'abord exécuter extract.py pour extraire les fichiers compressés.")
        print("   Commande : python ../etl_steps/extract.py")
        return
    
    print(f"📁 {len(csv_files)} fichier(s) CSV trouvé(s)")
    
    # Analyser chaque fichier
    successful_analyses = 0
    for csv_path in csv_files:
        try:
            # Charger un échantillon
            df = pd.read_csv(csv_path, nrows=10000)
            filename = os.path.splitext(os.path.basename(csv_path))[0]
            
            if analyze_temporal_data(df, filename):
                successful_analyses += 1
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse de {csv_path}: {e}")
    
    print(f"\n✅ Analyses temporelles terminées !")
    print(f"   - Fichiers analysés : {successful_analyses}/{len(csv_files)}")
    print(f"   - Résultats dans : {TEMPORAL_DIR}")

if __name__ == "__main__":
    main() 