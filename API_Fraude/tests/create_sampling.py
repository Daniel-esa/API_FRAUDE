from API_Fraude.infrastructure.loading.data_loader import load_data
from pathlib import Path
from API_Fraude.config import settings, settings_models
import pandas as pd

def create_data_tests(n_obs_each=20):
    """n_obs_each est le nombre de 1 et le nombre de 0 voulu 
    """
    # Étape 1 : Charger les données
    df_fraude = load_data()

    # Étape 2 : Échantillonnage
    df_fraude_1 = df_fraude[df_fraude['fraude'] == 1].sample(n=n_obs_each, random_state=settings.SEED)
    df_fraude_0 = df_fraude[df_fraude['fraude'] == 0].sample(n=n_obs_each, random_state=settings.SEED)

    # Étape 3 : Combiner les deux
    df_sample_fraude = pd.concat([df_fraude_1, df_fraude_0], ignore_index=True)

    # Étape 4 : Export
    test_path = Path(settings.TEST_PATH)
    # JSON
    df_sample_fraude.to_json(test_path/'sample_fraude.json', orient='records', lines=True)

    # Excel
    df_sample_fraude.to_excel(test_path/'sample_fraude.xlsx', index=False)

    return "Fichier créé"

test_path = Path(settings.TEST_PATH)


