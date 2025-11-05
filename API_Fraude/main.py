# main.py
import pandas as pd
# from API_Fraude.infrastructure.loading.data_loader import load_data
# from API_Fraude.application.train_and_saves.train_model import  x_train, modele, y_train, df, df_processed, x_train_dummy
# from API_Fraude.application import detect_fraud
# from API_Fraude.infrastructure.loading import load_model_pickle
# from API_Fraude.config import settings
# from API_Fraude.tests import create_sampling
from pathlib import Path

import uvicorn

def main():
    uvicorn.run(
        "API_Fraude.application.api_interface:app",
        host="127.0.0.2",#"0.0.0.0",#
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()
    
# streamlit run "C:\Users\dsonne\OneDrive - Micropole\Documents\Projet Python\Fraud detector\API_Fraude\API_Fraude\application\streamlit_interface.py"

#df_fraude = pd.read_json(create_sampling.test_path/"sample_fraude.json", lines=True)
# if __name__ == "__main__":
#     df = load_data()
#     print(df.head())
    
    # print(print_columns_to_drop)
    # print(df_processed)
    # print(x_train_dummy)
    # print(y_train)
    # print(load_model_pickle.load_pickle())
    # print(create_sampling.create_data_tests(10))
    #print(detect_fraud.predict_from_dataframe(df_fraude))

# if __name__ == "__main__":
#     # print(Path(__file__))
#     # print(Path(__file__).parent.parent)
#     # print(__)
#     uvicorn.run(
#         "API_Fraude.infrastructure.api_interface:app",
#         host="127.0.0.1",
#         port=8000,
#         reload=True
#     )

# pip install -e . : installe le package en mode editable, ce qui permet de modifier le code source sans réinstaller le package.