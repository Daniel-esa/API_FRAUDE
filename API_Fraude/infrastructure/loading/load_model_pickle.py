"""
Chargement de mon pickle
"""

import joblib
from API_Fraude.config import settings

def load_pickle() :
    
    model_pack = joblib.load(settings.MODEL_PATH)
    return model_pack