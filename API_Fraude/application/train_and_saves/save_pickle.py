"""
Sauvegarde du modèle, des min et max du logit et du cutoff optimal en pickle.
"""
import joblib

from API_Fraude.application.train_and_saves import compute_score_params

from API_Fraude.application.train_and_saves import best_threshold_score, train_model
from API_Fraude.config import settings

# Sauvegarde de mes infos au formt pickle

print("Sauvegarde du fichier pickle en cours")

## Création d'un dictionnaire avec tous les objets nécessaires

fraud_model_package = {
    "model": train_model.modele,
    "columns": train_model.x_train_dummy.columns.tolist(),
    "min_logit": compute_score_params.min_logit,
    "max_logit": compute_score_params.max_logit,
    "cutoff": best_threshold_score.seuil_optimal,
    "score_cutoff": best_threshold_score.score_optimal
}

## Sauvegarde en Pickle
joblib.dump(fraud_model_package, settings.MODEL_PATH)

print("Modèle sauvegardé sous 'fraud_model.pkl'")


# RUff : un outil de linting et de formatage pour Python, rapide et moderne écrit en Rust
# "Ruff check . pour voir les erreurs
# Ruff check .--fix pour appliquer les corrections nécessaires  
