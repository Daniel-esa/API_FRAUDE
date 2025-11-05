"""
Détermination du seuil et du score optimal de détection de fraude à partir des scores du modèle entraîné.
"""
from sklearn.metrics import roc_curve
import numpy as np
import pandas as pd
from pathlib import Path
import joblib

from API_Fraude.application.train_and_saves import compute_score_params
from API_Fraude.application.train_and_saves import train_model
from API_Fraude.config import settings_score, settings
from API_Fraude.domain.score_mapper import log_odd, compute_score
from API_Fraude.domain import fraud_rules
## ROC : récupération des seuils
fpr, tpr, thresholds = roc_curve(train_model.y_test, compute_score_params.probas)

log_odds_roc_curve = log_odd(thresholds[1:])

## Conversion en score
scores = compute_score(thresholds[1:], compute_score_params.min_logit, compute_score_params.max_logit, settings_score.MIN_SCORE, settings_score.MAX_SCORE).astype(int)

df_cutoffs = pd.DataFrame({
    'Seuil': np.round(np.clip(thresholds[1:], 1e-6, 1 - 1e-6), 5),
    'Score associé': scores
}).drop_duplicates(subset=['Seuil']).reset_index(drop=True)

# Pour chaque seuil, calcul de métriques
shape_model = len(compute_score_params.probas)

df_cutoffs['N Supens'] = df_cutoffs['Seuil'].apply(lambda p: np.sum(compute_score_params.probas >= p))
df_cutoffs['N vir accepté'] = shape_model - df_cutoffs['N Supens']
df_cutoffs['Taux de vir suspendus'] = df_cutoffs['N Supens'] / shape_model
df_cutoffs['Taux de vir accepté'] = 1 - df_cutoffs['Taux de vir suspendus']
df_cutoffs['Pertinence'] = [
    (train_model.y_test[compute_score_params.probas >= seuil].sum() / n_supens) if n_supens > 0 else 0
    for seuil, n_supens in zip(df_cutoffs['Seuil'], df_cutoffs['N Supens'])
]

total_fraudes = train_model.y_test.sum()

df_cutoffs['Taux de détection'] = [
    (train_model.y_test[(compute_score_params.probas >= seuil) & (train_model.y_test == 1)].sum() / total_fraudes) if total_fraudes > 0 else 0
    for seuil in df_cutoffs['Seuil']
]

# ==== DÉTERMINATION DU SEUIL OPTIMAL ====
subset = df_cutoffs[df_cutoffs["Taux de détection"] >= fraud_rules.DETECTION_RATE_THRESHOLD]
max_pertinence = subset["Pertinence"].max()
seuil_optimal = df_cutoffs[(df_cutoffs['Pertinence'] == max_pertinence) &
                           (df_cutoffs["Taux de détection"] >= fraud_rules.DETECTION_RATE_THRESHOLD)]["Seuil"].max()
score_optimal = df_cutoffs[(df_cutoffs['Pertinence'] == max_pertinence) &
                           (df_cutoffs["Taux de détection"] >= fraud_rules.DETECTION_RATE_THRESHOLD)]["Score associé"].max()

# print(f"Le seuil optimal est {seuil_optimal} et le score associé est {score_optimal}")
# print(df_cutoffs[df_cutoffs["Score associé"] == 570])


