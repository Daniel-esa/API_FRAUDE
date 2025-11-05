"""
Entrainement du modèle à l'aide d'un XGB Classifier
"""
# Import de packages

## Chargement de la donnée

from pathlib import Path

## Pétraitement/Sélection/Split

import pandas as pd

## Modelize

from xgboost import XGBClassifier

## Save models using pickle

import joblib

# My packages

from API_Fraude.infrastructure.loading.data_loader import load_data
from API_Fraude.config import settings, settings_models
from API_Fraude.infrastructure.data_modification.preprocessing import preprocess_input
from API_Fraude.infrastructure.data_modification.Split import split_data

# Chargement de la donnée

df = load_data()

# Prétraitement générale

df_processed = preprocess_input(df_input=df, columns_to_drop=settings.COLUMNS_TO_DROP, columns_to_clean=settings.COLUMNS_TO_CLEAN, columns_to_int=settings.COLUMNS_TO_INT, hour_column=settings.HOUR_COLUMN)

# Split _date 

x_train, y_train, X_test , y_test = split_data(df_input=df_processed, date_var=settings.DATE_COLUMN, split_date=settings.SPLIT_DATE, target_var=settings.TARGET)

#  Get dummies

x_train_dummy = pd.get_dummies(x_train, drop_first=True)

# Saves the dummy columns to be used later for inference

def dummy_data(df_input):
    """
    Applies one-hot encoding to categorical features in the input DataFrame.

    The resulting encoded DataFrame is aligned to match the column structure used 
    during model training. Any missing columns are added with a value of 0.

    Parameters
    ----------
    df_input : pandas.DataFrame
        Preprocessed input data containing both numeric and categorical features.

    Returns
    -------
    pandas.DataFrame
        One-hot encoded DataFrame with columns aligned to the training set's dummy variables.
    """
   
    df = df_input.copy()
    df_encoded = pd.get_dummies(df, drop_first=True).reindex(columns=x_train_dummy.columns, fill_value=0)
    
    return df_encoded

# Training models

modele = XGBClassifier(random_state=settings.SEED,  
                       min_samples_split=int(settings_models.MIN_SAMPLES_SPLIT_THRESHOLDS*len(x_train_dummy)), 
                       n_estimators=settings_models.N_ESTIMATORS, max_depth=settings_models.MAX_DEPTH, 
                       learning_rate=settings_models.LEARNING_RATE, objective=settings_models.OBJECTIVE, 
                       scale_pos_weight=settings_models.SCALE_POS_WEIGHT)

modele.fit(x_train_dummy, y_train)


