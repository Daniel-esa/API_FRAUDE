# API_Fraude/infrastructure/data_loader.py

import pandas as pd
from API_Fraude.config import settings


def load_data():
    """
    Charge les données depuis le chemin défini dans settings.
    """
    data_path = settings.DATA_PATH

    df = pd.read_sas(data_path, format='sas7bdat')

    return df
# df=load_data()
# print(df.head())

# Sous module donc peut pas être lancé directement. Préciser lors du lancement bash la requête suivante :
# python -m API_Fraude.infrastructure.data_loader 
# ou faire un main directement à la racine
# if __name__ == "__main__":
#     df = load_data()
#     print(df.head())