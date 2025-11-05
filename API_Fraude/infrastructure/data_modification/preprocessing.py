# API_Fraude/infrastructure/prepocessing.py
import pandas as pd
# from API_Fraude.application.train_and_saves import train_model


def preprocess_input(df_input, columns_to_drop : list, columns_to_clean : list, columns_to_int : list, hour_column):
    
    """
    Applies preprocessing steps to input data consistent with training-time transformations.

    This includes string cleaning, dropping irrelevant columns, converting data types,
    and extracting the hour from a time-formatted column.

    Args
    ----------
    df_input : pandas.DataFrame
        The raw input data to preprocess.
    columns_to_drop : list of str
        Column names to drop from the dataset (e.g., target label, identifiers).
    columns_to_clean : list of str
        Columns where string artifacts (e.g., byte-string notation) should be removed.
    columns_to_int : list of str
        Column names to convert to integer type.
    hour_column : str
        Name of the column containing time strings in '%H:%M:%S' format 
        to be converted to integer hour values.

    Returns
    -------
    pandas.DataFrame
        Preprocessed DataFrame ready for dummy encoding and model inference.
    """
    # Transformation identique à l'entraînement
   

    df = df_input.copy()
    
    # Nettoyage

    for col in columns_to_clean:
        df[col] = df[col].astype(str).str.replace("b", "", regex=False)
    
    # drop de variables inutiles dont la fraude qui n'est pas censé être connu ici

    df = df.drop(columns=[c for c in columns_to_drop if c in df.columns], errors='ignore')
   
    # Clean variable Heure. 
    # Modifier en date time après et prendre juste hour
    df[hour_column] = pd.to_datetime(df[hour_column], format='%H:%M:%S').dt.hour.astype(int)
    # df[hour_column] = df[hour_column].str[:2].astype(int)
   
    # Transformer en entier. tranformer en date time
    
    df[columns_to_int] = df[columns_to_int].astype(int)

    return df

# def dummy_data(df_input):
#     """
#     Applies one-hot encoding to categorical features in the input DataFrame.

#     The resulting encoded DataFrame is aligned to match the column structure used 
#     during model training. Any missing columns are added with a value of 0.

#     Parameters
#     ----------
#     df_input : pandas.DataFrame
#         Preprocessed input data containing both numeric and categorical features.

#     Returns
#     -------
#     pandas.DataFrame
#         One-hot encoded DataFrame with columns aligned to the training set's dummy variables.
#     """
   
#     df = df_input.copy()
#     df_encoded = pd.get_dummies(df, drop_first=True).reindex(columns=train_model.x_train_dummy.columns, fill_value=0)
    
#     return df_encoded
